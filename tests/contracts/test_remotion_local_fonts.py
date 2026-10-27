"""remotion-composer/src/lib/fonts.ts must emit @font-face rules Chromium accepts.

The renderer is headless Chromium, which skips any src entry whose format()
hint it does not recognise. The test runs the real TypeScript under Node
(type stripping is built in from Node 23.6) instead of matching source text.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FONTS_TS = REPO_ROOT / "remotion-composer" / "src" / "lib" / "fonts.ts"


def _font_face_css(font: dict) -> str:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not on PATH")
    script = (
        "const m = await import(process.argv[1]);"
        "process.stdout.write(m.localFontFaceCss(JSON.parse(process.argv[2])));"
    )
    proc = subprocess.run(
        [node, "--input-type=module", "-e", script, FONTS_TS.as_uri(), json.dumps(font)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    if proc.returncode != 0 and "Unknown file extension" in proc.stderr:
        pytest.skip("this Node cannot load .ts files without a loader")
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


def test_source_list_uses_css_format_names_not_file_extensions():
    css = _font_face_css(
        {"family": "Noto Sans TC", "src": ["fonts/a.woff2", "fonts/b.woff", "fonts/c.ttf", "fonts/d.otf"]}
    )

    assert "url('fonts/a.woff2') format('woff2')" in css
    assert "url('fonts/b.woff') format('woff')" in css
    assert "url('fonts/c.ttf') format('truetype')" in css
    assert "url('fonts/d.otf') format('opentype')" in css


def test_unknown_extension_gets_no_format_hint():
    css = _font_face_css({"family": "X", "src": ["fonts/x.bin", "fonts/noext"]})

    assert "url('fonts/x.bin')," in css or "url('fonts/x.bin');" in css
    assert "format('bin')" not in css
    assert "format('fonts/noext')" not in css


def test_single_source_keeps_its_declared_format():
    css = _font_face_css({"family": "X", "src": "fonts/x.otf", "format": "opentype"})

    assert "url('fonts/x.otf') format('opentype')" in css
