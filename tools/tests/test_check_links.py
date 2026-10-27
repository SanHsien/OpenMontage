"""check_links must judge paths the way GitHub serves them: case-sensitive."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_links


def _tree(tmp_path: Path, monkeypatch) -> Path:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "DECISIONS.md").write_text("# d\n", encoding="utf-8")
    monkeypatch.setattr(check_links, "ROOT", tmp_path)
    return tmp_path


def test_link_with_wrong_case_is_reported(tmp_path, monkeypatch):
    root = _tree(tmp_path, monkeypatch)
    readme = root / "README.md"
    readme.write_text("[d](docs/decisions.md) [D](Docs/DECISIONS.md)\n", encoding="utf-8")

    problems = check_links.check_document(readme)

    assert len(problems) == 2, problems


def test_link_with_exact_case_passes(tmp_path, monkeypatch):
    root = _tree(tmp_path, monkeypatch)
    readme = root / "README.md"
    readme.write_text("[d](docs/DECISIONS.md#top) [here](./README.md)\n", encoding="utf-8")

    assert check_links.check_document(readme) == []


def test_maintained_document_with_wrong_case_is_missing(tmp_path, monkeypatch):
    _tree(tmp_path, monkeypatch)
    monkeypatch.setattr(check_links, "MAINTAINED_DOCUMENTS", ("docs/decisions.md",))

    try:
        check_links.iter_documents()
    except FileNotFoundError as exc:
        assert "docs/decisions.md" in str(exc)
    else:
        raise AssertionError("wrong-case maintained document was accepted")
