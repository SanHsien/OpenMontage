"""Regression tests for video_trimmer concat losing video.

_concat placed -ss/-to AFTER -i while stream-copying. That is an output seek,
which with -c copy keeps only whole packets from the next keyframe — every
timed segment collapsed to a single video frame, and concatenating them
produced a file with no usable video. The tool returned success:True anyway,
so a nine-shot assembly came back as audio only.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.video.video_trimmer import VideoTrimmer  # noqa: E402

pytestmark = pytest.mark.skipif(
    shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None,
    reason="ffmpeg/ffprobe required to build the fixture clips",
)


def _frame_count(path: Path) -> int:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    out = proc.stdout.strip().split("\n")[0].strip()
    return int(out) if out.isdigit() else 0


@pytest.fixture
def clips(tmp_path) -> list[Path]:
    """Two 6s 320x240 25fps clips with audio and a 2s keyframe interval."""
    made = []
    for i, pattern in enumerate(("testsrc", "smptebars")):
        out = tmp_path / f"src{i}.mp4"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y",
             "-f", "lavfi", "-i", f"{pattern}=size=320x240:rate=25:duration=6",
             "-f", "lavfi", "-i", "sine=frequency=440:duration=6",
             "-c:v", "libx264", "-g", "50", "-pix_fmt", "yuv420p",
             "-c:a", "aac", str(out)],
            check=True,
        )
        made.append(out)
    return made


def test_concat_keeps_video_across_timed_segments(clips, tmp_path):
    out = tmp_path / "joined.mp4"
    result = VideoTrimmer().execute({
        "operation": "concat",
        "codec": "libx264",
        "segments": [
            {"input_path": str(clips[0]), "start_seconds": 1.4, "end_seconds": 3.4},
            {"input_path": str(clips[1]), "start_seconds": 0.6, "end_seconds": 2.6},
        ],
        "output_path": str(out),
    })

    assert result.success, result.error
    assert out.exists()
    # 2s + 2s at 25fps. One frame per segment was the bug.
    assert _frame_count(out) > 80, "video frames were dropped by the segment cut"


def test_concat_reports_failure_instead_of_a_videoless_file(clips, tmp_path, monkeypatch):
    """A concat that yields no video must not return success."""
    trimmer = VideoTrimmer()
    monkeypatch.setattr(trimmer, "_has_video_stream", lambda path: False)

    result = trimmer.execute({
        "operation": "concat",
        "segments": [{"input_path": str(clips[0]), "start_seconds": 1.0, "end_seconds": 3.0}],
        "output_path": str(tmp_path / "broken.mp4"),
    })

    assert not result.success
    assert "no video stream" in (result.error or "")
