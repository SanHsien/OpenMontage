"""music_selector routing: cost ceiling and the music_library tier."""

from __future__ import annotations

from tools.audio.music_library import MusicLibrary
from tools.audio.music_selector import MusicSelector
from tools.base_tool import BaseTool, ToolResult, ToolStatus


class _FakeTool(BaseTool):
    version = "0.0.0"
    input_schema = {"type": "object", "properties": {}}

    def __init__(self, name: str, capability: str) -> None:
        self.name = name
        self.provider = name
        self.capability = capability
        self.calls: list[dict] = []

    def get_status(self) -> ToolStatus:
        return ToolStatus.AVAILABLE

    def execute(self, inputs: dict) -> ToolResult:
        self.calls.append(inputs)
        return ToolResult(success=True, data={"output": f"{self.name}.mp3"})


def _selector(monkeypatch, tools_by_capability: dict[str, list[BaseTool]]) -> MusicSelector:
    selector = MusicSelector()
    monkeypatch.setattr(selector, "_tools_for", lambda cap: tools_by_capability.get(cap, []))
    return selector


def test_unknown_cost_ceiling_does_not_allow_paid_generation(monkeypatch):
    paid = _FakeTool("paid_gen", "music_generation")
    selector = _selector(monkeypatch, {"music_generation": [paid]})

    result = selector.execute({"operation": "acquire", "prompt": "calm", "max_cost_tier": "free"})

    assert not result.success
    assert "max_cost_tier" in result.error
    assert paid.calls == []
    assert selector.estimate_cost({"operation": "acquire", "max_cost_tier": "free"}) == 0.0


def _library_with_default(monkeypatch, tmp_path, default_has_tracks: bool) -> MusicLibrary:
    default_dir = tmp_path / "default_library"
    default_dir.mkdir()
    if default_has_tracks:
        (default_dir / "default.mp3").write_bytes(b"ID3")
    monkeypatch.setenv("MUSIC_LIBRARY_DIR", str(default_dir))
    monkeypatch.setattr(MusicLibrary, "_probe_duration", staticmethod(lambda path: None))
    return MusicLibrary()


def test_empty_library_dir_falls_through_to_stock_search(monkeypatch, tmp_path):
    library = _library_with_default(monkeypatch, tmp_path, default_has_tracks=True)
    search = _FakeTool("stock_search", "music_search")
    selector = _selector(monkeypatch, {"music_library": [library], "music_search": [search]})
    empty = tmp_path / "empty"
    empty.mkdir()

    result = selector.execute({"operation": "acquire", "query": "calm", "library_dir": str(empty)})

    assert result.success, result.error
    assert result.data["selected_tool"] == "stock_search"
    assert result.data["attempted"] == ["stock_search"]


def test_library_dir_with_tracks_is_used_before_paid_generation(monkeypatch, tmp_path):
    library = _library_with_default(monkeypatch, tmp_path, default_has_tracks=False)
    paid = _FakeTool("paid_gen", "music_generation")
    selector = _selector(monkeypatch, {"music_library": [library], "music_generation": [paid]})
    own = tmp_path / "own"
    own.mkdir()
    (own / "theme.wav").write_bytes(b"RIFF")

    result = selector.execute({"operation": "acquire", "prompt": "calm", "library_dir": str(own)})

    assert result.success, result.error
    assert result.data["selected_tool"] == "music_library"
    assert [t["name"] for t in result.data["tracks"]] == ["theme.wav"]
    assert paid.calls == []
