import ast
import os
import subprocess
import sys
from pathlib import Path

import nbformat
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


def test_student_is_valid_python():
    nb = sample_notebook()
    nb.cells.insert(1, new_code_cell(SETUP_CELL))
    for cell in make_student(nb).cells:
        if cell.cell_type == "code":
            ast.parse(strip_ipython(cell.source))


def run_setup_cell_as_colab(tmp_path: Path):
    """SETUP_CELL'in Colab dalını, git clone yerine klasör oluşturarak simüle eder."""
    content = tmp_path / "content"
    content.mkdir(exist_ok=True)
    source = SETUP_CELL.replace("/content", str(content))
    lines = []
    for line in source.splitlines():
        stripped = line.strip()
        indent = line[: len(line) - len(line.lstrip())]
        if stripped.startswith("!git clone"):
            target = stripped.split()[-1]
            lines.append(f"{indent}os.makedirs({target!r})")
        elif stripped.startswith("%cd"):
            lines.append(f"{indent}os.chdir({stripped.split(maxsplit=1)[1]!r})")
        elif stripped.startswith("%pip"):
            lines.append(f"{indent}pass")
        else:
            lines.append(line)
    code = "\n".join(lines)
    fake_colab = type(sys)("google.colab")
    sys.modules["google.colab"] = fake_colab
    cwd = os.getcwd()
    try:
        exec(code, {})
    finally:
        os.chdir(cwd)
        del sys.modules["google.colab"]
    return content


def test_setup_cell_idempotent(tmp_path):
    content = run_setup_cell_as_colab(tmp_path)
    run_setup_cell_as_colab(tmp_path)
    assert [p.name for p in content.iterdir()] == ["python-cevresel-modelleme"]
    assert list((content / "python-cevresel-modelleme").iterdir()) == []


def test_check_mode_detects_drift(tmp_path):
    (tmp_path / "cozumler").mkdir()
    (tmp_path / "notebooks").mkdir()
    nbformat.write(sample_notebook(), tmp_path / "cozumler" / "01_ornek.ipynb")
    script = ROOT / "scripts" / "make_student_notebooks.py"
    run = lambda *a: subprocess.run([sys.executable, str(script), "--root", str(tmp_path), *a])  # noqa: E731
    assert run("--check").returncode == 1
    assert run().returncode == 0
    assert run("--check").returncode == 0
