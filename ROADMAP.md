# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `500484e343d4` 查的快照，開工前先重查 GitHub。

## 現況
這是 Windows 原生的 AI 影片製作維護 fork（[AGENTS.md:7](AGENTS.md)、[README.md:62](README.md)）。2026-10-29 `gh` 查詢顯示 CI、CodeQL、Dependency freshness、Upstream check 最近結果成功，Dependabot 與 code scanning 開啟告警皆為 0；issues 停用，未查到 issue，不能當成零筆（2026-10-29 `gh` 查詢）。目前限制是雲端 OpenAI 工具只有 mock 驗證，語料 Dependabot 新設定仍待下一次適用事件驗證（[docs/DECISIONS.md:462](docs/DECISIONS.md)、[docs/DECISIONS.md:481](docs/DECISIONS.md)）。

## 近期：可以直接動手
| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 釐清 Windows CI 回歸測試的略過原因 | 本機與 runner 略過情境不同，既有報告只有推測 | 讀取最近 `CI` 的 fork regression 步驟；必要時用 pytest 的略過原因輸出重現，逐項確認是否為缺工具或權限，留下可核對的原因 | Codex | 深掃報告（2026-10-27）「驗證」：CI 在 `4ef7496` 為 342 passed／7 skipped，略過原因未列；commit `6875bfd` |

## 中期：等條件成立再做
| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 驗證語料 Dependabot 排除設定 | 語料依賴再次收到安全公告 | 查該目錄的 Dependabot job，確認不再產生 `update_files` 失敗；若設定未生效，修正後重驗且保留 composer 的安全更新 | Codex | [docs/DECISIONS.md:449](docs/DECISIONS.md) |
| 驗證 OpenAI 工具實際呼叫 | 維護者提供測試帳戶並同意費用 | 用一組最小素材驗證 TTS、圖片與影片所需路徑，核對輸出與成本；離線回歸 gate 通過 | 維護者 | [docs/DECISIONS.md:481](docs/DECISIONS.md) |
| 重評慢速剪輯與 PyAV 相容修正 | 上游合併相應修正，或本機重現慢速截斷／新版 PyAV 錯誤 | 先用真實慢速片段或轉錄輸入重現，再做最小修正；避免全域替換 PyAV 函式；相關回歸與 Windows gate 通過 | Codex | [docs/DECISIONS.md:410](docs/DECISIONS.md)；上游 #858、#859 |
| 重評依賴延後紀錄 | `.github/dependency-deferrals.json` 的 revisit 到期或 freshness 提醒新版 | 在乾淨環境測新版；`tools/dev_check.ps1` 與 `tools/test_fork_regressions.ps1` 通過，採用或續延有理由 | Codex | [docs/DECISIONS.md:466](docs/DECISIONS.md) |

## 刻意不做
| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 為舊語料更新失敗補 lockfile 或 dismiss 告警 | 固定語料的處理理由見 [docs/DECISIONS.md:449](docs/DECISIONS.md)，歷史失敗不代表目前 CI 故障 | 語料納入 CI、開始處理外部輸入或需重跑基線渲染 |
| 直接採用未合併的上游功能與改寫 fork 歷史 | 已有逐筆判斷與 baseline 制度；無共同祖先是已知的歷史整理結果 | 上游合併或實際需求命中，再按既有決策重評 |

## 維護方式
每週從 [tools/upstream_baseline.json](tools/upstream_baseline.json) 水位審查新增 commit、PR 與 issue；Upstream check 紅燈先看未審項目，驗證後才推進水位。每月查依賴新鮮度；採用理由只記 [docs/DECISIONS.md](docs/DECISIONS.md)，本檔只保留下一步。
