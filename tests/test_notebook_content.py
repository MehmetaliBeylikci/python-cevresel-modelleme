"""Notebook içeriğinin, katılımcıyı takılacağı bir duruma sokmadığını ve anlatımın çıktılarla çelişmediğini kontrol eder."""
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]


def code_of(path):
    nb = nbformat.read(ROOT / path, as_version=4)
    return [c.source for c in nb.cells if c.cell_type == "code"]


def text_of(path):
    return "\n".join(c.source for c in nbformat.read(ROOT / path, as_version=4).cells)


def test_day3_tolerates_any_scenario_name():
    """Öğrenci birleşik senaryoya farklı bir ad verirse sonraki grafik hücreleri KeyError vermemeli."""
    for source in code_of("cozumler/03_gorsellestirme_senaryolar.ipynb"):
        assert "colors[name]" not in source


def test_day3_prompt_names_combined_scenario():
    assert '"Hepsi birlikte"' in text_of("notebooks/03_gorsellestirme_senaryolar.ipynb").split("Alıştırma 2")[1].split("# TODO")[0]


def test_day2_student_keeps_spill_initialisation():
    """spill = 0.0 boşluğun dışında olmalı; yoksa doğru yazan öğrenci ilk ayda NameError alır."""
    student = next(s for s in code_of("notebooks/02_model_kurulumu.ipynb") if "def my_simulate(" in s)
    before_blank = student.split("# TODO")[0]
    assert "spill = 0.0" in before_blank


def test_day2_prose_does_not_claim_70_80_band():
    for path in ["cozumler/02_model_kurulumu.ipynb", "docs/parametreler.md"]:
        text = (ROOT / path).read_text(encoding="utf-8")
        assert "%70–80" not in text, path


def test_local_install_includes_jupyter():
    assert "jupyterlab" in (ROOT / "requirements.txt").read_text()
