# 維護決策

## 2026-09-12：建立 Windows-first 維護型 fork

**決定**：fork `calesthio/OpenMontage`，保留 GNU Affero General Public License v3.0 (AGPL-3.0) 與完整歷史。本線預設分支用 `main`。本線聚焦繁中文件、Windows 開發 gate、Windows CI，以及逐筆審查的上游追蹤。

**理由**：`OpenMontage` 是一套擁有 57.7K+ Star 的開源智能製片系統，支援 12 條影片生產流水線、Remotion 高清合成、Backlot 故事板與本機離線生成。本 fork 補足 Windows 11 原生開發／驗收骨架、繁體中文維護入口，以及可審計的上游追蹤機制。

**限制**：

- 不把 fork 包裝成原創專案，不移除原作者 calesthio 與官方連結。
- 不發佈未授權套件取代官方管道。
- 維護 gate 不預設安裝重型套件。
- 上游更新必須逐筆審查。

## 2026-09-12：依賴新鮮度追蹤

**決定**：`tools/check_dependency_freshness.py` 納管 `requirements-dev.txt`、`requirements.txt` 與 `requirements-gpu.txt`。

**理由**：本 repo 之產品依賴包含 FastAPI、Pydantic、Remotion 整合套件，維護依賴包含 pytest 與 ruff，納入每月新鮮度檢查以確保相容性。

## 2026-09-12：上游檢查涵蓋 Commit、PR 與 Issue 三面向

**決定**：`check_upstream_updates.py` 以 `--state all` 收集上游 PR 與 Issue，並追蹤 Commit SHA。`gh` 失敗時 fail closed（exit 2）。

**理由**：未合併即關閉的 PR 與待處理的 Issue 同樣可能揭露重要缺陷或需求。排程報告必須確保「未檢查」與「沒有新變更」截然分明。

## 2026-09-12：日常直接推 main

**決定**：日常維護修改在本機跑 `tools\dev_check.ps1` 後直接推 `origin/main`。Dependabot 與外部貢獻仍走 PR，合併前讀 diff。

**理由**：對齊 SanHsien 體系其他維護 fork 的治理規範。

## 2026-09-12：上游分支、PR 與 Issue 首次盤點結論

**決定**：
1. **上游分支清理**：刪除 GitHub fork 遠端上 27 個非 main 分支，維持 `origin` 僅有單一維護主線 `main`。
2. **上游 PR 與 Issue 水位鎖定**：
   - 審查起點 Commit SHA: `08e2151fa02de28a5d6a312b3d575692bf147ad7`（短 SHA `08e2151`，2026-09-06）
   - PR 水位: `649`
   - Issue 水位: `649`
3. **基準文件建立**：建立 `tools/upstream_baseline.json` 鎖定上述水位。

**理由**：
- 確立乾淨的審查基準線，增量檢查未來僅需處理大於 `#649` 的新項目或 `08e2151` 之後的新 Commit。

## 2026-09-12：上游未合併分支、PR 引進與缺陷修復

**決定**：
1. **上游分支審查**：經逐項 diff 比對，`upstream/fix/backlot-ui-layout` 所含之 `no-cache` middleware、直式 9:16 video 樣式與媒體欄排版改動，在上游 `main` 分支中早已透過其他提交合併，已無遺漏。
2. **上游 PR 引進**：
   - 引進 PR #640（`diagram_gen` 精確回報 Mermaid CLI 可用性並在 Preflight 拋出警示）。
   - 引進 PR #641（`source_media_review` 徹底修復影片技術探針被音訊覆蓋、抽樣缺少 `strategy` 及 key 錯誤之嚴重缺陷）。
   - 引進 PR #642（`video_trimmer` concat 模式改用輸入 seek、支援 `codec` 轉碼、修正 `list_path` 潛在 `UnboundLocalError`、增加解碼幀檢驗防範產生 videoless 純音訊檔案）。
   - 引進 PR #649（Remotion 增加 `lib/fonts.ts` 支援 CJK / 繁中與非拉丁字型動態注入；修復 `backlot_simulate_run.py` 遺漏 proposal 階段門禁前置檢查例外）。
   - 引進 PR #650（Remotion `CaptionOverlay` 單字間距保留與深色主題 `KPIGrid`、`ComparisonCard` 樣式對比度修復）。
