# Repository review（Windows-only）

- Review date: 2026-09-12
- Review baseline: `08e2151fa02de28a5d6a312b3d575692bf147ad7`
- Remediation: 同日 fork-local overlay（不回貢）
- Upstream reviewed through: `08e2151fa02de28a5d6a312b3d575692bf147ad7`
- Primary environment: Windows 11、PowerShell、Python 3.10-3.14（本機 gate）；產品 Python 要求 `>=3.10`
- Status: 維護骨架與產品相依環境全面可用。已完成建立 Windows 原生門禁與驗收。

## 結論

這個 fork 適合作為 Windows 本機、給 Agent 維護的 OpenMontage 影片生成線。產品行為跟隨 `calesthio/OpenMontage` `08e2151`，再加上本線維護骨架：繁體中文維護文件、Windows 原生 1-click gate、純 Windows 原生維護 CI、每週上游水位追蹤（commit、PR、issue）以及每月依賴新鮮度檢查。

本專案之維護依賴（`pytest`, `ruff`, `httpx`）已完整梳理並通過 Windows 原生環境驗證。在 Windows 環境下執行腳本時，門禁與工具腳本全面注入 `$env:PYTHONUTF8 = "1"`，避免 Windows 預設 ANSI/CP950 編碼解碼 UTF-8 檔案失敗。

## 本輪實證

### 審查當下（`08e2151`）

```text
git rev-parse HEAD
→ 08e2151fa02de28a5d6a312b3d575692bf147ad7

gh repo set-default --view
→ SanHsien/OpenMontage
```

實查結果：
- 上游 repository 為 `calesthio/OpenMontage`，採 GNU Affero General Public License v3.0 (AGPL-3.0)。
- 上游 PR 水位為 `#649`，Issue 水位為 `#649`。
- 上游已配置 ubuntu CI，本 fork 建立了純 Windows 原生 CI 工作流程。
- 維護工具無 `os.system`／`shell=True`／`eval(`／`exec(`。

## 已修 findings

