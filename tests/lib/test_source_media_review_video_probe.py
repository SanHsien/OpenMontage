"""Regression tests for video probing in source_media_review.

Three defects made every reviewed video carry false metadata while still
asserting reviewed: true —

1. audio_probe's audio-shaped result was assigned to technical_probe wholesale,
   so resolution/fps/audio_codec were absent and the ffprobe fallback that
   supplies them was gated behind `if not result["technical_probe"]`. A
   1280x720 clip with an AAC track summarized as "at unknown, without audio".
2. frame_sampler was called without its required "strategy" input, raising
   KeyError into a swallowing `except Exception`.
3. The sampler's result was read as data["frame_paths"]; it returns "frames".

Together they meant no video was ever frame-sampled and every video's
resolution and audio track were reported wrong.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from lib.source_media_review import review_source_media  # noqa: E402
from schemas.artifacts import validate_artifact  # noqa: E402

pytestmark = pytest.mark.skipif(
    shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None,
    reason="ffmpeg/ffprobe required to build the fixture clip",
)


@pytest.fixture
def clip_with_audio(tmp_path) -> Path:
    """A 4s 320x240 25fps clip with a real AAC stereo track."""
    out = tmp_path / "fixture.mp4"
    subprocess.run(
        [
            "ffmpeg", "-v", "error", "-y",
            "-f", "lavfi", "-i", "testsrc=size=320x240:rate=25:duration=4",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=4",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-ac", "2", "-ar", "48000",
            str(out),
        ],
        check=True,
    )
    return out


def test_video_probe_records_resolution_and_audio(clip_with_audio):
    art = review_source_media([clip_with_audio], {})
    validate_artifact("source_media_review", art)

    entry = art["files"][0]
    probe = entry["technical_probe"]

    assert probe["resolution"] == "320x240"
    assert probe["fps"] == 25.0
    assert probe["audio_codec"] == "aac"
    assert probe["channels"] == 2

    # The summary is what downstream stages read; "unknown"/"without audio"
    # here is what silently dropped a source audio track.
    assert "320x240" in entry["content_summary"]
    assert "with audio" in entry["content_summary"]
    assert "without audio" not in entry["content_summary"]


def test_video_probe_samples_real_frames(clip_with_audio):
    art = review_source_media([clip_with_audio], {})
    frames = art["files"][0]["representative_frames"]

    assert frames, "no frames sampled — the sampler call or its result key is wrong"
    for frame in frames:
        assert Path(frame).exists(), f"sampler reported a frame that is not on disk: {frame}"


def test_audio_track_marks_clip_usable_as_source_audio(clip_with_audio):
    art = review_source_media([clip_with_audio], {})
    assert "source audio" in art["files"][0]["usable_for"]
