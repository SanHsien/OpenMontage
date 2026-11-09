# 維護決策

## 2026-11-10：四筆依賴新版重新審視，保留下限並續延

**範圍**：`Dependency freshness` workflow（run 42673439625，main c5d7ac3）回報 `ruff`、`google-genai`、`openai`、`fastapi` 為 `REVIEW UPDATE`。

**成因**：2026-11-05 的 6e1863d 之所以綠，是因為四筆都有 `deferredLatest` 延後（ruff 0.17.3、google-genai 2.34.0、openai 3.46.0、fastapi 0.162.0）。延後項依設計在 PyPI 超過審視版本時自動失效；後來 PyPI 出 ruff 0.17.4、google-genai 3.0.0、openai 3.48.0、fastapi 0.162.2，延後失效而轉紅。不是檢查被改動。

| 套件 | 宣告下限 | 延後版本 → 本次 PyPI 版本 | 續延理由 |
| --- | --- | --- | --- |
| ruff | 0.9 | 0.17.3 → 0.17.4 | 維護 gate（ruff E9,F，範圍為 fork 工具）在 0.17.4 通過；產品樹不受 gate 檢查，升級依政策第 3 點獨立處理 |
| google-genai | 1.0.0 | 2.34.0 → 3.0.0 | 離線 Google provider 測試在 3.0.0 通過；Lyria／Veo／Gemini Omni 雲端呼叫仍待另行授權的實測，且上游下限未變 |
| openai | 2.44.0 | 3.46.0 → 3.48.0 | 離線 provider 測試在 3.48.0 通過；TTS／圖片／Sora 雲端呼叫未實測，上游下限未變 |
| fastapi | 0.110 | 0.162.0 → 0.162.2 | 上游下限未變；維護 gate 在 0.162.2 通過 |

**決定**：四筆均採指定版本延後，`reviewed: 2026-11-10`、`revisit: 2026-12-10`。不升下限：政策明定升下限不是消紅燈的出口，下限是相容承諾；上游 requirements 與本 fork 相同（僅 requirements-dev.txt 的 ruff 為本 fork 加入），沒有安全修正或 fork 需要的新 API 作為升級理由。google-genai 3、openai 3 為 major 版本，未讀完整 changelog 逐一核對呼叫點，故不宣稱相容，只記錄離線測試結果。

**驗證**：`.venv` 內實裝 google-genai 3.0.0、openai 3.48.0、fastapi 0.162.2、ruff 0.17.4；`pip check` 無衝突；`tests/tools/test_google_imagen_gemini_backend.py`、`test_google_vertex_backends.py`、`test_provider_refresh.py` 與 `tests/contracts/test_phase3_contracts.py` 共 129 passed。這些是離線 mock 證據，不是雲端實測。

**Python 版本與重審重點**：PyPI 上 google-genai 自 2.34.0 起 `requires_python >=3.11`，3.0.0 亦同；CI matrix 仍含 3.10，因下限 `>=1.0.0` 無上限，3.10 會自動解析到 2.x，不會壞。3.11 以上的新安裝會直接拿到 3.0.0（Developer API 預設 `v1`、HTTP client 改 `httpx2`、改用 OS trust store），這是既有的執行期風險、非本次引入；2026-12-10 重審時優先實測 Lyria、Veo、Gemini Omni 的雲端呼叫。

**重評**：到期、PyPI 超過本次版本，或取得雲端實測條件／上游調整下限時重評。

## 2026-11-05：八筆依賴新版重新審視，保留下限並續延

**範圍**：本機 `check_dependency_freshness.py --strict` 回報八筆 `REVIEW UPDATE`；工作樹起點 `c98eec01bf68f4e1f16be987c40ff86b1d15d5f0`，沒有前次未提交改動。

| 套件 | 宣告下限 | 原延後版本 → 本次 PyPI 版本 | 續延理由 |
| --- | --- | --- | --- |
| pydantic | 2.0 | 2.14.1 → 2.14.3 | 保留上游相容下限；新版驗證與 schema 行為尚未完成 Python 3.10–3.14 矩陣驗收 |
| google-auth | 2.0 | 2.62.0 → 2.62.1 | Google TTS／Vertex AI 服務帳戶驗證缺少具憑證的實測 |
| google-genai | 1.0.0 | 2.33.0 → 2.34.0 | Lyria／Veo／Gemini Omni 的雲端呼叫尚未完成另行授權的實測 |
| openai | 2.44.0 | 3.40.0 → 3.46.0 | 保留 Videos API 下限；離線 mock 不足以證明新版 TTS／圖片／影片服務呼叫相容 |
| websockets | 14.0 | 17.3 → 17.4 | 舊版 17.3 證據不能代替 17.4 的 Eleven v4 Turbo／即時傳輸驗收 |
| torch | 2.0 | 2.14.1 → 2.15.0 | 尚未驗證 Windows CUDA、GPU 推論與三件組的相容組合 |
| torchaudio | 2.0 | 2.11.0 → 2.11.1 | 音訊擴充需與 torch／Windows CUDA 成組驗證，不能各取最新版本推論相容 |
| torchvision | 0.15 | 0.29.1 → 0.29.2 | 尚缺 torch／CUDA 與 basicsr face_restore／upscale 實測；沿用上游 #875 的重評條件 |

**決定**：八筆均採指定版本延後（c），更新 `deferredLatest`、`reviewed: 2026-11-05`、`revisit: 2026-12-05` 與個別理由。不變更 requirements 下限、lock、產品程式或 workflow；續延不是宣稱新版已通過完整產品相容驗收，也不限制安裝器在現有範圍內選新版。

