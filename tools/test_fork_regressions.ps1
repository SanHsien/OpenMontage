[CmdletBinding()]
param()

# Product tests this fork added or changed. dev_check.ps1 only runs
# tools/tests, so without this step none of the fork's product fixes
# (Windows encoding, CJK subtitles, backlot path checks, music routing...)
# are exercised in CI. Add a test file here when a fork fix adds one.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $venvPython) {
    $pythonExe = $venvPython
} else {
    $pythonExe = (Get-Command python -ErrorAction Stop).Source
}

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$tests = @(
    "tests/backlot/test_server.py",
    "tests/contracts/test_comfyui_tools.py",
    "tests/contracts/test_hunyuan_cloud_video.py",
    "tests/contracts/test_phase0_contracts.py",
    "tests/contracts/test_remotion_local_fonts.py",
    "tests/lib/test_source_media_review_video_probe.py",
    "tests/tools/test_diagram_gen.py",
    "tests/tools/test_music_selector.py",
    "tests/tools/test_stock_provider_detection.py",
    "tests/tools/test_stock_source_adapters.py",
    "tests/tools/test_video_trimmer_concat.py",
    "tests/tools/test_video_trimmer_workspaces.py",
    "tests/tools/test_windows_cjk_followups.py"
)

$missing = @($tests | Where-Object { -not (Test-Path -LiteralPath $_) })
if ($missing.Count -gt 0) {
    throw "Listed fork regression tests are missing: $($missing -join ', ')"
}

Write-Host "==> Fork product regression tests ($($tests.Count) files)"
& $pythonExe -m pytest -q -p no:cacheprovider @tests
if ($LASTEXITCODE -ne 0) {
    throw "Fork regression tests failed with exit code $LASTEXITCODE"
}

Write-Host "FORK REGRESSION TESTS GREEN"
