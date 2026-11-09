# Fork 維護說明

本 repo fork 自 [`calesthio/OpenMontage`](https://github.com/calesthio/OpenMontage)，
沿用 GNU Affero General Public License v3.0 (AGPL-3.0) 與完整 Git 歷史。

## 為什麼維護 fork

- 保留原作者持續更新的 12 條影片生產管線、視覺化故事板 Backlot、Remotion 整合與 700+ Agent 影視知識庫。
- 採 Windows-first 維護：Windows 11 + PowerShell 是主要開發、除錯與完整驗收環境。
- 公開入口維持繁體中文為主，英文鏡像放 `README.en.md`，簡體鏡像保留 `README_zh-CN.md`。
- 建立可重現的 Windows 開發 gate、純 Windows CI 工作流程，以及逐筆審查的上游追蹤（涵蓋 commit、PR 與 issue 水位）。
- 產品執行路徑以上游為準；本線不發佈未授權第三方套件或變更上游授權。

**回貢判準：修的是上游的 bug 就送回去；這裡獨創的文件／Windows 維護骨架留在這裡。**
回貢前必須在當次對話取得維護者明確同意；「fork」「建開發環境」「開 PR」都不是同意。

## 與上游的差異

| 項目 | 說明 |
|---|---|
| `README.md` | 繁中主檔；加入 fork 維護資訊與快速入口 |
| `README.en.md` | 英文鏡像；加入 fork 維護資訊 |
| `README_zh-CN.md` | 上游簡體中文說明文件保留 |
| `AGENTS.md` | 本 fork 的 AI 維護單一真相源（載明 Windows 原生規範） |
| `NOTICE.md` / `FORK.md` / `LICENSE` | 來源、授權與同步說明 |
| `tools/dev_check.ps1` | Windows 本機一鍵 gate（維護工具，不安裝重型依賴） |
| `tools/bootstrap_dev.ps1` | Windows 本機一鍵初始化與驗收（支援 `-All` 參數安裝產品依賴） |
| `tools/test_product.ps1` | Windows 原生產品測試執行腳本（驗證語法、註冊中心與 demo 清單） |
| `requirements.txt` / `requirements-dev.txt` | 產品與維護依賴清單（納入 ruff） |
| `.github/workflows/ci.yml` | 純 Windows 原生 CI (windows-latest Python 3.10–3.14 矩陣)：compile / ruff / 維護測試 / 連結檢查 |
| `.github/workflows/upstream-check.yml` | 每週對 `upstream/main` 做未審查 commit、PR、issue 水位檢查 |
| `.github/workflows/dependency-freshness.yml` | 每月依賴新鮮度檢查 |
| `.github/workflows/codeql.yml` | CodeQL 安全掃描工作流程 |
| `docs/DECISIONS.md`、`docs/UPSTREAM.md`、`docs/DEVELOPMENT.md` | fork 維護文件 |
| `REVIEW.md` | 全庫風險快照 |
| `tests/contracts/test_phase0_contracts.py` | 平台指令檔清單移除 `CLAUDE.md`（本 fork 只維護 `AGENTS.md`） |
| `README_pt-BR.md` / `README_es.md` / `README_zh-CN.md` | 上游語言版本；語言切換列與內文的「英文版」連結改指 `README.en.md`（上游指 `README.md`，在本 fork 是繁中主檔），並在切換列加入繁中 `README.md` |
| `README.en.md` | 上游 `README.md` 的鏡像；語言切換列、Node 版本與 pip／certifi 升級說明、早期使用者公告同步自上游（2026-11-10） |
| `tools/minicut_cli.py` | `INSTALL_INSTRUCTIONS` 不採用上游的 `curl … \| bash` 安裝指令，改為請維護者自行下載、讀過再執行；其餘照上游 |
| `tests/contracts/test_bar_chart_format_contract.py` | 上游釘死 `formatValue` 這個實作；本 fork 保留自己的 `decimals` 屬性做法（見 `docs/DECISIONS.md` 2026-09-13），測試改為斷言同一性質（資料標籤不套用一位小數的軸刻度格式） |
| `tests/contracts/test_skill_reference_paths.py` | 引用路徑檢查先去掉 `:行號`／`:起-訖` 後綴（本 fork 的 `docs/DECISIONS.md` 用 `path:line` 引用程式位置） |
| `tools/audio/piper_tts.py`、`tools/video/video_trimmer.py`、`scripts/backlot_simulate_run.py`、`tools/subtitle/subtitle_gen.py`、`remotion-composer/src/components/charts/BarChart.tsx` | 與上游同步時衝突、保留 fork 先前修法並併入上游新增部分的檔案；逐檔理由見 `docs/DECISIONS.md` 2026-11-10 |
| `tools/video/hyperframes_compose.py` | 衝突時取上游，保留 fork 先前加的 `encoding="utf-8"`、`errors="replace"` 子行程解碼補丁（Windows ANSI 碼頁） |
| `.github/dependency-deferrals.json` | 依賴新鮮度的「看過、這次不升」清單（含 `certifi`、`pythainlp`） |

核心模組在 `tools/`、流水線定義在 `pipeline_defs/`、技能庫在 `skills/`、Remotion 合成在 `remotion-composer/`，以上游為準。

## 分支與 remote

- `origin/main`：SanHsien 維護線，也是唯一長期分支。
- 日常修改在本機跑 gate 後直接推 `origin/main`。
- `upstream/main`：calesthio 原始專案，只追蹤、不推送。
- Dependabot 或外部 fork 的變更走 PR，讀 diff 並通過 CI 後再合併。

不要 `git push upstream`。同步方式見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

上游更新英文 `README.en.md` 或其他文件時，把新內容併進本 fork 對應檔案。

## 換一台電腦怎麼開發

```powershell
git clone https://github.com/SanHsien/OpenMontage.git
cd OpenMontage
# `gh repo clone` 已會加上 `upstream` remote；若沒有：
# git remote add upstream https://github.com/calesthio/OpenMontage.git
pwsh -NoProfile -File tools\bootstrap_dev.ps1
```

要實際使用管線生成影片與啟動 Backlot 故事板，見 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。