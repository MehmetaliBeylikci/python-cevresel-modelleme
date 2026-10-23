"""Repodaki metin dosyalarında emoji ve yapay zekâ atfı bulunmamalı."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EMOJI = re.compile("[%s-%s%s-%s%s%s%s]" % tuple(chr(c) for c in (0x1F300, 0x1FAFF, 0x2600, 0x27BF, 0x2B50, 0x25B6, 0xFE0F)))
TEXT_SUFFIXES = {".md", ".py", ".ipynb", ".yml", ".yaml", ".cff", ".txt", ".csv"}


def tracked_text_files():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [ROOT / f for f in out.splitlines() if Path(f).suffix in TEXT_SUFFIXES]


def test_no_emoji_in_files():
    offenders = []
    for path in tracked_text_files():
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if EMOJI.search(line):
                offenders.append(f"{path.relative_to(ROOT)}:{n}")
    assert offenders == []


def test_no_ai_attribution_in_files():
    pattern = re.compile(r"\b(claude|anthropic)\b", re.IGNORECASE)
    offenders = [str(p.relative_to(ROOT)) for p in tracked_text_files()
                 if p.name != "test_repo_style.py" and pattern.search(p.read_text(encoding="utf-8"))]
    assert offenders == []
