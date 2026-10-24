import ast
import os
import subprocess
import sys
from pathlib import Path

import nbformat
import pytest
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from make_student_notebooks import make_student  # noqa: E402
from setup_cell import SETUP_CELL  # noqa: E402


def sample_notebook():
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell("# Başlık"),
        new_code_cell(
            "x = 1\n"
            "# BEGIN SOLUTION\n"
            "y = x + 1\n"
            "# END SOLUTION\n"
            "def f():\n"
            "    # BEGIN SOLUTION\n"
            "    return 42\n"
            "    # END SOLUTION\n"
            "print(y)",
            outputs=[new_output("stream", name="stdout", text="2\n")],
            execution_count=3,
        ),
        new_code_cell("assert y == 2", metadata={"tags": ["solution-only"]}),
    ]
    return nb


def strip_ipython(source: str) -> str:
    return "\n".join(
        line[: len(line) - len(line.lstrip())] + "pass" if line.strip().startswith(("!", "%")) else line
        for line in source.splitlines()
    )


def test_student_has_no_solution():
    student = make_student(sample_notebook())
    text = nbformat.writes(student)
    assert "BEGIN SOLUTION" not in text
    assert "return 42" not in text
    assert "y = x + 1" not in text
    assert len(student.cells) == 2
    code = student.cells[1]
    assert code.outputs == []
    assert code.execution_count is None
    assert "    # TODO: kendin yaz\n    ..." in code.source
    assert "# TODO: kendin yaz\n...\ndef f():" in code.source


def test_student_ids_match_nbstripout():
    student = make_student(sample_notebook())
    assert [c.id for c in student.cells] == ["0", "1"]


def test_student_is_valid_python():
    nb = sample_notebook()
    nb.cells.insert(1, new_code_cell(SETUP_CELL))
    for cell in make_student(nb).cells:
        if cell.cell_type == "code":
            ast.parse(strip_ipython(cell.source))


def run_setup_cell_as_colab(tmp_path: Path):
    """SETUP_CELL'in Colab dalını simüle eder: git clone, içinde src/model.py olan bir klasör oluşturur."""
    content = tmp_path / "content"
    content.mkdir(exist_ok=True)
    source = SETUP_CELL.replace("/content", str(content))
    lines = []
    for line in source.splitlines():
        stripped = line.strip()
        indent = line[: len(line) - len(line.lstrip())]
        if stripped.startswith("!rm -rf"):
            lines.append(f"{indent}shutil.rmtree(TARGET, ignore_errors=True)")
        elif stripped.startswith("!git clone"):
            lines.append(f"{indent}os.makedirs(os.path.join(TARGET, 'src')); open(os.path.join(TARGET, 'src', 'model.py'), 'w').close()")
        elif stripped.startswith("%cd"):
            lines.append(f"{indent}os.chdir(TARGET)")
        elif stripped.startswith("%pip"):
            lines.append(f"{indent}pass")
        else:
            lines.append(line)
    code = "import shutil\n" + "\n".join(lines)
    sys.modules["google.colab"] = type(sys)("google.colab")
    cwd, path = os.getcwd(), list(sys.path)
    try:
        exec(code, {})
    finally:
        os.chdir(cwd)
        sys.path[:] = path
        del sys.modules["google.colab"]
    return content / "python-cevresel-modelleme"


def test_setup_cell_idempotent(tmp_path):
    target = run_setup_cell_as_colab(tmp_path)
    (target / "notum.txt").write_text("kalmalı")
    run_setup_cell_as_colab(tmp_path)
    assert (target / "notum.txt").exists(), "ikinci çalıştırma repoyu yeniden klonlamamalı"
    assert sorted(p.name for p in target.parent.iterdir()) == ["python-cevresel-modelleme"]


def test_setup_cell_retries_partial_clone(tmp_path):
    """Yarıda kalmış bir klon (klasör var, src/model.py yok) yeniden indirilmeli."""
    partial = tmp_path / "content" / "python-cevresel-modelleme"
    partial.mkdir(parents=True)
    target = run_setup_cell_as_colab(tmp_path)
    assert (target / "src" / "model.py").exists()


def test_setup_cell_local_outside_repo_raises(tmp_path):
    cwd, path = os.getcwd(), list(sys.path)
    try:
        os.chdir(tmp_path)
        with pytest.raises(RuntimeError, match="repo"):
            exec(strip_ipython(SETUP_CELL), {})
    finally:
        os.chdir(cwd)
        sys.path[:] = path


def test_setup_cell_local_finds_repo_root_from_bonus(tmp_path):
    """Yerelde, kendi requirements.txt dosyası olan bir bonus klasöründen de repo köküne çıkmalı."""
    root = tmp_path / "repo"
    module = root / "bonus" / "ornek-modul"
    module.mkdir(parents=True)
    (root / "src").mkdir()
    (root / "src" / "model.py").write_text("")
    (root / "requirements.txt").write_text("")
    (module / "requirements.txt").write_text("")
    cwd, path = os.getcwd(), list(sys.path)
    try:
        os.chdir(module)
        exec(strip_ipython(SETUP_CELL), {})
        assert Path(os.getcwd()).resolve() == root.resolve()
    finally:
        os.chdir(cwd)
        sys.path[:] = path


def test_check_mode_detects_drift(tmp_path):
    (tmp_path / "cozumler").mkdir()
    (tmp_path / "notebooks").mkdir()
    nbformat.write(sample_notebook(), tmp_path / "cozumler" / "01_ornek.ipynb")
    script = ROOT / "scripts" / "make_student_notebooks.py"
    run = lambda *a: subprocess.run([sys.executable, str(script), "--root", str(tmp_path), *a])  # noqa: E731
    assert run("--check").returncode == 1
    assert run().returncode == 0
    assert run("--check").returncode == 0


def test_first_cell_is_setup_cell():
    solutions = sorted((ROOT / "cozumler").glob("*.ipynb")) + sorted((ROOT / "bonus").glob("*/cozum.ipynb"))
    assert solutions
    for path in solutions:
        nb = nbformat.read(path, as_version=4)
        assert nb.cells[0].source == SETUP_CELL, f"{path.name}: ilk hücre SETUP_CELL değil"
