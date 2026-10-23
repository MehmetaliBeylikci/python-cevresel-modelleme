"""Çözümlü notebook'lardan katılımcı (boşluklu) notebook'larını üretir.

Kullanım:
    python scripts/make_student_notebooks.py           # notebook'ları yazar
    python scripts/make_student_notebooks.py --check   # güncel değilse exit 1

Eşlemeler:
    cozumler/NN_ad.ipynb       → notebooks/NN_ad.ipynb
    bonus/<modul>/cozum.ipynb  → bonus/<modul>/<modul (tire yerine alt çizgi)>.ipynb

Kurallar:
    # BEGIN SOLUTION ... # END SOLUTION arası, aynı girintiyle "# TODO: kendin yaz" + "..." olur.
    "solution-only" etiketli hücreler silinir. Tüm çıktılar temizlenir.
"""

import argparse
import copy
import sys
from pathlib import Path

import nbformat

BEGIN = "# BEGIN SOLUTION"
END = "# END SOLUTION"


def _blank_solutions(source: str) -> str:
    out = []
    inside = False
    for line in source.splitlines():
        stripped = line.strip()
        if stripped == BEGIN:
            indent = line[: len(line) - len(line.lstrip())]
            out += [f"{indent}# TODO: kendin yaz", f"{indent}..."]
            inside = True
        elif stripped == END:
            inside = False
        elif not inside:
            out.append(line)
    return "\n".join(out)


def make_student(nb: nbformat.NotebookNode) -> nbformat.NotebookNode:
    student = copy.deepcopy(nb)
    cells = []
    for cell in student.cells:
        if "solution-only" in cell.get("metadata", {}).get("tags", []):
            continue
        if cell.cell_type == "code":
            cell.source = _blank_solutions(cell.source)
            cell.outputs = []
            cell.execution_count = None
        cells.append(cell)
    student.cells = cells
    return student


def pairs(root: Path):
    for src in sorted((root / "cozumler").glob("*.ipynb")):
        yield src, root / "notebooks" / src.name
    for src in sorted((root / "bonus").glob("*/cozum.ipynb")):
        yield src, src.parent / (src.parent.name.replace("-", "_") + ".ipynb")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Yazma; güncel değilse 1 ile çık")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    stale = []
    for src, dst in pairs(args.root):
        expected = nbformat.writes(make_student(nbformat.read(src, as_version=4))) + "\n"
        current = dst.read_text(encoding="utf-8") if dst.exists() else None
        if current == expected:
            continue
        if args.check:
            stale.append(dst)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(expected, encoding="utf-8")
            print(f"yazıldı: {dst.relative_to(args.root)}")

    for dst in stale:
        print(f"güncel değil: {dst.relative_to(args.root)}", file=sys.stderr)
    if stale:
        print("Çalıştırın: python scripts/make_student_notebooks.py", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
