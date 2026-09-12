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