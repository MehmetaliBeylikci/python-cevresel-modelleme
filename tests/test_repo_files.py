from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPO_URL = "https://github.com/MehmetaliBeylikci/python-cevresel-modelleme"

REQUIRED_FILES = [
    ".gitignore",
    "requirements.txt",
    "requirements-dev.txt",
    ".pre-commit-config.yaml",
    "LICENSE",
    "LICENSE-CONTENT.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "CITATION.cff",
    "README.md",
    ".github/ISSUE_TEMPLATE/hata.yml",
    ".github/ISSUE_TEMPLATE/icerik-onerisi.yml",
    ".github/pull_request_template.md",
]

YAML_FILES = [
    "CITATION.cff",
    ".pre-commit-config.yaml",
    ".github/ISSUE_TEMPLATE/hata.yml",
    ".github/ISSUE_TEMPLATE/icerik-onerisi.yml",
]


def test_required_files_exist():
    missing = [f for f in REQUIRED_FILES if not (ROOT / f).is_file()]
    assert missing == []


def test_yaml_files_parse():
    for f in YAML_FILES:
        assert yaml.safe_load((ROOT / f).read_text(encoding="utf-8")) is not None, f


def test_citation_fields():
    cff = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    assert cff["cff-version"] == "1.2.0"
    assert cff["repository-code"] == REPO_URL


def test_funding_points_to_github_sponsors():
    funding = yaml.safe_load((ROOT / ".github" / "FUNDING.yml").read_text(encoding="utf-8"))
    assert funding == {"github": ["MehmetaliBeylikci"]}
    assert "github.com/sponsors/MehmetaliBeylikci" in (ROOT / "README.md").read_text(encoding="utf-8")
