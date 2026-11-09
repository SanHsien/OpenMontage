r"""Piper installed beside the running interpreter is found without activating the venv.

Windows-first: `.venv\Scripts\python.exe -m ...` leaves `Scripts` off PATH, so
`shutil.which("piper")` alone reports an installed Piper as unavailable.
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

from tools.audio.piper_tts import PiperTTS
from tools.base_tool import ToolStatus


@pytest.fixture
def interpreter_dir(tmp_path, monkeypatch):
    scripts = tmp_path / "venv" / "Scripts"
    scripts.mkdir(parents=True)
    empty_path = tmp_path / "empty-path"
    empty_path.mkdir()
    monkeypatch.setenv("PATH", str(empty_path))
    monkeypatch.setattr(sys, "executable", str(scripts / "python.exe"))
    return scripts


def _launcher(directory):
    path = directory / ("piper.exe" if os.name == "nt" else "piper")
    path.write_bytes(b"test launcher")
    path.chmod(0o755)
    return path


def test_launcher_beside_interpreter_counts_as_available(interpreter_dir):
    _launcher(interpreter_dir)
    assert PiperTTS().get_status() == ToolStatus.AVAILABLE


def test_missing_launcher_stays_unavailable(interpreter_dir):
    assert PiperTTS().get_status() == ToolStatus.UNAVAILABLE


def test_directory_named_piper_is_not_a_launcher(interpreter_dir):
    (interpreter_dir / "piper").mkdir()
    (interpreter_dir / "piper.exe").mkdir()
    assert PiperTTS().get_status() == ToolStatus.UNAVAILABLE


def test_generate_runs_the_discovered_launcher(interpreter_dir, tmp_path, monkeypatch):
    launcher = _launcher(interpreter_dir)
    output = tmp_path / "audio.wav"
    seen = {}

    def fake_run(argv, **kwargs):
        seen["argv0"] = argv[0]
        output.write_bytes(b"audio")
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr(subprocess, "run", fake_run)
    result = PiperTTS().execute(
        {"text": "Hello", "model": "voice.onnx", "output_path": str(output)}
    )
    assert result.success, result.error
    assert os.path.samefile(seen["argv0"], launcher)
