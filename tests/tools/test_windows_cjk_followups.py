"""Windows locale / CJK follow-ups ported from open upstream PRs.

Ported as approaches, not diffs, because the upstream PRs are unmerged:
- piper_tts must feed narration to Piper as UTF-8 (upstream PR #842).
- text-mode subprocess calls in video_compose must decode as UTF-8 so a
  cp950/cp936 console locale cannot kill the pipe reader (upstream PR #696).
- subtitle_gen must not put spaces between adjacent CJK tokens (upstream
  PR #828, defect 1 of PR #725).
"""

from __future__ import annotations

import ast
import subprocess
from pathlib import Path
from types import SimpleNamespace

from tools.subtitle.subtitle_gen import SubtitleGen, _join_tokens

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_piper_sends_text_to_piper_as_utf8(monkeypatch, tmp_path):
    from tools.audio import piper_tts

    seen: dict = {}

    def fake_run(cmd, **kwargs):
        seen.update(kwargs)
        Path(cmd[cmd.index("--output_file") + 1]).write_bytes(b"RIFF")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(piper_tts.subprocess, "run", fake_run)
    result = piper_tts.PiperTTS()._generate(
        {"text": "你好，世界 Olá", "output_path": str(tmp_path / "out.wav")}
    )

    assert result.success, result.error
    assert seen["input"] == "你好，世界 Olá"
    assert seen["encoding"] == "utf-8"
    assert seen["errors"] == "replace"


def test_video_compose_text_subprocess_calls_decode_utf8():
    tree = ast.parse((REPO_ROOT / "tools/video/video_compose.py").read_text(encoding="utf-8"))
    offenders = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (
            isinstance(func, ast.Attribute)
            and isinstance(func.value, ast.Name)
            and func.value.id == "subprocess"
            and func.attr in {"run", "check_output", "Popen"}
        ):
            continue
        kwargs = {kw.arg: kw.value for kw in node.keywords if kw.arg}
        text_mode = isinstance(kwargs.get("text"), ast.Constant) and kwargs["text"].value is True
        if text_mode and "encoding" not in kwargs:
            offenders.append(node.lineno)
    assert not offenders, f"text-mode subprocess without encoding= at lines {offenders}"


def test_join_tokens_keeps_cjk_words_together():
    assert _join_tokens(["人", "工", "智", "能"]) == "人工智能"
    assert _join_tokens(["Hello", " world"]) == "Hello world"
    # A Latin word next to CJK keeps its space; CJK run stays joined.
    assert _join_tokens(["AI", "人工", "很", "好"]) == "AI 人工很好"
    # Karaoke markup does not hide the CJK boundary.
    assert _join_tokens(["<b>人</b>", "工"]) == "<b>人</b>工"


def test_cues_and_srt_do_not_space_out_chinese_characters():
    segments = [
        {
            "start": 0.0,
            "end": 2.0,
            "text": "人工智能很好",
            "words": [
                {"word": ch, "start": i * 0.3, "end": i * 0.3 + 0.3}
                for i, ch in enumerate("人工智能很好")
            ],
        }
    ]
    gen = SubtitleGen()
    cues = gen._build_cues(segments, max_words=10, max_chars=40)
    assert [c["text"] for c in cues] == ["人工智能很好"]
    assert "人工智能很好" in gen._render_srt(cues)
    assert "<b>人</b><b>" not in gen._render_srt(cues, highlight_style="karaoke")


def test_apply_corrections_keeps_chinese_segment_text_unspaced():
    segments = [
        {
            "start": 0.0,
            "end": 1.0,
            "text": "作用",
            "words": [
                {"word": "做", "start": 0.0, "end": 0.5},
                {"word": "用", "start": 0.5, "end": 1.0},
            ],
        }
    ]
    fixed = SubtitleGen._apply_corrections(segments, {"做": "作"})
    assert fixed[0]["text"] == "作用"


def test_subprocess_module_is_not_shadowed():
    # Guard for the monkeypatching above: piper_tts imports subprocess directly.
    from tools.audio import piper_tts

    assert piper_tts.subprocess is subprocess


# --- final_review black-frame check (closed-unmerged upstream PR #679) -------

import shutil  # noqa: E402

import pytest  # noqa: E402

_needs_ffmpeg = pytest.mark.skipif(
    not (shutil.which("ffmpeg") and shutil.which("ffprobe")), reason="ffmpeg not installed"
)


def _render_color_clip(tmp_path, color: str) -> Path:
    out = tmp_path / f"{color}.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", f"color=c={color}:s=1280x720:d=4",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=4",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(out),
        ],
        check=True, capture_output=True, timeout=60,
    )
    return out


@_needs_ffmpeg
def test_final_review_flags_a_black_render(tmp_path):
    from tools.video.video_compose import VideoCompose

    review = VideoCompose()._run_final_review(_render_color_clip(tmp_path, "black"))
    assert review["checks"]["visual_spotcheck"]["black_frames_detected"] is True


@_needs_ffmpeg
def test_final_review_does_not_flag_a_non_black_render(tmp_path):
    from tools.video.video_compose import VideoCompose

    review = VideoCompose()._run_final_review(_render_color_clip(tmp_path, "0x404040"))
    assert review["checks"]["visual_spotcheck"]["black_frames_detected"] is False