**參考**：[Pydantic 2.14.3](https://github.com/pydantic/pydantic/releases/tag/v2.14.3)、[Gen AI SDK 2.34.0](https://github.com/googleapis/python-genai/releases/tag/v2.34.0)、[OpenAI SDK 3.46.0](https://github.com/openai/openai-python/releases/tag/v3.46.0)、[websockets 相容政策與變更紀錄](https://websockets.readthedocs.io/en/stable/project/changelog.html)、[PyTorch 版本配套](https://docs.pytorch.org/get-started/previous-versions/)。google-auth 的對應 GitHub release 頁回 404，版本以本機 checker 的 PyPI 結果為準；不據此宣稱已讀到該版 release notes。

**重評**：沿用 ROADMAP「重評依賴延後紀錄」；到期、PyPI 超過本次版本或具備所需服務／GPU 驗收條件時重評。遠端 workflow 另檢查開放的 Dependabot PR；本次 `gh pr list --repo SanHsien/OpenMontage --state open --author app/dependabot --json number,title,url` 因無權讀取 GitHub CLI 設定而失敗，不宣稱遠端 workflow 已綠。

**驗證**：工作樹內新建 `.venv`，依 `requirements-dev.txt` 安裝（包含產品 requirements）；實裝 pydantic 2.14.3、google-auth 2.62.1、google-genai 2.34.0、openai 3.46.0、websockets 17.4，未安裝 GPU 三件組。`pip check` exit 0；新鮮度 strict 檢查由 exit 1（八筆 REVIEW UPDATE）轉為 exit 0；`tools/dev_check.ps1` exit 0（32 passed、16 份文件 0 斷鏈）；`tools/test_fork_regressions.ps1` exit 0（341 passed、8 skipped）；`tools/test_product.ps1` exit 0（PRODUCT TESTS GREEN）。首次維護 gate 因共用 pytest 暫存目錄權限失敗（25 passed、7 errors）；首次 fork 回歸也出現暫存錯誤並中止，將子行程 TEMP／TMP 指向工作樹 `scratch/` 後完成重跑。這些是本機離線 gate 證據，不是全量 pytest、Python 矩陣、雲端或 GPU 實測。原始輸出保留於未納管的 `scratch/`。

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
   - 引進 PR #649（Remotion 增加 `remotion-composer/src/lib/fonts.ts` 支援 CJK / 繁中與非拉丁字型動態注入；修復 `backlot_simulate_run.py` 遺漏 proposal 階段門禁前置檢查例外）。
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


## 2026-10-24：修補 Dependabot 警示 #8 與 `remotion-composer` 鎖檔的 audit 結果

**決定**：只動 `remotion-composer/package.json` 與 `remotion-composer/package-lock.json`，沒有改任何產品程式碼。鎖檔由 `npm update ... --package-lock-only --ignore-scripts` 與 `npm install --package-lock-only --ignore-scripts` 重新產生。

| 套件 | 舊 → 新 | 對應 |
| --- | --- | --- |
| `postcss-selector-parser` | 7.1.4 → 7.1.7 | Dependabot #8（medium，GHSA-rj75-hqrm-r3gf）；Dependabot PR #4 只升到 7.1.6，保持開啟 |
| `source-map-js` | 1.2.1 → 1.2.2 | `npm audit` high（GHSA-68fv-2mgg-jv7q），無 Dependabot 警示 |
| `fast-uri` | 3.1.7 → 3.1.9 | `npm audit` moderate（五則 GHSA），在 `^3.1.7` 範圍內 |
| `zod` | 4.3.6 → 4.6.7 | `npm audit` high（GHSA-mrhx-c7xc-m3w5），以 `overrides` 強制 |

**`zod` 為什麼用 override**：`zod` 只由 `@remotion/studio` 與 `@remotion/media` 以精確版本 `4.3.6` 相依；Remotion 最新版 4.0.538 也只升到 4.5.4，仍在受影響範圍（`< 4.6.6`），所以沒有可升的修補版 Remotion。Remotion 沒有把 `zod` 打包進自己的 dist（`@remotion/studio` 在執行時載入專案解析到的 `zod`），因此 override 真的改變執行時的 `zod`，不只是讓掃描器看不到。專案的 `src/` 沒有任何 `zod` 引用。
**代價**：Remotion 會在每次 `remotion` 指令印出「zod: installed 4.6.7, required 4.3.6」的版本不一致警告，宣稱可能造成 zod 型別相關功能異常。若日後在 Remotion Studio 的 schema 編輯器遇到問題，先移除這行 override 驗證；Remotion 釋出支援 `zod >= 4.6.6` 的版本後，刪掉 override。

**驗證**：`npm ci --ignore-scripts` 後 `npm audit` 為 0 個弱點（升級前 9 個：2 moderate、7 high）。lock diff 只有四個套件版本變動，無新增／移除套件、無新 install script、`resolved` 皆為官方 registry。在暫存副本（不入版控）手動補上 `CaptionOverlay.tsx` 缺少的 `>` 之後，`tsc --noEmit` 無錯誤，`remotion bundle src/index.tsx` 成功，只多上述警告。
**既有問題（未修，非本次範圍）**：`remotion-composer/src/components/CaptionOverlay.tsx` 第 126 行的 `<span style={{...}}` 少了結尾 `>`，造成 `tsc` 11 個語法錯誤與 `remotion bundle` 失敗；問題從 v1.0.0 初始提交就存在，與依賴無關。
**未涵蓋**：根目錄 `requirements*.txt` 都只有下限（`>=`）沒有釘版，沒有鎖檔可供 `pip-audit` 檢查，因此 Python 端沒有做弱點掃描。


## 2026-10-24：修正 `CaptionOverlay.tsx` 未關閉的 `<span>` 開始標籤

**發現**：`remotion-composer/src/components/CaptionOverlay.tsx` 第 126 行 `<span style={{...}}` 少了結尾 `>`，從 v1.0.0 初始提交就存在。`npx tsc --noEmit` 回報 11 個語法錯誤（第 127～145 行，全部是同一個缺漏造成的連鎖），`npx remotion bundle src/index.tsx` 在 esbuild 階段失敗（`127:17: ERROR: Expected "..." but found "w"`）。
**修正**：只在第 126 行 `}}` 後補上 `>`，沒有改動其他邏輯或 JSX 結構。
**驗證**：`npm ci --ignore-scripts` 安裝後，`npx tsc --noEmit` 為 0 錯誤；`npx remotion bundle src/index.tsx` 成功，只有既有的 zod 版本不一致警告（見上一條）。
**後續建議（未實作）**：目前 CI 沒有任何 job 對 `remotion-composer` 跑 `tsc`，這類語法錯誤才會在 main 上存在這麼久；建議另開變更，在 CI 加一個 `npm ci --ignore-scripts && npx tsc --noEmit` 的 job。


## 2026-10-24：上游審查（commit 08e2151→e01dbf4、PR #689–#848、Issue #694–#819）

**範圍**：上游 `main` 自審查基準 `08e2151` 前進到 `e01dbf433f46eeb91d39bf905e194162921019a3`（48 個 commit；相對基準 167 檔 +21,768／-1,005）。135 筆 PR（`--state all`：33 已合併、15 關閉未合併、87 開放）與 18 筆 Issue 全數逐項分類，水位推進到 PR #848、Issue #819。fork 與上游沒有共同祖先，所以以 `08e2151` 為 merge-base，用 `git merge-tree --write-tree --merge-base=08e2151 origin/main upstream/main` 做三方合併，再手解 4 個衝突；沒有對上游留言、開 PR 或 push。

**方法**：已合併 PR 經 commit 抵達，歸併到其 commit；未合併即關閉的 PR 先判斷是否「新增資料／巨量」型投稿，再掃 diff 的 Windows／CJK 關鍵字（`win32`、`cp950`、`gbk`、`encoding=`、CJK 字元等），命中才讀 diff 並到 fork 實測缺陷是否仍在；開放中的 PR 以「PR 刪除的程式行在合併後的 fork 是否仍存在」當缺陷證據（逐筆比例見附錄 A）。

### 一、Commit（48）：採用 45（含 2 個合併提交）、已在 fork 1、僅略過 `README.md` 部分 2

| 組 | Commit（PR） | 結論 | 證據與處置 |
| --- | --- | --- | --- |
| provider 更新 | `b75ac8a` `0fcd7fd` `4f13650`（#698）、`e01dbf4`（#845）、`cf22f15`（#840）、`0f191f9`（#839） | 採用 | #698 為 45 檔 +7,999、#845 為 46 檔 +6,221，多為新 provider 工具、`tools/provider_contracts/*.json`、`docs/provider-*.md` 與技能；`requirements.txt` 新增 `websockets>=14.0`，見第四節 |
| 資產快取 | `dec5094`（#379）、`907ab3b` `37de71d` `9041ee7`（#787 #789 #793）、`841eee6`（#794）、`45ee719`（#796） | 採用 | 新 `lib/asset_cache.py`（+563）、`tools/base_tool.py`（+249）；與 fork 在 `base_tool.py` 的空白環境變數修正自動合併，無衝突 |
| 工作區隔離／路徑安全 | `d4f4e71` `5469a4e` `8aabbc9` `cf9f03c` `d7f3a93`（#713 #719 #788 #711 #717） | 採用 | `5469a4e` 與 fork 的 `video_trimmer.py` 衝突，見第三節 |
| 音訊 | `a903d77` `cc21a7b` `a960ff9` `d380b69` `4fafc6b` `aae521c`（#761 #790 #791 #752 #267 #805） | 採用 | `audio_mixer.py`、`audio_enhance.py`、`elevenlabs_tts.py`、`google_tts.py`、`gemini_tts.py` |
| 影片 | `3ef87b7` `e754761` `008a3a4` `314d5af` `39f7434` `e45f5b1`（#795 #798 #759 #592 #606 #697）、`46a0c94` `a3768a0` `9327439`（#527 ComfyUI WAN 2.2） | 採用 | fork 在 `tests/contracts/test_comfyui_tools.py` 新增的測試與上游自動合併 |
| 契約與狀態 | `b137959` `1555403`（#702 #704 checkpoint）、`cdc3a78` `0e0fbce`（#760 #813 schema）、`9468d72` `adcfce5`（#706 #709） | 採用 | `lib/checkpoint.py`＋2 個 schema |
| Remotion | `fdcb861`（#613）、`c9f5f53`（#820 RTL）、`7157ce1`（#663 字型內建） | 採用 | `fdcb861` 與 fork 衝突，見第三節；`src/lib/localFonts.ts` 與 fork 的 `src/lib/fonts.ts`（PR #649 引進）檔名與匯出皆不同，`Explainer.tsx` 同時 import 兩者，`tsc` 與 `remotion bundle` 通過 |
| 其他 | `29c6466`（#573）、`90409ef`（#776 非 ASCII 斷詞，對 CJK 有利）、`f4ac4a7`（#753 BMTS-Lite）、`3b92389`（#832 backlot Host 標頭） | 採用 | `29c6466` 衝突見第三節；`backlot/server.py` 的 fork 路徑檢查與上游 Host 檢查自動合併 |
| 已在 fork | `7ad9fac`（#647 CostTracker 狀態轉換） | 無需動作 | fork 於 2026-09-13 已引進同一修正，合併後 `tools/cost_tracker.py` 與上游逐位元組相同 |
| 贊助商 | `f11bf79` `c806645` | 略過 `README.md`；`README.en.md` 與資產採用 | fork 的 `README.md` 是自寫的繁中主檔、沒有 Sponsors 區，該 diff 無法套用；`README.en.md` 是上游英文鏡像，同步移除 Sponsors 區與導覽連結，並刪除只被它引用的 `assets/sponsors/atlas-cloud.png`、`bloome.png` |

### 二、PR（135）：採用 37、略過 25、延後 73

- **採用 37**：33 筆已合併 PR 經 commit 抵達（#697 #698 #702 #704 #706 #709 #711 #713 #717 #719 #752 #753 #759 #760 #761 #776 #787 #788 #789 #790 #791 #793 #794 #795 #796 #798 #805 #813 #820 #832 #839 #840 #845）；#842 移植；#696 #725 #828 部分移植（見第三節）。
- **略過 25**：
  - 已被合併 PR 或 fork 既有修正取代：#695 #714（→#613／#697）、#727 #757（→#805）、#740（→#839）、#758（→#820）、#749（fork 的 `scripts/backlot_simulate_run.py:97-175` 已寫入 proposal 階段）。
  - 非修正或與本線方向不合：#692（macOS 安裝）、#803 #817（贊助商、部署按鈕宣傳）、#755 #775（已關閉的新功能）、#810 #811（已關閉；diff 無 Windows／CJK 命中）、#821 #822 #823 #824 #825 #827（同作者 2026-10-19 同日關閉的功能包）。
  - 巨量或無關投稿，不收：#804（+72,895／430 檔）、#837（+101,677／650 檔）、#838、#830、#808。
- **延後 73**，觸發條件一律是「上游合併後經 commit 抵達再比對，或 fork 實際命中該情境」：
  - 新功能／新 provider／素材（25 筆）：#699 #744 #746 #747 #748 #751 #762 #764 #765 #766 #767 #768 #770 #774 #777 #782 #783 #784 #801 #818 #829 #834 #836 #847 #848。
  - 缺陷修正，缺陷代碼仍在 fork（39 筆）：#691 #700 #701 #703 #705 #707 #708 #710 #712 #716 #718 #720 #721 #726 #737 #738 #739 #741 #742 #743 #750 #754 #769 #772 #773 #779 #780 #781 #785 #786 #792 #797 #806 #807 #814 #815 #816 #844，另 #800（已關閉）。例：#708（FFconcat 檔名含單引號）對應 `silence_cutter.py:339,449`、`video_compose.py:643`、`video_stitch.py:603`、`video_trimmer.py` 的 `f.write(f"file '{safe_path}'\n")`；#773／#814／#800 對應 `audio_mixer.py:271` 對 ffprobe `N/A` 直接 `float()`。
  - 文件小修（7 筆）：#689 #690 #763 #809 #833 #835 #843。#809 對應 Issue #799，fork 仍有 12 行引用不存在的 `docs/*-best-practices.md`。
  - 其他：#826（已關閉，含一個真缺陷：巢狀 `projects/<series>/<topic>` 的 atelier 暫存目錄互撞；觸發=fork 使用巢狀專案目錄跑 atelier）、#831（TLS 信任庫版本下限；觸發=合併，或 CI 出現 TLS 錯誤）。

### 三、同步時的人工決定

| 項目 | 決定與證據 |
| --- | --- |
| `README.md` 衝突 | 保留 fork 版本（上游只刪 Sponsors 區） |
| `lib/source_media_review.py` 衝突（`29c6466`） | 探針保留 fork 直接以 ffprobe 讀取（`encoding="utf-8", errors="replace"`，PR #641 引進、`tests/lib/test_source_media_review_video_probe.py` 覆蓋），不採上游「先 audio_probe 再補 ffprobe」的二段式；取上游的 `frames` 解包成路徑字串，以及輸出目錄按檔名隔離（`.source_review_frames_<stem>`） |
| `tools/video/video_trimmer.py` 衝突（`5469a4e`） | 保留 fork 的 `-ss/-to` 置於 `-i` 之前、`codec` 參數、`_has_video_stream` 驗證（PR #642 引進），再採上游 `tempfile.TemporaryDirectory` 每次呼叫獨立工作區與擴大後的 `idempotency_key_fields`；fork 原本的 `.concat_tmp` 與 finally 清理移除（由 context manager 取代） |
| `CaptionOverlay.tsx` 衝突（`fdcb861` ＋ `c9f5f53`） | 整檔取上游版本。fork 的 NBSP 字距（PR #650）被上游「分隔符號放在 inline-block span 之外」取代；結果含 `>`（本日前一節修的缺漏不會重現），`tsc --noEmit` 0 錯誤、`remotion bundle` 成功 |
| 移植 #842 | `tools/audio/piper_tts.py`：`subprocess.run(..., input=text, text=True)` 沒有 encoding，Windows 非 UTF-8 碼頁會在送進 Piper 前就弄壞中文；加 `encoding="utf-8", errors="replace"`。上游 PR 尚未合併，所以移植的是做法而非 diff |
| 部分移植 #696 | `tools/video/video_compose.py` 4 處 `text=True` 缺 encoding（ffprobe／volumedetect 輸出在 cp950／GBK 主控台會讓 reader thread 丟 `UnicodeDecodeError`），補 `encoding="utf-8", errors="replace"`；fork 的 `hyperframes_compose.py` 早已如此。transcriber（PyAV 解碼）與 `full_mix` 響度兩段延後，觸發=上游合併或本機重現 |
| 部分移植 #725／#828 | `tools/subtitle/subtitle_gen.py` 新增 `_join_tokens`：兩個相鄰 CJK 字元之間不加空格（含 karaoke 的 `<b>` 標記），拉丁字之間與拉丁／CJK 交界仍加空格；韓文不算 CJK（用空格分詞）。依字數切 cue、以腳本取代 ASR 做字幕、Doubao 時間戳正規化延後，觸發=上游合併或要產繁中字幕片／接入 Doubao |
| 上一輪遺留 #679（已關閉未合併） | `video_compose.py` 的 `_run_final_review` 以「PNG 小於 2000 位元組」判黑畫面，實測 1280×720 純黑 PNG 為 4,349 位元組、1920×1080 為 8,651 位元組，檢查永遠不會觸發，上游 `main` 仍未修；改為平均亮度 `< 6.0`，兩個以 ffmpeg 產生黑／灰畫面的測試覆蓋 |
| 上一輪遺留 #680（已關閉未合併） | 延後：上游 diff 找 `sys.executable` 旁的無副檔名 `piper`，在 Windows（`Scripts\piper.exe`）不成立；觸發=未啟用 venv 時 `piper` 找不到 |
| 上一輪遺留 #685（已關閉未合併） | 延後：hyperframes 風格橋接讀鍵；觸發=fork 使用 hyperframes playbook schema |
| 上一輪遺留 #663（現已合併） | 採用，見第一節 Remotion 列。#681（RTL 文字）、#661 #662 #669 #672 #683 #684 #687 仍開放，維持延後；#682（字距）被 #613 取代 |

上面四項移植的測試都在 `tests/tools/test_windows_cjk_followups.py`。

### 四、依賴

- `requirements.txt` 新增 `websockets>=14.0`（`tools/audio/_realtime_session.py`）。`check_dependency_freshness.py --strict` 對它回報 REVIEW UPDATE（PyPI 現行 17.3），在 `.github/dependency-deferrals.json` 加一筆 `deferredLatest: 17.3`（2026-11-24 回看）：維持上游宣告的相容性下限 14.0，在 17.3 下跑過相關測試。不調高下限來消音。
- `remotion-composer/package.json`／`package-lock.json` 上游未動，`zod` 4.6.7 override 保留。

### 五、Dependabot 警示 #9（zod，high，GHSA-mrhx-c7xc-m3w5）：延後，不 dismiss

警示位於 `.agents/skills/remotion-to-hyperframes/assets/test-corpus/tier-3-data-driven/remotion-src/package.json`（`zod ^3.22.0`，修補版 4.6.6）。證據：

- 該目錄沒有 lockfile，也不在 CI 與測試之中；唯一用法是 `SKILL.md`／`README` 描述、由人手動執行的 `npm install && npm run render` 基線渲染。
- `Root.tsx`、`Stargazed.tsx` 只用 `z.object`／`z.array`／`z.string`／`z.number` 宣告靜態 props 形狀，並驗證寫死的 `defaultProps`，不處理任何外部輸入。
- 產品的 `remotion-composer` 用 zod 4.6.7（見 `remotion-composer/package.json` 的 override），這個 fixture 不被產品打包。
- 修補版 4.6.6 是 4.x：fixture 的 `z.object`／`z.array` 寫法在 4.x 大概可用，但沒有人實際重跑過基線渲染，不在未驗證時改動測試資料；Remotion 最新版本自身已相依 zod 4.x（見上方 override 說明），所以這份 `^3.22.0` 宣告本來就與最新 Remotion 不同調。

**重新評估的觸發條件**（任一成立）：fixture 被納入 CI；加了 lockfile；開始處理外部輸入；有人要重跑基線渲染時（屆時順手改成 `^4.6.6` 並實測）。

## 2026-10-26：修補 tier-3 Remotion corpus 的 zod Dependabot 警示 #9

**決定**：將 `.agents/skills/remotion-to-hyperframes/assets/test-corpus/tier-3-data-driven/remotion-src/package.json` 的直接相依由 `zod ^3.22.0` 改為精準安全版本 `zod 4.6.7`，並以局部 npm override 將 `@remotion/cli` 子樹的 zod 固定為 `4.6.7`；不新增 corpus lockfile。

**理由**：GitHub Advisory `GHSA-mrhx-c7xc-m3w5`（CVE-2023-54404）確認 `< 4.6.6` 皆受高風險記憶體耗盡弱點影響。這份 corpus 會由 eval 的基線 render 安裝及執行；原先的寬鬆範圍加上無 lockfile，無法可靠識別實際安裝版本。`4.6.7` 是首個修補版本 `4.6.6` 以上、且已由本 repo 的 `remotion-composer` 安全 override 使用的同一修補線。精準 pin 讓 corpus 安裝時可決定性地取得已驗證的安全版本，而不以提高下限或隱藏警示為目的。

**巢狀相依重新檢查**：直接 pin 後的隔離 `npm ls zod --all` 發現 `@remotion/cli 4.0.538` 仍帶有 6 個 `zod 4.5.4`（仍在受影響範圍）。eval 與 tier-3 README 都使用 npm，因此改以 `@remotion/cli` 的局部 override 覆蓋這條 Remotion 4.x 子樹，不影響任何其他 zod consumer。重裝後，6 個位置皆為 deduped 的 `zod 4.6.7`；隔離暫時 lockfile 的 `npm audit --omit=dev --json` 為 0 個弱點且沒有 zod 項目。

**相容性驗證**：在工作樹外的隔離副本以 `npm install --ignore-scripts --no-audit --no-fund --package-lock=false` 安裝 `zod 4.6.7` 與 corpus 同一組 Remotion/React 相依；補足 React 18 型別後，`npx --no-install tsc --noEmit` 成功。以原始 `stargazedSchema` 與 `Root.tsx` 的既有 `defaultProps` 驗證：合法預設 props 通過，將 `stats[0].value` 改成字串的非法 props 被拒絕。未啟動影片 render、外部圖像 API 或產出基線檔案。

**範圍**：保留現有離線測試與 corpus 結構；不新增大型 lockfile，也未對 CodeQL #22 進行 dismiss。

### 六、Issue（18）：採用 2、略過 3、延後 13

| 項目 | 結論 | 證據與觸發條件 |
| --- | --- | --- |
| #736 #819 | 採用 | 已由 #839（`0f191f9`）、#820（`c9f5f53`）修正並隨 commit 抵達 |
| #724 | 略過 | fork 的 `scripts/backlot_simulate_run.py:97-175` 已寫入 proposal 階段，PR #749 同題不需要 |
| #694 | 略過 | 使用請求，非缺陷 |
| #756 | 略過 | 報告 Windows＋Claude Code 的 Bash／PowerShell hooks 不相容；repo 不含 hook 設定（`git ls-files` 無 `.claude/settings*`），fork 的 Windows 啟動是 `tools/bootstrap_dev.ps1`＋`docs/DEVELOPMENT.md`。觸發=fork 新增 Claude Code hooks |
| #728 #730 #731 #732 #733 #734 #735 #771 | 延後 | 缺陷仍在 fork：`remotion-composer/src/TalkingHead.tsx:224`（`&& overlay.text`）、`CinematicRenderer.tsx` 無 overlays 處理、`tools/video/video_compose.py:1331`、`tools/video/video_selector.py:331,597`（`operation` 預設 `text_to_video`）、`tools/enhancement/color_grade.py:185-204`、`tools/audio/pixabay_music.py:104`（只有 timeout 重試）、`tools/audio/audio_mixer.py:271`；對應開放 PR #743 #750 #741 #742 #737 #738 #739／#772 #814／#773。觸發=對應 PR 合併，或維護者實際用到該路徑 |
| #722 #723 #729 #745 #799 | 延後 | #722 測試網路守門（`tests/conftest.py:46-99`，PR #781）；#723 `CostTracker(` 在 `tools/`、`lib/` 沒有任何產品程式碼實例化；#729 `schemas/artifacts/proposal_packet.schema.json:69` 要求 `render_runtime`，與 proposal director 技能矛盾，無對應 PR；#745 為功能（PR #746）；#799 見 #809。觸發=上游給出修法 |

### 七、驗證

Windows 11、Python 3.14.9，在乾淨的 venv（`requirements-dev.txt`）內，於獨立 worktree 執行；長指令放背景。

| 指令 | 結果 |
| --- | --- |
| `python -m pytest -v --ignore=tests/qa/test_08_end_to_end.py -rfE`（全量） | 2,265 passed、13 skipped、2 failed；2 筆失敗是 `tests/tools/test_video_trimmer_workspaces.py`（上游測試以 mock 取代 `run_command`，fork 的 concat 會用 ffprobe 驗證輸出而失敗），測試改為 stub `_has_video_stream` 後該檔與 fork 的 `test_video_trimmer_concat.py` 共 5 passed |
| `python -m pytest tests/tools/test_windows_cjk_followups.py tests/contracts/test_phase3_contracts.py tests/tools/test_subtitle_timestamps.py tests/tools/test_unicode_tokenizers.py` | 103 passed（exit 0） |
| `pwsh -NoProfile -File tools/dev_check.ps1` | exit 0（compile、ruff E9+F、`tools/tests` 32 passed、連結檢查 16 份 0 斷鏈） |
| `ruff check --select E9`（全 repo）／`--select F`（逐檔對比 `origin/main`） | E9 全過；變動檔案的 F 數量不增加，上游新增的 `realtime_audio.py`、`bria_image.py`、`bmts_lite.py` 各 1 筆（非 gate 範圍） |
| `python tools/check_dependency_freshness.py --strict` | 無 deferral 時 `websockets` 為 REVIEW UPDATE（exit 1）；加入 deferral 後 exit 0 |
| `remotion-composer`：`npm ci --ignore-scripts` | exit 0，`found 0 vulnerabilities` |
| `remotion-composer`：`npx tsc --noEmit` | exit 0 |
| `remotion-composer`：`npx remotion bundle src/index.tsx` | exit 0（含新的 woff2 字型 import） |
| `python tools/check_upstream_updates.py --strict`（水位推進後） | exit 0，三個面向皆「No new … above」；`tools/tests/test_fork_docs.py` 原先寫死舊的 `reviewed_through` SHA，水位一動必紅，改為只驗證 40 位十六進位格式 |

**排除**：`tests/qa/test_08_end_to_end.py` 在 import 階段就跑完整個端到端腳本（所有輸出階段皆 `[PASS]`），然後在清理暫存檔時因 Windows 檔案被占用 `PermissionError [WinError 32]` 使收集失敗；該檔上游未動，與本次變更無關，所以從全量排除。

**未驗證**：需要重型依賴或付費金鑰的 provider 實機呼叫（HeyGen、ElevenLabs realtime 等）只由 mock 測試覆蓋；`websockets` 17.3 只驗證到測試層級。

### 八、水位

`tools/upstream_baseline.json`：`reviewed_through` → `e01dbf433f46eeb91d39bf905e194162921019a3`、`reviewed_date` 2026-10-24、`reviewed_pr_through` 848、`reviewed_issue_through` 819（均已實際分類到）。Baseline 代表已審查，未代表已合併。

### 附錄 A：PR 逐筆分類（未合併者；已合併者見第一節）

「缺陷行」= PR 刪除的程式行在合併後 fork 仍存在的行數／總行數（僅非測試檔）；新增型 PR 為 0/0。

| PR | 狀態 | 規模 | 結論 | 缺陷行 | 標題與備註 |
| --- | --- | --- | --- | --- | --- |
| #689 | open | +5/-5 2檔 | 延後 | 5/5 | fix(motion-graphics): correct relative reference paths in ag；文件小修（#809 對應 Issue #799）；觸發=上游合併 |
| #690 | open | +5/-5 3檔 | 延後 | 5/5 | fix(skills): repair broken relative links；文件小修（#809 對應 Issue #799）；觸發=上游合併 |
| #691 | open | +24/-16 4檔 | 延後 | 10/10 | fix(paths): resolve default output and composer paths from t；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #692 | closed | +60/-0 1檔 | 略過 | 0/0 | Add double-click macOS installer script；已關閉；macOS 雙擊安裝，本線為純 Windows |
| #695 | open | +19/-6 3檔 | 略過 | 1/3 | fix(remotion): keep spaces between caption words; add captio；「字詞間空格」已由合併的 #613(fdcb861 Fragment 分隔)取代，fork 的 NBSP 作法已被上游版本取代；caption placement props 延後 |
| #696 | open | +896/-46 10檔 | 部分採用 | 26/37 | fix(tools): transcriber on newer PyAV, UTF-8 subprocess outp；只移植 UTF-8 解碼段(video_compose.py 4 處 text=True 缺 encoding，GBK/cp950 讀 ffmpeg/ffprobe 輸出會炸 reader thread)；transcriber PyAV 解碼(需 faster-whisper+新 PyAV 才能重現)與 full_mix 響度重寫(+896 行)延後，觸發=上游合併或本機重現 |
| #699 | open | +997/-17 6檔 | 延後 | 12/12 | feat(video): add dashscope_video provider for Wan 3.0；新功能；觸發=上游合併後比對 |
| #700 | open | +99/-2 2檔 | 延後 | 2/2 | fix(fal): preserve image format across resumable jobs；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #701 | open | +61/-4 2檔 | 延後 | 4/4 | fix(pacing): match TerminalScene frame rounding；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #703 | open | +118/-10 2檔 | 延後 | 9/9 | fix(frames): return only frames sampled by the current call；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #705 | open | +115/-4 3檔 | 延後 | 4/4 | fix(backlot): track concurrent scene generation by call；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #707 | open | +92/-6 2檔 | 延後 | 5/5 | fix(reframe): honor explicit dimensions at the same aspect r；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #708 | open | +83/-3 3檔 | 延後 | 3/3 | fix(media): escape apostrophes in FFconcat filenames；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #710 | open | +62/-2 2檔 | 延後 | 2/2 | fix(video_compose): preserve portrait display ratio when enc；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #712 | open | +46/-1 2檔 | 延後 | 1/1 | fix(captions): handle whitespace-only SRT separators；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #714 | open | +14/-4 2檔 | 略過 | 2/4 | fix(remotion): stage anime_scene images and fix caption spac；anime_scene 暫存已由合併的 #697(e45f5b1)、字距由 #613 取代 |
| #716 | open | +90/-3 2檔 | 延後 | 3/3 | fix(green-screen): validate and sanitize bg_color to prevent；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #718 | open | +30/-1 2檔 | 延後 | 0/0 | fix(subtitle): preserve literal backslashes in correction va；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #720 | open | +54/-2 2檔 | 延後 | 2/2 | fix(audio-energy): handle fractional video duration windows；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #721 | open | +64/-5 2檔 | 延後 | 5/5 | fix(subtitle): escape literal transcript text in WebVTT；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #725 | open | +689/-11 6檔 | 部分採用 | 4/9 | feat(subtitles): make CJK captions render, align, and break ；只移植缺陷1(subtitle_gen 以空格串接 CJK 單字，subtitle_gen.py 舊 L155/264/302)；缺陷2-5(依字數切 cue、改用腳本做字幕、compose 設定 wordSeparator、0.5s 最短 cue；+689 行)延後，觸發=上游合併或維護者要產繁中字幕片 |
| #726 | open | +175/-63 5檔 | 延後 | 32/34 | fix(remotion): make scene defaults frame-aware for vertical ；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #727 | open | +5/-1 1檔 | 略過 | 0/1 | fix(tts): keep the genai client alive for the duration of th；genai client 提前釋放問題已由合併的 #805(aae521c)修正；#757 的 Veo RAI 原因訊息為額外功能，延後 |
| #737 | open | +65/-2 2檔 | 延後 | 2/2 | fix(video_selector): infer image_to_video from a first-frame；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #738 | open | +194/-15 2檔 | 延後 | 9/9 | fix(color_grade): correct intensity blend direction, honour ；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #739 | open | +102/-3 2檔 | 延後 | 3/3 | fix(pixabay_music): retry 403/429/5xx with backoff；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #740 | open | +46/-2 2檔 | 略過 | 0/2 | fix(freesound_music): return each sound's license and author；已由合併的 #839(0f191f9)取代 |
| #741 | open | +27/-11 1檔 | 延後 | 7/7 | fix(explainer): keep chart scenes clear of the caption band；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #742 | open | +54/-5 2檔 | 延後 | 3/3 | fix(video_compose): use the playbook's chart_palette for cha；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #743 | open | +2/-2 1檔 | 延後 | 2/2 | fix(talking-head): render section_title when only a subtitle；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #744 | open | +152/-5 9檔 | 延後 | 3/4 | feat(captions): forward CaptionOverlay style props (captionP；新功能；觸發=上游合併後比對 |
| #746 | open | +230/-2 3檔 | 延後 | 2/2 | feat(image_selector): optional per-request hooks for referen；新功能；觸發=上游合併後比對 |
| #747 | open | +186/-2 3檔 | 延後 | 1/1 | feat(video_compose): optional Remotion canvas size and rende；新功能；觸發=上游合併後比對 |
| #748 | open | +150/-0 3檔 | 延後 | 0/0 | feat(skills): add commercial product video guidance；新功能；觸發=上游合併後比對 |
| #749 | open | +56/-2 2檔 | 略過 | 2/2 | fix(backlot): include proposal gate in simulation driver；fork 已含同等修正(scripts/backlot_simulate_run.py:97-175 寫入 proposal 階段) |
| #750 | open | +55/-9 3檔 | 延後 | 8/8 | Fail fast when CinematicRenderer receives overlays；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #751 | open | +1552/-0 11檔 | 延後 | 0/0 | Integrate BGM Montage reference-guided video editing；新功能；觸發=上游合併後比對 |
| #754 | open | +2/-1 1檔 | 延後 | 0/1 | fix(charts): keep BarChart value labels at the data's own pr；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #755 | closed | +221/-1 7檔 | 略過 | 1/1 | Feat/backlot uisfx sounds；已關閉未合併的新功能(backlot UI 音效 +221；short-drama pipeline +6403)，非缺陷 |
| #757 | open | +7/-2 2檔 | 略過 | 1/2 | fix: keep Gemini TTS client alive; surface Veo RAI filter re；genai client 提前釋放問題已由合併的 #805(aae521c)修正；#757 的 Veo RAI 原因訊息為額外功能，延後 |
| #758 | closed | +46/-8 5檔 | 略過 | 6/8 | Arabic support；已關閉；阿拉伯語/RTL 由合併的 #820(c9f5f53)處理 |
| #762 | open | +12370/-452 72檔 | 延後 | 0/0 | Fix/tutorial last frame hold；新功能；觸發=上游合併後比對 |
| #763 | open | +29/-22 3檔 | 延後 | 20/20 | docs(lyria): align skill with current model selection；文件小修（#809 對應 Issue #799）；觸發=上游合併 |
| #764 | open | +1380/-1 11檔 | 延後 | 1/1 | feat(tts): add Sarvam AI Bulbul provider for Indic narration；新功能；觸發=上游合併後比對 |
| #765 | open | +109/-16 4檔 | 延後 | 11/12 | feat(gemini-omni): accept a service-account key as a second ；新功能；觸發=上游合併後比對 |
| #766 | open | +158/-0 2檔 | 延後 | 0/0 | fix(fal_3d): download MTL and texture alongside Hunyuan OBJ ；新功能；觸發=上游合併後比對 |
| #767 | open | +874/-12 8檔 | 延後 | 10/10 | feat(graphics): add fal_rig humanoid auto-rigging tool via f；新功能；觸發=上游合併後比對 |
| #768 | open | +182/-3 2檔 | 延後 | 3/3 | feat(local_diffusion): support SDXL and other diffusers pipe；新功能；觸發=上游合併後比對 |
| #769 | open | +194/-7 5檔 | 延後 | 1/1 | fix(checkpoint): require approval before proposal completion；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #770 | open | +657/-0 7檔 | 延後 | 0/0 | feat(styles): add seven brand & motion style playbooks (VO +；新功能；觸發=上游合併後比對 |
| #772 | open | +152/-7 2檔 | 延後 | 6/6 | fix(pixabay_music): retry the search page once after a bot-p；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #773 | open | +51/-1 2檔 | 延後 | 1/1 | fix(audio): reject unusable ffprobe duration when fading out；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #774 | open | +430/-0 10檔 | 延後 | 0/0 | Feature/chatgpt mcp；新功能；觸發=上游合併後比對 |
| #775 | closed | +6403/-3 55檔 | 略過 | 0/0 | feat(short-drama): Scheme F pipeline, subgraph IR, and Drama；已關閉未合併的新功能(backlot UI 音效 +221；short-drama pipeline +6403)，非缺陷 |
| #777 | open | +655/-0 4檔 | 延後 | 0/0 | Add KIE AI multi-model gateway integration；新功能；觸發=上游合併後比對 |
| #779 | open | +110/-2 3檔 | 延後 | 2/2 | fix(stock_sources): restore Coverr and Mixkit search results；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #780 | open | +2/-1 2檔 | 延後 | 1/1 | fix(remotion): cap caption lingering and honor line breaks i；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #781 | open | +75/-0 2檔 | 延後 | 0/0 | fix(tests): close the loopback-proxy hole in the session net；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #782 | open | +871/-0 16檔 | 延後 | 0/0 | feat: add DreamAPI as a bring-your-own-key media provider；新功能；觸發=上游合併後比對 |
| #783 | open | +1414/-7 15檔 | 延後 | 7/7 | feat: add Deepgram TTS (Aura-2) and STT (Nova-3) providers；新功能；觸發=上游合併後比對 |
| #784 | open | +767/-6 8檔 | 延後 | 6/6 | feat: add gemini_stt provider (Gemini 3.5 Transcribe)；新功能；觸發=上游合併後比對 |
| #785 | open | +51/-1 2檔 | 延後 | 1/1 | fix(cache): reject oversized assets before evicting usable e；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #786 | open | +118/-2 4檔 | 延後 | 1/2 | fix(graphics): retain rendering controls in local image cach；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #792 | open | +62/-3 3檔 | 延後 | 1/1 | fix(audio): schedule every channel of delayed tracks；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #797 | open | +160/-8 2檔 | 延後 | 7/7 | fix(video): apply recorded dynamic crop commands；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #800 | closed | +87/-14 2檔 | 延後 | 6/6 | fix(audio_mixer): reject tracks with an unknown duration wit；已關閉；audio_mixer 對 ffprobe `N/A` 時長 float() 會丟裸 ValueError(缺陷代碼仍在 fork，6/6 行)；同題 #773/#814 開放中，觸發=其一合併或實際遇到 |
| #801 | open | +160/-3 3檔 | 延後 | 3/3 | Fix Mixkit stock adapter; add keyless mixkit_music tool; con；新功能；觸發=上游合併後比對 |
| #803 | closed | +2/-2 3檔 | 略過 | 0/2 | docs: replace Bloome sponsor with Renoise；贊助商/部署按鈕宣傳文字；README.md 為 fork 維護的繁中主檔，不收 |
| #804 | open | +72895/-7 430檔 | 略過 | 0/0 | Factory/business documentary pilot；巨量/非修正投稿(#804 +72,895/430 檔、#837 +101,677/650 檔、#838 店面原型、#830 repo 分析、#808 無關內容)，不收 |
| #806 | open | +57/-5 2檔 | 延後 | 5/5 | fix(audio): keep short music cue fades inside segment bounds；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #807 | open | +39/-2 2檔 | 延後 | 2/2 | fix(frames): keep scene-guided samples inside short shots；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #808 | open | +2507/-0 4檔 | 略過 | 0/0 | Огуоц；巨量/非修正投稿(#804 +72,895/430 檔、#837 +101,677/650 檔、#838 店面原型、#830 repo 分析、#808 無關內容)，不收 |
| #809 | open | +29/-24 17檔 | 延後 | 20/20 | fix(skills): remove references to files that aren't in the r；文件小修（#809 對應 Issue #799）；觸發=上游合併 |
| #810 | closed | +150/-0 2檔 | 略過 | 0/0 | feat(video): pass a job-scoped browser executable to Remotio；已關閉未合併；diff 無 Windows/CJK 命中(關鍵字掃描 0 筆)，屬瀏覽器路徑/錯誤摘要功能 |
| #811 | closed | +162/-2 2檔 | 略過 | 2/2 | fix(comfyui): summarize execution errors instead of dumping ；已關閉未合併；diff 無 Windows/CJK 命中(關鍵字掃描 0 筆)，屬瀏覽器路徑/錯誤摘要功能 |
| #814 | open | +47/-1 2檔 | 延後 | 1/1 | fix(audio): actionable error when a fade_out track has no pr；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #815 | open | +56/-7 5檔 | 延後 | 7/7 | fix(stock): process-stable source_id for ESA/NOAA/LOC adapte；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #816 | open | +50/-1 2檔 | 延後 | 1/1 | fix(slideshow-risk): do not count unspecified camera movemen；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #817 | open | +8/-2 1檔 | 略過 | 0/2 | docs: add RepoCloud one-click deploy button；贊助商/部署按鈕宣傳文字；README.md 為 fork 維護的繁中主檔，不收 |
| #818 | open | +573/-5 6檔 | 延後 | 4/4 | feat(publishers): add youtube_upload, a private/scheduled-on；新功能；觸發=上游合併後比對 |
| #821 | closed | +618/-115 5檔 | 略過 | 62/64 | fix(audio): keep audio intact when stitching and trimming mi；同作者 2026-10-19 同日關閉的 7 筆功能包(+190~1238 行)；#822 的 Piper 模型解析、#823 的環境變數路徑皆非 fork 實際遇到的問題 |
| #822 | closed | +459/-20 6檔 | 略過 | 18/18 | feat(tts): ElevenLabs pronunciation dictionaries and model g；同作者 2026-10-19 同日關閉的 7 筆功能包(+190~1238 行)；#822 的 Piper 模型解析、#823 的環境變數路徑皆非 fork 實際遇到的問題 |
| #823 | closed | +438/-53 16檔 | 略過 | 47/47 | feat(paths): configure config, env file, styles, pipelines a；同作者 2026-10-19 同日關閉的 7 筆功能包(+190~1238 行)；#822 的 Piper 模型解析、#823 的環境變數路徑皆非 fork 實際遇到的問題 |
| #824 | closed | +235/-8 10檔 | 略過 | 6/6 | feat(checkpoint): opt-in autonomous policy with automated ap；同作者 2026-10-19 同日關閉的 7 筆功能包(+190~1238 行)；#822 的 Piper 模型解析、#823 的環境變數路徑皆非 fork 實際遇到的問題 |
| #825 | closed | +1238/-39 16檔 | 略過 | 28/30 | feat(remotion): playbook-defined themes and fonts, component；同作者 2026-10-19 同日關閉的 7 筆功能包(+190~1238 行)；#822 的 Piper 模型解析、#823 的環境變數路徑皆非 fork 實際遇到的問題 |
| #826 | closed | +377/-20 8檔 | 延後 | 15/15 | fix(video_compose): collision-free atelier staging, pre-bund；已關閉；含一個真缺陷(巢狀 projects/<series>/<topic> 暫存目錄互撞)，觸發=fork 使用巢狀專案目錄跑 atelier |
| #827 | closed | +190/-15 3檔 | 略過 | 12/13 | feat(backlot): list projects grouped under subdirectories；同作者 2026-10-19 同日關閉的 7 筆功能包(+190~1238 行)；#822 的 Piper 模型解析、#823 的環境變數路徑皆非 fork 實際遇到的問題 |
| #828 | open | +168/-8 2檔 | 部分採用 | 2/7 | fix(subtitle_gen): accept Doubao timestamps and join Chinese；中文 token 去空格已移植(同 #725 缺陷1)；Doubao startTime/endTime 正規化延後(本 fork 無 Doubao 流程)，觸發=接入 Doubao TTS |
| #829 | open | +8/-0 1檔 | 延後 | 0/0 | feat(captions): background_color option for remotion_caption；新功能；觸發=上游合併後比對 |
| #830 | open | +2551/-19 26檔 | 略過 | 0/0 | Claude/openmontage repo analysis yw9pdf；巨量/非修正投稿(#804 +72,895/430 檔、#837 +101,677/650 檔、#838 店面原型、#830 repo 分析、#808 無關內容)，不收 |
| #831 | open | +56/-11 9檔 | 延後 | 7/10 | fix: require patched TLS trust stores after eMudhra incident；TLS 信任庫(certifi>=2026.10.19、pip>=26.2.2、Node 範圍)，開放中；fork 的 requirements/CI 為 Windows runner 自帶最新 certifi，觸發=合併或 CI 出現 TLS 錯誤 |
| #833 | open | +3/-1 2檔 | 延後 | 1/1 | docs: list documentary-montage and fix stale TTS tool path；文件小修（#809 對應 Issue #799）；觸發=上游合併 |
| #834 | open | +4425/-22 40檔 | 延後 | 0/0 | feat: add Seedance product scene workflow；新功能；觸發=上游合併後比對 |
| #835 | open | +8/-0 1檔 | 延後 | 0/0 | chore: ignore in-tree npm cache and pytest scratch dirs；文件小修（#809 對應 Issue #799）；觸發=上游合併 |
| #836 | open | +238/-1 5檔 | 延後 | 1/1 | feat(tts): add Audexum TTS provider tool；新功能；觸發=上游合併後比對 |
| #837 | open | +101677/-7 650檔 | 略過 | 0/0 | Kilo/mega 100；巨量/非修正投稿(#804 +72,895/430 檔、#837 +101,677/650 檔、#838 店面原型、#830 repo 分析、#808 無關內容)，不收 |
| #838 | open | +7536/-0 31檔 | 略過 | 0/0 | Build AO groupe storefront prototype；巨量/非修正投稿(#804 +72,895/430 檔、#837 +101,677/650 檔、#838 店面原型、#830 repo 分析、#808 無關內容)，不收 |
| #842 | open | +22/-0 2檔 | 採用(移植做法) | 0/0 | fix(piper_tts): send narration text to Piper as UTF-8；piper_tts.py:134 `text=True` 無 encoding，Windows 非 UTF-8 碼頁(cp950/cp936)會把中文/重音字弄壞；已加 encoding="utf-8"+測試 tests/tools/test_windows_cjk_followups.py |
| #843 | open | +0/-2 1檔 | 延後 | 1/1 | fix(core/remotion): remove reference to missing mori-no-seis；文件小修（#809 對應 Issue #799）；觸發=上游合併 |
| #844 | open | +122/-13 2檔 | 延後 | 10/12 | fix(hyperframes_compose): accept a warm npx cache when the r；缺陷修正；觸發=上游合併或 fork 命中該情境 |
| #847 | open | +1774/-41 9檔 | 延後 | 31/31 | feat(dashscope): add Qwen voice cloning and cloned-voice TTS；新功能；觸發=上游合併後比對 |
| #848 | open | +382/-15 4檔 | 延後 | 14/14 | feat(dashscope_image): add Qwen-Image 3.0 / 2.1 models；新功能；觸發=上游合併後比對 |

## 2026-10-28：上游審查（PR #849–#863、Issue #854–#856；commit 無新進）

**範圍**：上游 `main` 仍在 `e01dbf4`，沒有新 commit。`--state all` 列出 11 筆 PR（1 筆關閉未合併、10 筆開放、0 筆已合併）與 3 筆 Issue（皆開放），逐筆分類，水位推進到 PR #863、Issue #856。沒有對上游留言、開 PR 或 push。

**方法**：取每筆 PR **目前**的 head（下表）抓 diff。隱藏內容掃描（`\S\s{40,}\S`、`eval(`／`new Function(`／`globalThis[`／`atob(`／`fromCharCode`、超過 400 字元的新增行）：11 筆皆 0 命中，超長行只有 #849、#862 的 Markdown 段落。再掃新增行的 Windows／CJK 關鍵字，只有 #861 含 Windows 修正，其餘命中都是新程式本身寫 `encoding="utf-8"` 或內文的破折號。

| 項目 | 狀態／head | 規模 | 結論 | 證據與觸發條件 |
| --- | --- | --- | --- | --- |
| PR #849 | closed `b5aaee3c7b` | +36/-1 2 檔 | 略過 | 新增 `local-voice-cloning` 技能文件（從原始碼建置 OmniVoice GGUF）；不是缺陷修正，上游未收 |
| PR #850 | open `73e1b665eb` | +1389/-4 19 檔 | 延後 | YouTube／TikTok 上傳與排程自動發片，含新 workflow `autopilot-short.yml` 與平台 token 取得腳本；新功能。觸發=上游合併後比對 |
| PR #851 | open `d12aea976c` | +81/-31 5 檔 | 延後 | 文件中的管線／工具數量同步與 `.python-version`；文件小修。觸發=上游合併 |
| PR #852 | open `adf14b704b` | +2922/-16 11 檔 | 延後 | Kling O3 的 fal 影像／影片模式；新 provider。觸發=上游合併後比對 |
| PR #857 | open `fd2197b051` | +383/-0 2 檔 | 延後 | Openverse 圖庫來源；新功能。觸發=上游合併後比對 |
| PR #858 | open `4862c0ee83` | +19/-1 2 檔 | 延後 | `CinematicRenderer.tsx` 在 `playbackRate ≠ 1` 時不傳 `trimAfter`（對應 Issue #855）。fork 仍是舊寫法：`remotion-composer/src/CinematicRenderer.tsx:69-71` 無條件換算 `trimAfterSeconds`。上游 PR 的測試只比對原始碼字串，沒有實際渲染證據；本機沒有慢速片段可重現。觸發=上游合併，或 fork 實際用到 `playbackRate < 1` 的片段 |
| PR #859 | open `80331e9c69` | +25/-8 1 檔 | 延後 | `transcriber.py` 對新版 PyAV 去掉 `metadata_errors` 參數。fork 的 `tools/analysis/transcriber.py` 沒有這段相容處理，`requirements*.txt` 也沒有釘 `av`。不照抄的原因：做法是在執行期替換 `faster_whisper.audio.av.open` 這個全域屬性，同一行程內並行轉錄會互相覆蓋。同 #696 transcriber 段，觸發=上游合併或本機以新 PyAV 重現 |
| PR #860 | open `57454c778c` | +66/-0 4 檔 | 略過 | Dockerfile 與 Docker 文件；本線為 Windows 原生維護線（同 #692 macOS 安裝的處理） |
| PR #861 | open `01ef8d3036` | +50/-27 3 檔 | 部分採用 | **Piper 段採用做法**（`52ccaa6`）：fork 先前移植 #842 時只修父行程那端；`pip install piper-tts` 的 Piper 是讀 `sys.stdin` 的 Python 程式，子行程在 Windows 仍用 ANSI 碼頁解碼，中文會被弄壞。現在傳 `PYTHONIOENCODING=utf-8` 給子行程，測試用讀 stdin 的替身 Piper 實跑，修前失敗。**`HeroTitle.tsx` 段略過**：改成 `title.split(" ")` 後每個字詞是 `nowrap`，沒有空格的中文標題會變成一整段不能換行，直式畫面會溢出；fork 現行的逐字排列（`HeroTitle.tsx:41`）對中文可正常換行。`StatCard` 字級屬性是新功能，延後 |
| PR #862 | open `424a5ea4b9` | +225/-9 7 檔 | 延後 | 發布階段記錄「留言關鍵字」CTA；新功能。觸發=上游合併後比對 |
| PR #863 | open `504d9b205a` | +93/-0 2 檔 | 延後 | 兩份 demo props 素材。觸發=上游合併後比對 |
| #853 | 不存在 | — | 無需動作 | `gh api repos/calesthio/OpenMontage/issues/853` 回 404（已刪除），PR 與 Issue 清單都沒有它 |
| Issue #854 | open | — | 略過 | 第三方分析報告公告，不是缺陷 |
| Issue #855 | open | — | 延後 | 同 PR #858 |
| Issue #856 | open | — | 略過 | 使用提示詞，不是缺陷 |

**水位**：`tools/upstream_baseline.json` 的 `reviewed_pr_through` 848→863、`reviewed_issue_through` 819→856、`reviewed_date` 2026-10-28；`reviewed_through` 維持 `e01dbf4`（上游沒有新 commit）。

## 2026-10-28：fork 自加程式深度掃描

**範圍**：`git diff upstream/main HEAD` 中 fork 自己加或改的程式（67 檔、+3,828/-275），排除艦隊正本 `tools/check_upstream_updates.py`（只能改正本）與 lockfile。上游原有、fork 未動的程式不改。每個缺陷先寫修前會失敗的測試，一個缺陷一個 commit。

| 位置 | 輸入 → 錯誤結果 | 處理 |
| --- | --- | --- |
| `tools/audio/piper_tts.py` | 中文旁白經 `pip` 版 Piper → 子行程以 ANSI 碼頁讀 stdin，文字變成替代字元 | 修（`52ccaa6`），見上節 #861 |
| `backlot/server.py` `/media`、`/thumb` | `/media/film/../film-private/renders/secret.png` → 200；包含檢查是 `startswith(base_path)` 不含分隔符號，同前綴的兄弟專案被當成在專案內；改用 `normpath` 後也不再跟隨符號連結 | 修（`3ea6ae7`）：兩個路由共用 `_project_file()`，兩邊 `realpath`、前綴含分隔符號。符號連結測試在不能建連結的機器上略過 |
| `tools/audio/music_selector.py` 成本上限 | `max_cost_tier="free"`（不是合法值）→ 退回最高等級，直接呼叫付費生成 | 修（`7acb628`）：不認得的值回錯誤 |
| `tools/audio/music_selector.py` 音樂庫 | `library_dir` 指向有曲目的資料夾、預設資料夾是空的 → 跳過音樂庫去付費生成；`library_dir` 是空資料夾 → 回報「已取得」但 0 首曲目，不再試圖庫 | 修（`ae0464c`）：依 `library_dir` 判斷可用性，0 首曲目不算成功 |
| `tools/video/stock_sources/pond5_pd.py` | `POND5_API_KEY="   "` → 判為可用並送出空的 Bearer；結尾換行的金鑰把換行帶進標頭 | 修（`40aa0a1`），與 Pexels／Pixabay 一致去除空白 |
| `tools/check_links.py` | README 連到 `docs/decisions.md`（實際是 `DECISIONS.md`）→ Windows 上判為存在，GitHub 上是 404 | 修（`6594f0b`）：repo 內路徑逐段比對實際檔名大小寫 |
| `remotion-composer/src/lib/fonts.ts` | `src: ["fonts/x.ttf"]` → `format('ttf')`，Chromium 不認得這個提示而跳過字型，中文退回拉丁字型 | 修（`64ad793`）：副檔名對應 `truetype`／`opentype`／`woff`／`woff2`，其他不加提示；測試以 Node 實跑 `fonts.ts`，`tsc --noEmit` 通過 |
| `tools/bootstrap_dev.ps1` | gate 失敗 → 仍印「維護環境可用」並以 0 結束（PowerShell 不會因原生指令非 0 而中止） | 修（`0abaa5c`），`python -m venv` 一併檢查 |
| CI 覆蓋 | `ci.yml` 只跑 `dev_check.ps1`（`tools/tests`），fork 為自己的產品修正寫的測試在 CI 上一個都沒跑 | 補（`6875bfd`）：`tools/test_fork_regressions.ps1` 列出這些測試檔，CI 在 gate 後執行；清單上的檔案不見會直接失敗 |

**看過、不修**：

- `tools/check_dependency_freshness.py`：延後紀錄 `deferredLatest: "17.3"` 時，PyPI 出 `17.3.1` 仍算延後中。這是刻意的「依宣告精度比較」，既有測試（`9.1` 涵蓋 `9.1.0`）釘住這個語意，不改。
- `tools/video/hyperframes_compose.py`：`npm view` 結束碼 0 但沒有輸出時，fork 記成空版本，上游版本會判為錯誤。之後還有 `doctor` 實跑 CLI 確認可執行，不會誤判可用；只差在報告欄位，不修。
- `tools/video/video_trimmer.py`：`_has_video_stream` 要求超過 1 幀，只有 1 幀的片段會被拒。這是為了擋 PR #642 修的「每段只剩 1 幀」問題刻意設的門檻，保留。
- `tools/video/stock_sources/archive_org.py`、`wikimedia.py`：任一搜尋策略的網路錯誤會中止整個來源。這是 R-21（PR #652）刻意把錯誤傳給 `corpus_builder` 的設計。
- `tools/_kling/account.py`：快取鍵用 10 萬次 PBKDF2，每次查用量多花數十毫秒；為了消 CodeQL 警示（R-27），功能正確，不改。

**驗證**：Windows 11、Python 3.14.9、乾淨 venv（`requirements-dev.txt`）。`tools/dev_check.ps1` exit 0（`tools/tests` 32 passed、連結 16 份 0 斷鏈）；`tools/test_fork_regressions.ps1` 348 passed、1 skipped（符號連結）；`remotion-composer` `npm ci --ignore-scripts` 後 `npx tsc --noEmit` exit 0。

## 2026-10-28：Dependabot 不再對 remotion-to-hyperframes 測試語料開安全性更新

**現象**：2026-10-24 Dependabot 三次對 `.agents/skills/remotion-to-hyperframes/assets/test-corpus/tier-3-data-driven/remotion-src` 的 zod 安全性更新失敗（run `40088430924`、`40126278641`、`40141518030`，`update_files` exit 1）。`dependabot.yml` 原本沒有 npm entry，所以這些是預設設定下的安全性更新；語料有三份 `package.json`（tier-1、tier-2、tier-3），都沒有 lockfile。10-26 已把 tier-3 改成 `zod 4.6.7` 並關閉警示 #9（見上方 10-26 條），之後沒有新的失敗，但只要語料的任何依賴再出現公告，同樣會失敗。

**決定**：`.github/dependabot.yml` 新增一個只涵蓋語料的 npm entry：`directories: ["/.agents/skills/remotion-to-hyperframes/assets/test-corpus/*/remotion-src"]`、`open-pull-requests-limit: 0`、`ignore: [{dependency-name: "*"}]`。

- Dependabot 的安全性更新是每個 manifest 目錄各跑一個工作（run 名稱是「npm_and_yarn in /<目錄>」），套用的是指名那個目錄的 entry。所以 entry 要直接指到語料目錄；`directory: "/"` 只看根目錄，而根目錄沒有 `package.json`，碰不到語料，還會多一個找不到檔案的工作（初版就是這樣，審查時退回）。
- `ignore` 依 GitHub 文件同時套用到版本更新與安全性更新；`open-pull-requests-limit: 0` 關掉版本更新 PR。語料目錄有 `package.json`，不會有找不到檔案的失敗。
- `remotion-composer` 不在這個 entry 的目錄裡，維持原本的預設安全性更新（例如 PR #4）。
- 排除只影響 Dependabot 開 PR，**警示仍會列在 Dependabot alerts**。語料的處理方式維持 10-26 的做法：由人在隔離副本實測後修改，不 dismiss。

**理由**：語料是遷移技能的固定測試資料，沒有 lockfile、不在 CI，只供人手動跑基線渲染。Dependabot 對它的自動修補不能產出可驗證的 PR，只會留下失敗紀錄蓋過真的失敗。

**驗證**：設定生效後，語料目錄不應再出現 Dependabot PR。被 `ignore` 擋下的安全性更新可能在 run 或警示上記一筆「all versions ignored」之類的錯誤，這屬預期；若出現的是 `update_files` 之類的執行失敗，代表設定沒套上，記在這裡再改。

**重新評估的觸發條件**：語料加了 lockfile 或被納入 CI（那時應恢復自動修補），或上述驗證失敗。

## 2026-10-28：四筆依賴延後到期，以新版實測後續延

推送 `dependabot.yml` 觸發的 Dependency freshness（run `40641976720`）報四筆 REVIEW UPDATE：延後時看到的版本之後又出了新版，延後自動失效。

| 套件 | 宣告 | 原延後版本 | 現行版 |
|---|---|---|---|
| `pytest` | `>=8.0` | 9.1.1 | 9.2.0 |
| `pytest-asyncio` | `>=0.23` | 1.4.0 | 1.4.1 |
| `ruff` | `>=0.9` | 0.17.2 | 0.17.3 |
| `openai` | `>=2.44.0` | 3.37.0 | 3.40.0 |

**實測**：Windows 11、Python 3.14.9，工作樹內新建 `.venv`，`requirements.txt`＋`requirements-dev.txt` 並把這四個釘在現行版。`tools/dev_check.ps1` GREEN（ruff 0.17.3 檢查通過、`tools/tests` 32 passed）；`tools/test_fork_regressions.ps1` GREEN（348 passed、1 skipped）。

**決定**：宣告下限不動（都是上游的相容性下限），四筆 `deferredLatest` 更新為現行版、`reviewed` 2026-10-28、`revisit` 2026-11-28；理由欄沿用。PyPI 再出新版時會再次提醒。

**補充驗證**（接手後）：另一個乾淨 venv（Python 3.14.9），四個套件同樣是現行版，全量產品測試 `python -m pytest --ignore=tests/qa/test_08_end_to_end.py`（收集 2,291 個）exit 0，沒有失敗或錯誤。openai 的四個工具（`tools/audio/openai_tts.py`、`tools/graphics/image_gen.py`、`tools/graphics/openai_image.py`、`tools/video/sora_video.py`）只有 mock 測試覆蓋，沒有實機呼叫。

**workflow 觸發路徑**：`dependency-freshness.yml` 的 push `paths` 原本不含 `.github/dependency-deferrals.json`，續期推上去不會重跑檢查，紅燈要等下個月排程或手動觸發才會消失。已把這個檔案加進 `paths`。

## 2026-10-30：Windows CI 七項回歸測試略過原因確認

**範圍**：只調查略過原因並保存證據，不修改產品、測試或 CI 設定。最近一次 [CI run 40745301061](https://github.com/SanHsien/OpenMontage/actions/runs/40745301061) 對應 `050d55993c8c6c65c7b85aa3f687b13c359bc6c6`（本次工作樹起點），執行於 2026-10-28 UTC／2026-10-29 台北時間。Python 3.10、3.11、3.12、3.13、3.14 的 `Fork product regression tests` 步驟全部成功，皆為 `342 passed, 7 skipped`。

**確認方法**：原 CI 使用 `pytest -q`，沒有 `-rs`，所以沒有原因文字；不能把本機的符號連結略過直接當成 runner 原因。[Python 3.14 job 123017370355](https://github.com/SanHsien/OpenMontage/actions/runs/40745301061/job/123017370355) 的進度字元顯示：349 個測試中，第 276–278、336–337、348–349 個為 `s`，其餘為 `.`。使用相同的 13 檔清單，在本機僅從子行程 PATH 移除含 `ffmpeg.exe`／`ffprobe.exe` 的目錄，保留 Node，再以 `-rs` 和 JUnit XML 核對收集順序，七個位置完全一致：

- 第 276–278 個，`tests/lib/test_source_media_review_video_probe.py`：
  - `test_video_probe_records_resolution_and_audio`
  - `test_video_probe_samples_real_frames`
  - `test_audio_track_marks_clip_usable_as_source_audio`
  - 原因：`ffmpeg/ffprobe required to build the fixture clip`。檔案層的條件為任一工具不在 PATH，略過建立真實影音素材的三項測試。
- 第 336–337 個，`tests/tools/test_video_trimmer_concat.py`：
  - `test_concat_keeps_video_across_timed_segments`
  - `test_concat_reports_failure_instead_of_a_videoless_file`
  - 原因：`ffmpeg/ffprobe required to build the fixture clips`。同樣檢查任一工具不在 PATH，略過兩項真實串接測試。
- 第 348–349 個，`tests/tools/test_windows_cjk_followups.py`：
  - `test_final_review_flags_a_black_render`
  - `test_final_review_does_not_flag_a_non_black_render`
  - 原因：`ffmpeg not installed`。實際條件同時檢查 FFmpeg 與 ffprobe；文字本身不能證明只缺 FFmpeg。

**結論與限制**：CI 的七項略過由影音工具在 PATH 上不可用造成，不是符號連結權限，也不是缺少 Python 套件。這是依原 CI 的略過位置、同版本原始碼條件與受控重現交叉確認；原 runner 已結束，不能再探測它當時究竟少了哪一個執行檔，也不能把「不在 PATH」宣稱成「磁碟未安裝」。Node 字型測試沒有略過，缺少 Python 依賴會造成收集錯誤，不能解釋此次綠燈的七項略過。

**本機差異**：Windows、Python 3.14.10、Node 26.12.1、FFmpeg／ffprobe 9.0.2，專案內乾淨 `.venv` 安裝 `requirements-dev.txt`。本機建立符號連結實際回傳 `WinError 1314`（缺少權限），因此第 9 個 `tests/backlot/test_server.py::TestBacklotServerApi::test_media_rejects_symlink_out_of_project` 另有一項略過，原因為 `creating symlinks needs Developer Mode or admin on Windows`；CI 同一位置是 `.`，已執行通過。移除影音工具的本機完整清單結果為 `341 passed, 8 skipped`（上述七項＋本機權限一項），exit 0；正常 PATH 的結果另見下方驗證。

**重現指令**（僅暫改目前 PowerShell 行程的環境，結束後還原；不需卸載工具或改權限）：

```powershell
$savedPath = $env:PATH
$savedPytestOptions = $env:PYTEST_ADDOPTS
try {
    $env:PATH = ($env:PATH -split ';' | Where-Object {
        $_ -and -not ((Test-Path -LiteralPath (Join-Path $_ 'ffmpeg.exe')) -or
                     (Test-Path -LiteralPath (Join-Path $_ 'ffprobe.exe')))
    }) -join ';'
    .venv\Scripts\python.exe -c "import shutil; print({x: shutil.which(x) for x in ('ffmpeg', 'ffprobe', 'node')})"
    $env:PYTEST_ADDOPTS = '-rs'
    pwsh -NoProfile -File tools\test_fork_regressions.ps1
    if ($LASTEXITCODE -ne 0) { throw "Regression exit code: $LASTEXITCODE" }
} finally {
    $env:PATH = $savedPath
    $env:PYTEST_ADDOPTS = $savedPytestOptions
}
```

正常情境沿用 `PYTEST_ADDOPTS=-rs` 跑相同腳本，不變更 PATH。此項為調查與文件修正，沒有程式 bug 修正，故不製造先紅後綠的回歸測試；缺依賴造成的收集錯誤也不算回歸紅燈。

**正常環境驗證**：`PYTEST_ADDOPTS=-rs` 下，`pwsh -NoProfile -File tools/test_fork_regressions.ps1` exit 0，結尾 `348 passed, 1 skipped in 117.85s (0:01:57)`、`FORK REGRESSION TESTS GREEN`；七項影音測試全部通過，只略過符號連結測試。`pwsh -NoProfile -File tools/test_product.ps1` exit 0，找到 156 個工具，結尾 `PRODUCT TESTS GREEN`。本次 CI 摘要、位置比對、JUnit XML 與本機輸出保存在忽略目錄 `scratch/ci-skip-audit/`，不列入提交；上述 CI 連結與重現指令可獨立核對結論。

## 2026-11-02：上游審查（commit `e01dbf4`..`195eab2`、PR #865–#885、Issue #864／#880）

**範圍**：3 個新 commit（`53e34e6`、`454bb28`、`195eab2`）、18 筆 PR（2 筆已關閉未合併、1 筆已合併、15 筆開放）、2 筆 Issue（皆開放）。水位：commit `e01dbf4`→`195eab2`、PR 863→885、Issue 856→880。沒有對上游留言、開 PR 或 push。

**方法**：commit 以 `git diff e01dbf4 upstream/main` 取得後 `git apply -3`（3 檔，乾淨套用）；PR 取每筆**目前**的 head（下表）抓 diff。隱藏內容掃描（`\S\s{40,}\S`、`eval(`／`new Function(`／`globalThis`／`atob(`／`fromCharCode`、base64 長串、零寬與雙向控制字元、控制碼）：15 筆開放／已合併 PR 皆 0 命中，只有 #871 有 2 行超過 400 字元（Markdown 設計文件段落）。

### commit 軸（3 筆，全部採用）

- `53e34e6`（Merge commit from fork，GHSA-cg89-3297-mwhg；`tools/video/showcase_card.py` +138/-47、`tools/video/video_compose.py`、新增 `tests/tools/test_showcase_card_security.py` 283 行）、`454bb28`／`195eab2`（#867，把回歸測試改成斷言真正的 `force_style` 屬性）。缺陷：`title_color` 等值直接串進 FFmpeg filtergraph，可附加第二個 drawtext 讀任意本機檔案；`_build_subtitle_style` 的字幕樣式值同樣未過濾。**本 fork 已有的舊緩解**：套用前 `video_compose.py` 的 `_build_subtitle_style` 完全沒有 `_safe()`（與上游舊版相同），所以沒有衝突，上游新版直接取代。這是安全修正且為上游已合併的 commit，依「產品程式以上游為準」整批取用。驗證：`python -m pytest tests/tools/test_showcase_card_security.py` 24 passed。

### PR／Issue 軸

| 項目 | 狀態／head | 規模 | 結論 | 證據與觸發條件 |
| --- | --- | --- | --- | --- |
| PR #867 | merged `454bb286` | +58/-6 1 檔 | 已隨 commit 軸採用 | 見上 |
| PR #873 | open `8c327560` | +6/-6 2 檔 | **採用(移植做法)** | `tools/avatar/lip_sync.py:197-204` 與 `talking_head.py:201-211` 以 `cwd=wav2lip_dir`／`sadtalker_dir` 執行推論腳本，但 `--face`／`--audio`／`--source_image` 原樣傳入使用者給的相對路徑，子行程在模型目錄找不到檔案。已在入口對 `video_path`／`audio_path`／`image_path`／`output_path` 加 `.resolve()`，與上游 diff 相同（規模只有 6 行，沒有不照抄的部分）；新增 `tests/tools/test_avatar_relative_paths.py`（2 個測試，修前失敗、修後通過）。觸發=上游合併時以上游版本為準 |
| PR #865＋Issue #864 | open `147fab1b` | +156/-1 2 檔 | 延後 | `math_animate` 的靜態掃描只看 import 根與 dunder，`zipfile.os.system(...)` 可繞過（上游測試 7 項）。`MathAnimate._scan_scene_code` docstring 已寫明掃描「不保證安全」，且 `allow_unsafe_code` 是明確的逃生口，威脅模型是 Agent 自己寫的場景碼。PR 在 `_scan_scene_code` 前多加了一行重複的 `@staticmethod`（diff 內可見），品質待上游收斂。本 fork 沒有對外接受不可信場景碼的入口。觸發=上游合併，或本 fork 開放不可信輸入進 `math_animate`；屆時採上游版本 |
| PR #872 | open `3c6f6b12` | +27/-2 1 檔 | 延後 | 缺陷存在（`diagram_gen.py:188` 固定傳 `-w`，mermaid-cli 12 起改為 `--size`），只影響已升到 mermaid-cli 12 的環境。本機未安裝 mmdc，無法重現。觸發=上游合併，或本機升級 mermaid-cli 12 |
| PR #874 | open `750ef2e0` | +8/-0 1 檔 | 本 fork 已處理 | `scripts/backlot_simulate_run.py:97-` 已有 proposal 階段的 `cp("proposal", …)` 與完整 `proposal_packet`（fork 先前加的 80 行）；PR 的版本只是較簡單的同一件事。不採用 |
| PR #875 | open `0cc6fa1f` | +127/-17 5 檔 | 延後 | torchvision 新版移除 `functional_tensor`，`face_restore`／`upscale` 需補相容層（新增 `_basicsr_compat.py`，fork 沒有這檔，`tools/` 內也無 `functional_tensor` 引用）。需要 GPU 與 basicsr 實機驗證，本機無法重現。觸發=上游合併，或本機實際跑 face_restore |
| PR #876 | open `4d15bb04` | +257/-27 3 檔 | 延後 | HunyuanVideo 1.5／LTX-2／CogVideoX 的 I2V pipeline 對應（`tools/video/_shared.py:171-209` 目前各只有單一 `pipeline_class`）。需要 diffusers 與大模型權重驗證；本線沒有這些本機模型。觸發=上游合併，或本機啟用這三個模型的 I2V |
| PR #877 | open `b72e2d6c` | +102/-0 4 檔 | 略過 | 新增 Claude Code plugin 與 `.claude-plugin/marketplace.json`；本 fork 沒有 `.claude-plugin/` 或 `plugins/`（`ls` 皆不存在），是新發佈管道，不是缺陷修正 |
| PR #878 | open `94117fbe` | +20/-6 3 檔 | 延後 | Remotion 直式短片的字幕版面與尾端留白選項；新功能。觸發=上游合併後比對 |
| PR #879 | open `fc461b71` | +274/-5 3 檔 | 延後 | 泰文逐字卡拉 OK 字幕斷詞，新增 `requirements.txt` 依賴。非 CJK 專屬；與 #828 的中文處理不同路徑。觸發=上游合併，或本線出現泰文需求 |
| PR #881 | open `12da36ec` | +102/-6 3 檔 | 延後 | talking-head 技能文件的 `execute()` 範例修正與契約測試；文件小修。觸發=上游合併 |
| PR #882 | open `b2ee8da3` | +104/-1 2 檔 | 延後 | `VideoCompose.idempotency_key_fields = ["operation", "input_path", "edit_decisions"]`（`video_compose.py:228`）未含其他渲染輸入，快取可能誤命中；缺陷屬實但牽動快取語意，且與 #883 同一類，等上游一起定案。觸發=上游合併，或本機遇到換參數卻拿到舊輸出 |
| PR #883 | open `90703bd5` | +75/-1 2 檔 | 延後 | 同 #882，對象是 `remotion_caption_burn`（`idempotency_key_fields = ["input_path", "segments", "srt_path"]`，`:147`）。同上 |
| PR #884 | open `2be2633d` | +166/-3 2 檔 | 延後 | `provider_routing.py` 對自由格式 model 欄位的明確指定；路由行為變更。觸發=上游合併 |
| PR #871 | open `26bead7a` | +522/-53 20 檔 | 延後 | 雙輸出編輯風格匯出與資料解說風格，含 `ci.yml` 與 `lib/` 變更；新功能且動到 CI，不收。觸發=上游合併後比對 |
| PR #869 | closed `7973b5c1` | +95/-1 5 檔 | 略過 | Docker／whisperx 文件，上游未收；本線為 Windows 原生維護線（同 #860） |
| PR #870 | closed `5f13966a` | +455/-91 13 檔 | 略過 | 「checkpoint existing provider and composer work」，非修正投稿，上游未收 |
| PR #885 | open `4a440fea` | +115/-0 3 檔 | 延後 | 新增於審查途中（`--strict` 重跑才出現）；`comfyui_video` 改用下載後的 ffprobe 結果回報寬高／fps／影格數（對應 Issue #880）。缺陷屬實：`comfyui_video.py:577` 缺輸入時以 WAN 預設 832／640 回報，與自訂 workflow 實際輸出不符；動到共用 `_shared.py` 的 `probe_output`，本機沒有 ComfyUI 可重現。diff 掃描 0 命中。觸發=上游合併，或本機使用自訂 ComfyUI workflow |
| Issue #864 | open | — | 延後 | 同 PR #865 |
| Issue #880 | open | — | 延後 | 同 PR #885（`comfyui_video` 對成功渲染的自訂 workflow 回傳預設媒體 metadata） |

**水位**：`tools/upstream_baseline.json` 的 `reviewed_through` `e01dbf4`→`195eab2`（完整 SHA）、`reviewed_pr_through` 863→885、`reviewed_issue_through` 856→880、`reviewed_date` 2026-11-02。

## 2026-11-10：上游審查（commit `195eab2`..`fecb9a1`、PR #886–#925、Issue #886–#917）

**範圍**：上游 `main` 自 `195eab2` 前進到 `fecb9a1e3cc23ef84de30b272059457a427f16f8`；`--strict` 列出 224 個 commit（第一親代鏈 70 筆：67 筆 PR 合併、3 筆直接提交 `d21f5d4`、`63d1087`〔#897〕、`fecb9a1`〔#905〕）、31 筆 PR（#889–#922，審查途中 `--strict` 重跑又多出 #923、#924、#925，與 #925 一併處理，共 34 筆）、4 筆 Issue（#886–#888、#917）。224 筆中日期早到 2026-08-26 的是 PR 分支上的原始提交，上游 2026-11-07 起才合併進 `main`，所以排在 baseline 之後。相對 `195eab2` 共 218 檔 +17,484／-634。水位：commit `195eab2`→`fecb9a1`、PR 885→925、Issue 880→917。沒有對上游留言、開 PR 或 push。

**方法**：fork 與上游沒有共同祖先，所以先 `git fetch upstream main`，再 `git diff 195eab2 upstream/main` 取得整段差異，以 `git apply -3 --index` 套用；13 檔衝突，逐檔手解（下表），其餘乾淨套用。未合併 PR 取每筆**目前**的 head，用 `gh pr diff`（唯讀）抓 diff。隱藏內容掃描（`\S\s{40,}\S`、`eval(`／`new Function(`／`globalThis`／`atob(`／`fromCharCode`、120 字元以上 base64 長串、零寬與雙向控制字元、控制碼、`curl|bash`／`iwr|iex`／`bypass`／`dangerously`／`skip-permissions`、超過 400 字元的新增行）：整段合併差異與 22 筆未合併 PR 的 diff 都沒有零寬、雙向控制、控制碼、base64 命中，`eval`／`atob` 等 0 命中。需要人看的命中有兩處：`tools/minicut_cli.py` 的安裝提示字串含 `curl -fsSL https://minicut.ai/install.sh | bash`（只是錯誤訊息，程式不會執行它；處理見下），以及 Markdown 與 JSON 的長段落（`tools/provider_contracts/pika_h3_flex.json`、技能文件、README 翻譯）。

### commit 軸：整批採用，13 檔衝突的處理

| 檔案（來源 PR） | 處理 | 理由 |
| --- | --- | --- |
| `README.md`（#908、`d21f5d4`） | 保留 fork | fork 的繁中主檔是自寫的；上游新增的語言切換列與「早期使用者」公告改併入 `README.en.md`（鏡像），`README_pt-BR.md`、`README_es.md`、`README_zh-CN.md` 的英文連結改指 `README.en.md` |
| `.gitignore`（#875） | 兩邊都留 | fork 的報告檔忽略規則，加上游的 `.npm-cache/`、`pytest-of-*/`、`gfpgan/` |
| `remotion-composer/src/Explainer.tsx`（#585、#895） | 兩邊都留 | fork 的 `fontFamily` 與上游的 `{...props.captionProps}` |
| `remotion-composer/src/components/TextCard.tsx`（#780） | 兩邊都留 | fork 的 `fontFamily`（CJK 字型），加上游的 `whiteSpace: "pre-line"` |
| `remotion-composer/src/components/charts/BarChart.tsx`（#656） | 保留 fork | fork 在 2026-09-13 以 `decimals` 屬性修了同一個問題（Issue #654），標籤與軸刻度都用它；上游另寫 `formatValue`，合併帶進來但不再被引用，已刪除。上游測試 `tests/contracts/test_bar_chart_format_contract.py` 釘的是 `formatValue` 這個實作，改成斷言同一性質（標籤不套用一位小數的格式），已登記 `FORK.md` |
| `scripts/backlot_simulate_run.py`（#749） | 保留 fork 並補一步 | fork 版本有完整 proposal 階段；上游新增的契約要求完成的 proposal 檢查點必須帶 `approval.status` 為 approved 的封包，fork 版本原本留在 pending，上游新測試 `tests/backlot/test_simulate_run.py` 修前失敗（`CheckpointValidationError`），補上「核准後存檔再完成」，修後通過 |
| `tests/tools/test_stock_source_adapters.py`、`tools/video/stock_sources/pond5_pd.py`（#597） | 保留 fork | fork 的 Pond5 空白金鑰視為未設定，及其 2 個測試 |
| `tools/audio/piper_tts.py`（#889） | 保留 fork | fork 版本已包含上游的 UTF-8 編碼，並多傳 `PYTHONIOENCODING` 給子行程 |
| `tools/graphics/diagram_gen.py`（#786） | 取上游 | `idempotency_key_fields` 與 `cache_key()` 較完整；fork 原有的 `idempotency_key()` 覆寫保留 |
| `tools/subtitle/subtitle_gen.py`（#718、#721） | 合併 | 上游的 `escape()` 與 fork 的 `_join_tokens()` 同時使用 |
| `tools/video/hyperframes_compose.py`（#844） | 取上游 | 離線快取優先；404 與暫時性錯誤分開回報 |
| `tools/video/video_trimmer.py`（#554） | concat 保留 fork，其餘取上游 | fork 的 concat 已把 `-ss`／`-to` 放在 `-i` 前並檢查輸出有影像串流；取上游 `_cut` 的 `-ss`／`-t` 加 `-avoid_negative_ts`，以及 `codec: auto`。複查發現 schema 預設 `auto` 只有 `_cut` 懂，concat 會產生 `-c:v auto` 讓 ffmpeg 失敗；`_concat` 把 `auto` 視為 `copy`（concat demuxer 要求各段編碼參數一致，且與先前預設相同），新增 `tests/tools/test_video_trimmer_concat_codec.py`，修前 1 failed、修後 2 passed |

**其他調整**（皆已登記 `FORK.md`）：

- `tools/minicut_cli.py`（#900）：`INSTALL_INSTRUCTIONS` 不採用 `curl … | bash`，改為請維護者自行下載、讀過再執行。MiniCut 工具（#900–#903）本身照上游採用；程式只呼叫已安裝的 `minicut` 命令，不會自行安裝。
- `tests/contracts/test_skill_reference_paths.py`（#809）：本 fork 的 `docs/DECISIONS.md` 用 `path:line`、`path:起-訖`、`path:行,行` 引用程式位置，測試先去掉這些後綴再檢查路徑；另把本檔 2026-09-13 條目的 「lib/fonts.ts」 改成完整路徑 `remotion-composer/src/lib/fonts.ts`。
- 新依賴：`requirements.txt` 新增 `pythainlp>=5.0`（泰文字幕斷詞，#895）與 `certifi>=2026.10.19`。`.github/dependency-deferrals.json` 各加一筆（`certifi` 2026.10.23、`pythainlp` 5.4.0，2026-12-10 回頭看）；`ruff`、`google-genai`、`openai`、`fastapi` 的 REVIEW UPDATE 在本次審查之前就存在，不屬於本次範圍。
- `remotion-composer/package.json` 新增 `engines.node`（`^22.23.4 || ^24.22.1 || ^26.12.1`）；`.node-version` 為 22.23.4。本機 Node 為 26.12.1，符合。
- 新檔：`.claude/commands/reel.md`（#673，只是把請求導向本 repo 的技能流程，沒有外部指令）、`README_pt-BR.md`、`README_es.md`。

### PR／Issue 軸

已合併的 PR（#889、#895、#897、#898、#900–#903、#905、#906、#908）隨 commit 軸採用，不另列。

| 項目 | 狀態／head | 規模 | 結論 | 證據與觸發條件 |
| --- | --- | --- | --- | --- |
| PR #894＋Issue #888 | open `c0f4ee87` | +181/-5 4 檔 | **採用(移植做法)** | Windows 用 `.venv\Scripts\python.exe` 直接執行、沒有啟用 venv 時，`shutil.which("piper")` 找不到裝在同一個 `Scripts` 的 `piper.exe`，狀態被誤報為不可用。`tools/audio/piper_tts.py` 新增 `_resolve_executable()`（PATH 優先，其次直譯器同目錄，Windows 另補 `.exe`，目錄不算執行檔），`get_status()` 與 `_generate()` 共用；沒找到時 `_generate()` 仍用裸名 `piper`，維持原本的失敗方式（上游版本改成提前回錯，會讓既有測試跟著改）。新增 `tests/tools/test_piper_adjacent_launcher.py` 4 個測試，修前 2 個失敗、修後通過。README 段落不收（fork 的 `README.md` 沒有安裝章節）。觸發=上游合併後比對 |
| PR #915 | open `68ab36c2` | +46/-3 2 檔 | **採用(同上游 diff)** | `tools/analysis/scene_detect.py` 以 `threshold or 27.0` 取預設，明確傳入 `0` 會被當成沒傳。diff 與上游相同；新增的 `tests/tools/test_scene_detect_threshold.py` 修前 3 個失敗、修後通過 |
| PR #913 | open `cd7f4e65` | +8/-5 4 檔 | **採用(同上游 diff)，測試加調整** | `skills/core/remotion.md`、`skills/creative/bg-remove-usage.md`、`skills/creative/lip-sync-usage.md` 引用的路徑不存在（「skills/styles/」、「tools/bg_remove.py」、「tools/lip_sync.py」），改成實際路徑；同 PR 擴大 `tests/contracts/test_skill_reference_paths.py` 的檢查範圍，套上測試後 12 個失敗，其中 9 個是本 fork `docs/DECISIONS.md` 的 `path:line` 引用被誤判（`path:行,行` 的寫法到第二次全量才發現），見上方調整 |
| PR #923 | open `b1abd981` | +115/-1 2 檔 | **採用(同上游 diff)** | 渲染前的 slideshow 閘門只認場景清單；傳入 `scene_plan` 產出物（`{"version", "scenes"}`）時被當成鍵的迭代，評分丟例外被吞成警告，檢查等於沒執行。`tools/video/video_compose.py` 的 `_pre_compose_validation()` 改為先取出 `scenes`，並在輸入 schema 宣告 `scene_plan`。diff 與上游相同；新增的 `tests/tools/test_video_compose_scene_plan_artifact.py` 修前 6 個失敗、1 個通過，修後 7 個全過 |
| PR #924 | open `60ab427e` | +93/-7 5 檔 | 延後 | `StatCard`、`HeroTitle` 的字型改吃主題標題字型；`TextCard` 的 `fontFamily` 屬性 fork 已有（`remotion-composer/src/components/TextCard.tsx`），diff 在 `Explainer.tsx` 與 `TextCard.tsx` 上無法直接套用。觸發=上游合併，或本機影片的數字卡／標題卡字型與主題不一致 |
| PR #925 | open `c0dfe11d` | +254/-16 2 檔 | 延後 | 審查途中新增；放寬 `schemas/artifacts/edit_decisions.schema.json` 讓 Explainer 場景屬性通過驗證。schema 變更，需對照本 fork 的 `edit_decisions` 使用；diff 掃描 0 命中。觸發=上游合併 |
| PR #909 | open `f37ec8e4` | +65/-10 2 檔 | 無需動作 | 上游 #703 已合併，`tools/analysis/frame_sampler.py` 已用暫存目錄只回報本次的影格；PR 的 4 個測試在合併後的樹上直接通過（`4 passed`） |
| PR #891 | open `3ed54e09` | +418/-1 4 檔 | 延後 | 在工具執行時強制預算閘門（新 「tools/cost_gate.py」，改 `tools/tool_registry.py`，與合併後的 `tool_registry.py` 衝突）。行為變更且動到所有工具的執行路徑；本線沒有設預算上限的使用情境。觸發=上游合併，或本機啟用預算上限 |
| PR #899 | open `9e4b67ce` | +786/-1 6 檔 | 延後 | Kling 4 經 MiniCut CLI 的新 provider，建立在 #900 之上，`docs/PROVIDERS.md` 衝突。本機沒有安裝 `minicut`，無法實跑。觸發=上游合併，或本機啟用 MiniCut |
| PR #912 | open `a11d66a5` | +111/-2 3 檔 | 延後 | 缺陷屬實：`tools/graphics/code_snippet.py:99`、`:103` 宣告了 `border_radius`、`width`，執行時沒有使用。修法會改變輸出圖片尺寸與透明度。觸發=上游合併，或本線出現需要這兩個參數的卡片 |
| PR #918 | open `894bdb87` | +161/-14 2 檔 | 延後 | 缺陷看來屬實：`tools/video/video_compose.py:447-448` 的 `-af apad` 搭配 `-shortest` 與 `-c:v copy`。上游描述 ffmpeg 會停在 100% CPU；本機未重現（沒有觸發的素材），不在沒有證據時改動混音路徑。觸發=上游合併，或本機遇到混音卡住 |
| PR #919 | open `edc82bdb` | +35/-1 2 檔 | 延後 | `tools/audio/audio_mixer.py:675` 的 `apad=whole_dur=`；上游說 `target_duration` 會隨機截斷，同 #918 屬混音路徑，未重現。觸發=上游合併，或遇到截斷 |
| PR #920 | open `338f9fa8` | +113/-1 8 檔 | 延後 | `edit_decisions` 新增每段 `tone`／`filter` 欄位（改 schema 與 `CinematicRenderer.tsx`）；新功能。觸發=上游合併 |
| PR #921 | open `16607bd4` | +109/-15 3 檔 | 延後 | `remotion-composer/src/components/charts/KPIGrid.tsx:278` 以 `Math.round` 計數，小數 KPI 顯示成整數；缺陷屬實，新增 `format.ts`。與 #922 同一類圖表格式化。觸發=上游合併，或本機影片出現小數 KPI |
| PR #922 | open `57c4dc99` | +112/-7 3 檔 | 延後 | `remotion-composer/src/components/charts/LineChart.tsx:88` 的 x 軸刻度用 `formatNumber`，年份會印成 `2.0K`；與合併後的樹有衝突（`git apply --check` 失敗於 `LineChart.tsx:178`）。觸發=上游合併，或本機折線圖用年份當 x 軸 |
| PR #896 | open `d9cc159a` | +98/-2 2 檔 | 略過 | `Makefile` 把選定環境的 `bin` 放上 `PATH`；本線在 Windows 用 PowerShell 腳本，Piper 的同一問題由 #894 的移植處理 |
| PR #911 | open `6cc23b99` | +53/-52 12 檔 | 略過 | 上游組織搬遷後的連結與 `ci.yml` 改寫，會蓋掉 fork 的 CI 與 README；與本線無關 |
| PR #914 | open `c940612b` | +12/-0 1 檔 | 略過 | `.claude/launch.json` 加入作者個人專案的預覽伺服器 |
| PR #916 | open `fc4ebfe4` | +3/-3 1 檔 | 略過 | `remotion-composer/package-lock.json` 只是搬動 `engines` 欄位的位置，沒有行為差異 |
| PR #890 | closed `a4151a1c` | +1230/-0 35 檔 | 略過 | 個人宣傳片素材（含 mp4）、`.github/workflows/media-job.yml` 與 「scripts/run_job.py」；非修正，上游未收 |
| PR #893 | closed `3d5d6988` | +26/-5 3 檔 | 略過 | 讓 Backlot 綁定位址與信任主機清單可由環境變數放寬；會削弱 DNS rebinding 防護，上游未收 |
| PR #907 | closed `dcaacab9` | +5844/-7 35 檔 | 略過 | 新的 relay provider 層與設定檔；非修正，上游未收 |
| PR #910 | closed `2cba40f3` | +14458/-625 211 檔 | 略過 | 「CI 驗證用的批次整合」，內容就是上述已合併 PR 的集合，上游未收 |
| Issue #886 | closed | — | 無需動作 | 已由 #897 合併修正 |
| Issue #887 | open | — | 延後 | CogVideoX 在 Apple Silicon 的 MPS 張量型別錯誤；本機是 Windows，無法重現。觸發=上游合併修正，或本機使用 Apple Silicon |
| Issue #917 | open | — | 略過 | 要求新增 Google AI Pro 方案支援，不是缺陷 |

### 後續修正

- `AGENTS.md` 的「測試檔案一律不可提交」與同檔的測試目錄說明及長期做法（`tests/`、`tools/tests/` 皆提交）矛盾，改寫為只排除臨時重現腳本、測試產出與素材。
- `tools/test_fork_regressions.ps1` 補入本次新增或改寫的回歸測試。

### 驗證

Windows 11、Python 3.14.10，在專案 `.venv`（補裝 `pythainlp` 5.4.0 與 `certifi`）內執行，BelowNormal 優先權。

| 指令 | 結果 |
| --- | --- |
| `python -m pytest -q --ignore=tests/qa/test_08_end_to_end.py`（衝突解完後第一次） | 4 failed、2975 passed、19 skipped：模擬執行（上游新增的核准契約）、`BarChart` 釘實作的契約測試、泰文斷詞 2 項（venv 缺 `pythainlp`）；前兩項依上表處理，後兩項補裝依賴後通過 |
| 同上（移植與調整後第二次） | 1 failed、3346 passed、19 skipped：失敗的是引用路徑測試遇到 `path:行,行` 後綴，已修正並單獨重跑 |
| 同上（含 #923 移植與本節文字，第三次） | 6 failed、3388 passed、19 skipped：6 個失敗都是本節文字把不存在的路徑（舊路徑、上游新增檔）放在反引號內被引用路徑測試擋下，改用「」標示後 `python -m pytest -q tests/contracts/test_skill_reference_paths.py` 為 404 passed |
| `python -m pytest -q tests/tools/test_video_compose_scene_plan_artifact.py tests/tools/test_scene_detect_threshold.py tests/tools/test_piper_adjacent_launcher.py` | 先紅後綠：#923 修前 6 failed／1 passed、修後 7 passed；#915 修前 3 failed、修後通過；#894 修前 2 failed／2 passed、修後 4 passed |
| `remotion-composer`：`npm ci --ignore-scripts` | `found 0 vulnerabilities` |
| `remotion-composer`：`npx tsc --noEmit` | exit 0 |
| `remotion-composer`：`npx remotion bundle src/index.tsx` | exit 0 |

**排除與未驗證**：`tests/qa/test_08_end_to_end.py` 排除原因同 2026-10-24（Windows 清理暫存檔 `PermissionError`）。需要付費金鑰、`minicut` 命令、GPU 或 Apple Silicon 的 provider 只由 mock 測試覆蓋，沒有實機呼叫。

### 水位

`tools/upstream_baseline.json`：`reviewed_through` `195eab2`→`fecb9a1e3cc23ef84de30b272059457a427f16f8`、`reviewed_pr_through` 885→925、`reviewed_issue_through` 880→917、`reviewed_date` 2026-11-10。Baseline 代表已審查，不代表已合併。
