"""bootstrap_dev.ps1 must fail when the gate it runs at the end fails.

Runs the real script in a scratch copy of the repo layout: the venv python is
Git for Windows' true.exe (exits 0 for any arguments, so nothing is
installed) and tools/dev_check.ps1 is a stub that exits 1.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
GIT_USR_BIN = Path(r"C:\Program Files\Git\usr\bin")


def test_bootstrap_fails_when_the_gate_fails(tmp_path: Path) -> None:
    pwsh = shutil.which("pwsh")
    true_exe = GIT_USR_BIN / "true.exe"
    if pwsh is None or not true_exe.is_file():
        pytest.skip("needs pwsh and Git for Windows' true.exe")

    (tmp_path / "tools").mkdir()
    shutil.copy2(TOOLS / "bootstrap_dev.ps1", tmp_path / "tools" / "bootstrap_dev.ps1")
    (tmp_path / "tools" / "dev_check.ps1").write_text("exit 1\n", encoding="utf-8")
    (tmp_path / "requirements-dev.txt").write_text("", encoding="utf-8")
    scripts = tmp_path / ".venv" / "Scripts"
    scripts.mkdir(parents=True)
    shutil.copy2(true_exe, scripts / "python.exe")
    for dll in GIT_USR_BIN.glob("msys-2.0.dll"):
        shutil.copy2(dll, scripts / dll.name)

    proc = subprocess.run(
        [pwsh, "-NoProfile", "-NonInteractive", "-File", str(tmp_path / "tools" / "bootstrap_dev.ps1")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
        timeout=120,
    )

    assert proc.returncode != 0, proc.stdout + proc.stderr
