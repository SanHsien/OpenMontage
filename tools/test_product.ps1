[CmdletBinding()]
param()

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

Write-Host "==> Run OpenMontage product verification suite (Windows)"

Write-Host "--> 1. Core modules syntax compilation"
& $pythonExe -m py_compile tools/base_tool.py tools/tool_registry.py tools/cost_tracker.py tools/analysis/composition_validator.py
if ($LASTEXITCODE -ne 0) {
    throw "Core module compilation failed with exit code $LASTEXITCODE"
}

Write-Host "--> 2. Tool registry discovery test"
& $pythonExe -c "from tools.tool_registry import registry; registry.discover(); print(f'Successfully discovered {len(registry._tools)} tools in registry')"
if ($LASTEXITCODE -ne 0) {
    throw "Tool registry discovery failed with exit code $LASTEXITCODE"
}

Write-Host "--> 3. Demo video listing test"
& $pythonExe render_demo.py --list
if ($LASTEXITCODE -ne 0) {
    throw "render_demo.py --list failed with exit code $LASTEXITCODE"
}

Write-Host "PRODUCT TESTS GREEN"