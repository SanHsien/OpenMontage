# AGENTS.md

給 Codex、Claude Code、Cursor、Antigravity 與其他自動化代理在本專案工作時的指引。產品與使用方式先讀 [`README.md`](README.md)；開發與驗收細節見 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。

## 專案定位

這是 [`calesthio/OpenMontage`](https://github.com/calesthio/OpenMontage) 的 GNU AGPLv3 fork。
核心價值是 12 條影片生產管線、視覺化故事板 Backlot、Remotion 高清合成、本機離線生成（Ollama、ComfyUI、Piper TTS）與 700+ Agent 技能檔案。

`origin` 是 `SanHsien/OpenMontage`（預設分支 `main`），`upstream` 是原作者 repo（預設分支 `main`）。
保留上游作者、AGPL-3.0 與產品程式。本 fork 的維護差異記在 [`FORK.md`](FORK.md) 與 [`docs/DECISIONS.md`](docs/DECISIONS.md)。

主要開發與完整驗收環境是 **Windows 11 + PowerShell**。本 fork 為純 Windows 維護線，所有測試與工作流程均在 Windows 原生環境執行。

## 硬性邊界

- 不提交使用者輸入影片、音訊素材、專有文件、API key、token、私鑰或 `.env`。
- 不推送到 `upstream`。上游同步先跑 `python tools/check_upstream_updates.py`，逐筆審查後再 merge / cherry-pick；不盲目覆蓋 fork 文件與 Windows gate。
- 不要把維護 gate 改成完整產品依賴安裝。維護環境（`requirements-dev.txt`）僅安裝 pytest、ruff 與必要依賴。
- 不把 fork 包裝成原創產品，不移除上游作者或官方連結。

## 技術與資料流

- 核心工具：`tools/`（工具註冊中心、成本追蹤、各類音訊/視訊/字幕模組）。
- 故事板：`backlot/`（FastAPI + WebSocket 視覺化分鏡伺服器）。
- 流水線定義：`pipeline_defs/`。
- 合成引擎：`remotion-composer/`（React + TypeScript + Remotion）。
- 技能與範本：`skills/`。
- 維護工具：`tools/dev_check.ps1`、`tools/bootstrap_dev.ps1`、`tools/test_product.ps1`。
- 維護契約測試：`tools/tests/`（獨立於產品測試目錄）。

## 開發原則

- 一般變更直接推 `origin/main`，不開功能分支、不開維護 PR。只有在需要他人審查、或改動風險高到值得先讓 CI 在 PR 上跑一輪時，才退回 **branch → PR → CI → merge**。
- 修 bug 先補可重現失敗測試，再做最小修正。
- 不為了套格式而大改上游程式；Ruff 只閘維護工具的 E9（語法）與 F（pyflakes）。
- 使用繁體中文回覆；使用者文件以繁中為主，公開入口同步維護 `README.en.md`。
- 提交訊息用 Conventional Commit。Dependabot 或外部 fork 的變更走 PR，讀 diff 並通過 CI 後再合併。
- `REVIEW.md` 是風險快照，不是每個一般 bug 的流水帳。
- 不 force-push `main`，不刪 `upstream` remote。

## 上游處理

1. `git fetch upstream main`
2. `python tools/check_upstream_updates.py --strict`
3. 逐筆判斷是否與繁中 README、Windows gate、發佈閘門或測試衝突。
4. 可同步的提交用 merge；只需要部分修正時 cherry-pick 或最小重做。
5. 跑 `pwsh -NoProfile -File tools\dev_check.ps1`
6. 採用／略過寫進 `docs/DECISIONS.md`，驗證後才推進 `tools/upstream_baseline.json`

Baseline 代表「已審查」，不代表「全部已合併」。

## 依賴新鮮度

每月的 `Dependency freshness` workflow 跑 `tools/check_dependency_freshness.py`，比對宣告與 PyPI 現行版。

紅燈只有兩種正當出口，兩種都要留下理由：

- **維持宣告**：在宣告那一行加 `# freshness-hold: <理由>`。
- **已延後**：在 `.github/dependency-deferrals.json` 加一筆
  `{"deferredLatest": "<當時看到的版本>", "reason": "<為什麼這次不升>"}`。

不要用調高宣告下限讓報告變綠。