3. **Windows 11 原生缺陷修復**：
   - 修復 `tools/video/hunyuan_video.py` 遺漏 `from typing import Any`（F821 未定義變數）。
   - 修復 `tools/video/hyperframes_compose.py` 與 `tools/video/video_trimmer.py` subprocess 在繁中 Windows 預設 ANSI/cp950 下 reader thread 的 `UnicodeDecodeError`，全面改為 `encoding="utf-8", errors="replace"`。
   - 更新 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md` 引用 `AGENT_GUIDE.md`。

## 2026-09-12：防範第三方假冒二進位安裝檔安全政策（Issue #626）

**決定**：在 `SECURITY.md` 明確宣告 OpenMontage 目前為純 Python / Node.js 原始碼發布，官方從未提供任何編譯好的 `.exe` / `.msi` 安裝包；防範網路上假冒的釣魚惡意木馬。

## 2026-09-12：標籤管理政策（只保留最新 tag）

**決定**：
1. 確保 `origin` 與本機僅保留單一最新維護標籤 `v0.1.0-sanhsien.1`。
2. 日後若有新版本釋出，自動清理或覆蓋舊 tag，確保 `origin` 永遠只維持最新唯一 tag。

## 2026-09-13：上游全面審查（Commits、分支、PR #644–#655、Issue #654）

**決策**：
1. **上游 main 分支與 commit 水位**：
   - 上游最新 commit 為 `08e2151fa02de28a5d6a312b3d575692bf147ad7`，本 fork 已完整包含至此 SHA，無新 commit。
2. **上游遠端分支全面審查（共 27 條）**：
   - 25 條分支已完全合併至 `upstream/main`（涵蓋 `feat/*`, `codex/*`, `fix/*` 等）。
   - 2 條未合併分支經評估：
     - `upstream/docs/readme-add-alexandria-remove-abyss`：僅修改 Star History 圖表與排版，無功能價值，略過。
     - `upstream/fix/backlot-ui-layout`：經比對其修復（no-cache 與 portrait video player），已在上游 main 相關檔案（`backlot/server.py`, `backlot/ui/board.css`, `backlot/ui/board.js`）完全實現，無殘留修復。
3. **上游 Pull Requests 評估與引進**：
   - **PR #644（引進並合併）**：`Add music_selector, the missing music capability selector`。補足音樂能力缺乏 selector 的架構空缺，跨 `music_library`（本地免費）、`music_search`（免 key 庫存搜索）、`music_generation`（付費 API）三層能力，提供免消耗的 `plan` 試探與低成本優先的 `acquire` 取得功能。
   - **PR #646（評估並拒絕）**：`update render demo`。僅刪除 `render_demo.py` 第一行 docstring 開頭，屬於無效／意外 commit，予以拒絕。
   - **PR #647（引進並合併）**：`Prevent invalid CostTracker state transitions`。修復 CostTracker 生命週期狀態機漏洞（已完成項目不可退款、未保留項目不可調和／退款），並補足單元測試。
   - **PR #648（評估並拒絕）**：`feat: add Diana series film pipeline`。屬特定使用者的 43 部童書故事影片生成腳本，高達 11,000+ 行非核心腳本，且上游已關閉，不予引進。
   - **PR #651（引進並合併）**：`Fix Pexels and Pixabay provider preflight detection`。修復環境變數空白字串識別、加強 `.env` 覆蓋邏輯，並確保庫存提供者相依性正確宣告與檢測。
   - **PR #652（引進並合併）**：`fix: propagate archive source transport errors`。讓 Archive.org 與 Wikimedia 傳輸錯誤向上拋出給 corpus_builder，不再吞掉錯誤偽裝為空結果。
   - **PR #653（引進並合併）**：`Fix Pond5 provider contract`。要求 `POND5_API_KEY`、使用 Bearer 驗證、傳播傳輸錯誤並移除無效的 HTML scraper 偽 fallback。與 PR #652 合併後，徹底清空 `tests/tools/test_stock_source_adapters.py` 中長期存在的 `_STILL_SWALLOWS_TRANSPORT_ERRORS` 已知缺陷清單。
   - **PR #655（評估並暫緩 / Defer）**：`fix(security): gate .env loading behind an allow-list`。該 PR 正處於密集迭代中（Round 10、16 個 commits），引入破壞性的全域白名單阻擋機制及外部 Strix 安全掃描 CI 依賴，且與已引進的 PR #651 存在程式碼衝突，暫緩引進，待上游決定合併或穩定後再行評估。
4. **上游 Issue #654 修復（評估並修復）**：
   - **Issue #654**：`BarChart value labels misstate non-integer data`。`formatNumber` 針對浮點數使用 `.toFixed(1)` 截斷，導致 `0.15` 被顯示為 `0.1`、`1.33` 被顯示為 `1.3`。
   - 修復方案：更新 `remotion-composer/src/components/charts/BarChart.tsx` 與 `LineChart.tsx` 中的 `formatNumber`，保留最多兩位有效小數並去除尾隨零（如 `0.15`、`0.69`、`1.33` 均精確顯示），同時為 `BarChartProps` 與 `LineChartProps` 擴充可選 `decimals` 屬性。
5. **基準線水位推進**：
   - `tools/upstream_baseline.json` 水位推進至 PR 655、Issue 654、日期 2026-09-13。
