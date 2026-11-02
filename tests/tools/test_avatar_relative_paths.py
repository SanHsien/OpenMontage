"""Avatar tools run the model's inference script with cwd set to the model dir.

Ported as an approach from open upstream PR #873: relative input paths must be
resolved against the caller's cwd *before* the subprocess starts, otherwise the
child (cwd = Wav2Lip / SadTalker checkout) cannot find the files.
"""

from __future__ import annotations

import os
from pathlib import Path

from tools.avatar.lip_sync import LipSync
from tools.avatar.talking_head import TalkingHead


def _option_value(cmd: list[str], flag: str) -> str:
    return cmd[cmd.index(flag) + 1]


def test_lip_sync_passes_absolute_paths_to_wav2lip(monkeypatch, tmp_path):
    model_dir = tmp_path / "Wav2Lip"
    (model_dir / "checkpoints").mkdir(parents=True)
    (model_dir / "inference.py").write_text("", encoding="utf-8")
    from tools.avatar import lip_sync

    (model_dir / "checkpoints" / lip_sync.MODEL_CHECKPOINTS["wav2lip"]).write_bytes(b"x")
    work = tmp_path / "work"
    work.mkdir()
    (work / "face.mp4").write_bytes(b"v")
    (work / "voice.wav").write_bytes(b"a")
    monkeypatch.setenv("WAV2LIP_PATH", str(model_dir))
    monkeypatch.chdir(work)

    captured: dict = {}

    def fake_run(self, cmd, **kwargs):
        captured["cmd"] = cmd
        captured["cwd"] = kwargs.get("cwd")
        Path(_option_value(cmd, "--outfile")).write_bytes(b"out")

    monkeypatch.setattr(LipSync, "run_command", fake_run)

    result = LipSync().execute({"video_path": "face.mp4", "audio_path": "voice.wav"})

    assert result.success, result.error
    for flag in ("--face", "--audio", "--outfile"):
        assert os.path.isabs(_option_value(captured["cmd"], flag)), flag
    assert Path(captured["cwd"]) == model_dir


def test_talking_head_passes_absolute_paths_to_sadtalker(monkeypatch, tmp_path):
    model_dir = tmp_path / "SadTalker"
    model_dir.mkdir()
    work = tmp_path / "work"
    work.mkdir()
    (work / "face.png").write_bytes(b"i")
    (work / "voice.wav").write_bytes(b"a")
    monkeypatch.setenv("SADTALKER_PATH", str(model_dir))
    monkeypatch.chdir(work)

    captured: dict = {}

    def fake_run(self, cmd, **kwargs):
        captured["cmd"] = cmd
        result_dir = Path(_option_value(cmd, "--result_dir"))
        (result_dir / "run1").mkdir(parents=True, exist_ok=True)
        (result_dir / "run1" / "gen.mp4").write_bytes(b"out")

    monkeypatch.setattr(TalkingHead, "run_command", fake_run)

    result = TalkingHead().execute(
        {"image_path": "face.png", "audio_path": "voice.wav", "model": "sadtalker"}
    )

    assert result.success, result.error
    for flag in ("--driven_audio", "--source_image", "--result_dir"):
        assert os.path.isabs(_option_value(captured["cmd"], flag)), flag
