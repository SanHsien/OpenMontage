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

## 接受、不改契約

| ID | 嚴重度 | 處理 |
|---|---|---|
| - | - | （無。所有已識別項目皆已妥善處理完畢） |

## 尚未宣稱範圍

- **不宣稱** 已將任何修改提交回原作者上游（依 fork 維護政策，所有 PR/commit 僅限於 `SanHsien/OpenMontage`）。