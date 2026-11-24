"""Offline checks for credential instructions and agent documentation links."""

from pathlib import Path
import os
import re
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
BFL_FILES = [
    f"{tree}/skills/bfl-api/{name}"
    for tree in (".agents", ".claude")
    for name in ("SKILL.md", "references/api-key-setup.md")
]
LINK_FILES = [
    f"{tree}/skills/{name}"
    for tree in (".agents", ".claude")
    for name in (
        "flux-best-practices/AGENTS.md",
        "manimgl-best-practices/SKILL.md",
    )
] + [
    ".claude/skills/d3-viz/SKILL.md",
    ".claude/skills/remotion-best-practices/SKILL.md",
]


@pytest.mark.parametrize("relative", BFL_FILES)
def test_bfl_instructions_keep_credentials_out_of_agent_output(relative):
    text = (ROOT / relative).read_text(encoding="utf-8")
    assert not re.search(r"(?im)^\s*(?:echo|printenv)\s+[\"']?\$?BFL_API_KEY", text)
    # A bare grep prints the complete .env assignment, even after echo is removed.
    assert not re.search(r"(?im)^\s*grep\b[^\n]*\.env", text)
    assert "paste it here" not in text.lower()
    assert "never request raw api keys in chat" in text.lower()


@pytest.mark.parametrize("relative", BFL_FILES)
@pytest.mark.parametrize("key", ["", "test-only-secret-do-not-print"])
def test_documented_presence_check_never_prints_the_key(relative, key):
    text = (ROOT / relative).read_text(encoding="utf-8")
    snippets = re.findall(r'python -c "([^"\n]+)"', text)
    assert snippets, f"{relative}: no cross-platform presence check"
    for code in set(snippets):
        result = subprocess.run(
            [sys.executable, "-c", code],
            env={**os.environ, "BFL_API_KEY": key},
            capture_output=True, text=True, check=True, timeout=10,
        )
        expected = "OK: Key configured" if key else "Error: BFL_API_KEY not set"
        assert result.stdout.strip() == expected
        assert not result.stderr


@pytest.mark.parametrize("relative", LINK_FILES)
def test_agent_skill_local_references_exist(relative):
    source = ROOT / relative
    text = source.read_text(encoding="utf-8")
    targets = re.findall(r"\]\(([^)]+)\)", text)
    if "/d3-viz/" in relative:
        targets += [f"assets/{name}" for name in re.findall(r"`([^`\s]*-template\.[a-z]+)`", text)]
    local = [target.split("#", 1)[0] for target in targets if ":" not in target]
    assert any(local), f"{relative}: no local references checked"
    missing = [target for target in local if target and not (source.parent / target).exists()]
    assert not missing, f"{relative}: missing {missing}"


VIDEO_TOOLKIT_FILES = [
    ".agents/skills/video-toolkit/SKILL.md",
    ".claude/skills/video_toolkit/SKILL.md",
]


@pytest.mark.parametrize("relative", VIDEO_TOOLKIT_FILES)
def test_video_toolkit_env_check_lists_names_not_values(relative):
    # `cat .env | grep MODAL` prints whole assignments, including any Modal token.
    text = (ROOT / relative).read_text(encoding="utf-8")
    assert not re.search(r"(?im)^\s*cat\b[^\n]*\.env", text)
    for line in re.findall(r"(?im)^\s*grep\b[^\n]*\.env[^\n]*$", text):
        assert re.search(r"\bgrep\s+-o\s+'\^MODAL\[A-Z0-9_\]\*'", line), line
