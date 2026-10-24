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
