"""music_selector routing: cost ceiling and the music_library tier."""

from __future__ import annotations

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