| ID | 嚴重度 | 做了什麼 |
|---|---|---|
| R-01 | P2 | `.gitignore` 加入 `.env`、`.venv`、`upstream-review-report.md`、`dependency-freshness-report.md`、`.ruff_cache/` |
| R-02 | P2 | 建立獨立維護測試目錄 `tools/tests/` 與獨立 `tools/pytest.ini`，避免產品環境污染 |
| R-03 | P2 | 建立 `FORK.md`、`NOTICE.md`、`SECURITY.md`、`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`，寫明對外邊界與安全性 |
| R-04 | P3 | `README.md`（繁體中文）與 `README.en.md`（英文鏡像）雙向互指，並標明 upstream 與 AGPL-3.0 條款 |
| R-05 | P2 | 建立 `tools/dev_check.ps1` 與 `tools/bootstrap_dev.ps1`，規範 Windows 11 原生 PowerShell 驗收門禁（注入 `PYTHONUTF8=1` 防範 CP950 解碼例外） |
| R-06 | P2 | 建立 `tools/test_product.ps1` 驗證 Python 語法健康度、工具註冊中心發現與 demo 清單 |
| R-07 | P2 | 建立純 Windows 原生 CI（`ci.yml`、`codeql.yml`、`upstream-check.yml`、`dependency-freshness.yml`） |
| R-08 | P2 | 建立上游追蹤水位防重複巡檢機制，鎖定 PR `#649`、Issue `#649` |
| R-09 | P2 | 清理 GitHub fork 遠端上 27 個非 main 分支，維持 `origin` 僅有單一維護主線 `main` |
| R-10 | P1 | 修復 `tools/video/hunyuan_video.py` 遺漏 `from typing import Any`（Ruff F821 未定義變數例外） |
| R-11 | P3 | 修正 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md` 引用 `AGENT_GUIDE.md`，使 `test_platform_wrappers_reference_agent_guide` 100% 通過 |
| R-12 | P2 | 引進上游 PR #640：`tools/graphics/diagram_gen.py` 精確回報 Mermaid CLI (`mmdc`) 可用性狀態，並在 Preflight 拋出明確警示 |
| R-13 | P1 | 引進上游 PR #641：修復 `lib/source_media_review.py` 將影片資訊誤歸類為音訊探針、`frame_sampler` 遺漏 `strategy` 參數及回傳 frame key 錯誤，徹底解決影片抽樣與規格誤報問題 |
| R-14 | P1 | 引進上游 PR #642：修復 `tools/video/video_trimmer.py` concat 模式因輸出 seek 導致輸出無畫面（僅剩 1 幀/純音訊）之嚴重大 bug，並修正 `codec` 被忽略、`list_path` 提前未綁定引發 `UnboundLocalError`，並加入輸出影片解碼幀驗證 |
| R-15 | P2 | 引進上游 PR #649：為 Remotion 增加 CJK / 繁體中文與非拉丁字型動態注入支援（`lib/fonts.ts`、`Explainer.tsx`、`TextCard.tsx`），並補齊 `scripts/backlot_simulate_run.py` 所缺之 proposal 門禁前置條件 |
| R-16 | P2 | 修復 Windows 11 環境下 `hyperframes_compose.py` 與 `video_trimmer.py` 呼叫 subprocess 時因預設 cp950 導致 `UnicodeDecodeError: 'cp950'` 之例外，全面強化 `encoding="utf-8", errors="replace"` |
| R-17 | P2 | 引進上游 PR #650：修復 Remotion 字幕在 inline-block 中單字空白被瀏覽器修剪黏合之缺陷（改採 non-breaking space 保持間隔），並修復深色主題下 `KPIGrid` 與 `ComparisonCard` 顏色對比度不足／卡片文字白底白字之問題 |
| R-18 | P2 | 引進 PR #644：新增 tools/audio/music_selector.py，串接音樂三大能力層與成本選擇 |
| R-19 | P2 | 引進 PR #647：修復 tools/cost_tracker.py 狀態轉移漏洞，防止已完成預算被竄改 |
| R-20 | P2 | 引進 PR #651：修復 Pexels/Pixabay 庫存提供者 Preflight 檢測與空白環境變數判定 |
| R-21 | P2 | 引進 PR #652：傳播 Archive.org 與 Wikimedia 傳輸錯誤至 corpus_builder |
| R-22 | P2 | 引進 PR #653：修復 Pond5 契約，強制金鑰與 Bearer 驗證，清空全部 known transport swallowers |
| R-23 | P2 | 修復 Issue #654：修復 BarChart.tsx 與 LineChart.tsx 數值標籤浮點數精度截斷問題 |
| R-24 | P3 | 評估 PR #655：安全白名單門控（密集迭代中），維持 Defer 暫緩引進決策 |
| R-25 | P2 | 引進 PR #659：tools/_comfyui/client.py 明確以 UTF-8 載入工作流，防止 Windows cp950 解碼非 ASCII 崩潰 |
| R-26 | P2 | 建立 main 分支保護規則：綁定 Windows CI 矩陣、CodeQL、Upstream check，禁止 force-push 與 deletion |
| R-27 | P1 | 全面修復 GitHub Code Scanning 全部 17 個警示：包含 Kling 金鑰 PBKDF2 安全雜湊（CWE-327）、Backlot 伺服器路徑注入防護（CWE-22）與各模組 URL 網域名稱精準解析校驗（CWE-20） |

## 接受、不改契約

| ID | 嚴重度 | 處理 |
|---|---|---|
| - | - | （無。所有已識別項目皆已妥善處理完畢） |

## 尚未宣稱範圍

- **不宣稱** 已將任何修改提交回原作者上游（依 fork 維護政策，所有 PR/commit 僅限於 `SanHsien/OpenMontage`）。
