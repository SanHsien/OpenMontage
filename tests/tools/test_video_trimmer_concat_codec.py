"""concat must understand the schema default codec "auto" (no ffmpeg needed)."""

from tools.video.video_trimmer import VideoTrimmer


def _run(tmp_path, monkeypatch, codec):
    source = tmp_path / "in.mp4"
    source.write_bytes(b"x")
    commands = []
    tool = VideoTrimmer()
    monkeypatch.setattr(tool, "run_command", lambda cmd, *a, **k: commands.append(list(cmd)))
    monkeypatch.setattr(tool, "_has_video_stream", lambda _p: True)
    inputs = {
        "operation": "concat",
        "segments": [{"input_path": str(source), "start_seconds": 1, "end_seconds": 2}],
        "output_path": str(tmp_path / "out.mp4"),
    }
    if codec is not None:
        inputs["codec"] = codec
    tool._concat(inputs)
    return commands


def test_auto_codec_is_never_passed_to_ffmpeg_as_an_encoder(tmp_path, monkeypatch):
    for codec in ("auto", None):
        first = _run(tmp_path, monkeypatch, codec)[0]
        assert "auto" not in first
        assert first[first.index("-c") + 1] == "copy"


def test_explicit_encoder_is_still_used(tmp_path, monkeypatch):
    first = _run(tmp_path, monkeypatch, "libx264")[0]
    assert first[first.index("-c:v") + 1] == "libx264"
