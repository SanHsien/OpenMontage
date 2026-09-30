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

## 2026-09-15：分支清理（僅留 main）、Dependabot 依賴合併、PR #656–#660 審查與 main 分支保護

**決策**：
1. **單一 main 分支治理與本機／遠端分支清理**：
   - 遠端分支清理：Dependabot 自動開啟之 3 個 PR 經評估：
     - PR #1 (`fast-uri` 3.1.5 -> 3.1.7 高風險安全性修正 GHSA-qw65-cvwx-89v3)：引進並 squash-merge，刪除遠端分支。
     - PR #3 (`browserslist` 4.28.4 -> 4.28.9 與 `baseline-browser-mapping` 2.11.23)：引進並 squash-merge，刪除遠端分支。
     - PR #2 (`baseline-browser-mapping` 2.10.40 -> 2.11.23)：已完全被 PR #3 包含，自動關閉並刪除遠端分支。
   - 本機分支清理：刪除所有歷史暫存 `pr-*` 分支（pr-640 至 pr-655）。
   - 結果：本機與遠端 `origin` 均僅保留唯一的 `main` 分支。
2. **main 分支保護設定（比照其他維護 repo）**：
   - 透過 GitHub API 對 `SanHsien/OpenMontage` 的 `main` 分支設定分支保護規則：
     - `required_status_checks`：設定 Windows CI 矩陣（Python 3.10–3.14）、CodeQL 安全掃描（Python security scan）與 Upstream check 為必要檢查項（strict: false）。
     - `allow_force_pushes`：false（禁止強制推送）。
     - `allow_deletions`：false（禁止刪除 main 分支）。
     - `enforce_admins`：false（允許管理員維護推送，符合「push 到 main 是我一直說的原則」）。
3. **上游 PR #656–#660 評估與引進**：
   - **PR #656**：`Fix BarChart value label precision`。上游針對 Issue #654 的修復，本 fork 先前已完成修復並同時支援小數控制，故標記已對齊。
   - **PR #657**：`Feature/gpt gateway`。空白 PR 說明、未經測試的草稿，予以拒絕。
   - **PR #658**：`TalkingHead: image overlay`。上游已關閉，略過。
   - **PR #659（引進並合併）**：`fix: read ComfyUI workflow files as UTF-8`。修復 Windows 環境下載入 ComfyUI 工作流 JSON 時因未指定 UTF-8 導致 cp950 解碼崩潰之重要跨平台 bug，並引入非 ASCII 測試。
   - **PR #660**：`feat(captions): shared phrase captions for subtitles.style "karaoke"`。卡拉 OK 歌詞渲染器功能擴充，先予暫緩（Defer）。
4. **基準線更新**：
   - `tools/upstream_baseline.json` 水位推進至 PR 660、Issue 654、日期 2026-09-15。

## 2026-09-30：上游 PR #661–#687、Issue #664 審查（無新 commit）

**決策**：上游 main 無新 commit（水位維持 `08e2151`）。19 筆 PR、1 筆 issue 已逐筆分流；未合併的開放 PR 一律暫緩，待上游合併後經 commit 軸抵達再評估（同 PR #655/#660 前例）。

| 項目 | 結論 | 理由 |
| --- | --- | --- |
| #661 #662 #663 | 暫緩 | 開放中，Remotion 元件 props/字型變更（+28～260 行），尚未合併；合併後與本 fork remotion-composer 比對 |
| #669 | 暫緩 | 開放中，playbook 契約測試與新 playbook |
| #672 | 暫緩 | 開放中，1 檔 8 行 runtime-selection 修正，尚未合併 |
| #673 | 不適用 | 新增 `/reel` 指令，上游工作流導向 |
| #679 | 暫緩（adoption pending） | 開放中，`final_review` 黑畫面檢查修正（+48/-3），明確 bug 但未合併且未於本機驗證 |
| #680 | 暫緩（adoption pending） | 開放中，piper_tts 在 venv 內尋找 binary（+39/-2），合併後採用 |
| #681 #682 | 暫緩 | 開放中，RTL 文字與字幕空白修正，尚未合併 |
| #683 #684 #687 | 暫緩 | 開放中，新 provider / 發佈器（+606～1272 行），不屬修正 |
| #685 | 暫緩 | 已關閉未合併的 hyperframes 鍵讀取修正（+105/-16），觸發條件：本 fork 使用 hyperframes playbook schema 時回看 |
| #666 | 不適用 | 已關閉；雲端設定下載 Piper 模型，本 fork 為純 Windows 維護線 |
| #667 | 不適用 | 開放中，POD 產品廣告 pipeline（+17.6k 行），非修正 |
| #674 #677 | 不適用 | 已關閉；巨量 vendor 更新（>700 檔） |
| #678 | 不適用 | 已關閉；素材/藝術檔（77 檔） |
| Issue #664 | 不適用 | 功能請求（新增 Magnific provider），非缺陷 |

**基準線**：`tools/upstream_baseline.json` 推進至 PR 687、Issue 664、日期 2026-09-30。Baseline 代表已審查，未代表已合併。
