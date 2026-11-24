# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 本輪狀態於 2026-11-24 在 `codex/upstream-1124` 起始 SHA `2942c696c3dce088a9342ed689f6389f28744388` 查核；以下舊 CI 數字保留為歷史快照，不代表目前服務狀態。

## 現況
2026-11-24：已審上游 main `2e003e65fa99a0f329478a2c1cdcf26bc481933a`（1 commit、31 PR、19 Issue），PR 水位 #981、Issue 水位 #977。採用 #979／#964 的 BFL 憑證保護目的並本地重做；#980 已由本地 `fcb37d9` 等效修復。GitHub Actions 停用的最後本地記錄是 `2942c69`；本輪未重查 Actions 帳號狀態、不推送。逐項證據見 [docs/DECISIONS.md](docs/DECISIONS.md)。

這是 Windows 原生的 AI 影片製作維護 fork（[AGENTS.md:7](AGENTS.md)、[README.md:62](README.md)）。2026-10-29 `gh` 查詢顯示 CI、CodeQL、Dependency freshness、Upstream check 最近結果成功，Dependabot 與 code scanning 開啟告警皆為 0；issues 停用，未查到 issue，不能當成零筆（2026-10-29 `gh` 查詢）。目前限制是雲端 OpenAI 工具只有 mock 驗證，語料 Dependabot 新設定仍待下一次適用事件驗證（[docs/DECISIONS.md:462](docs/DECISIONS.md)、[docs/DECISIONS.md:481](docs/DECISIONS.md)）。2026-10-30 已核對最近 CI 的七項略過，皆為 FFmpeg／ffprobe 在 PATH 不可用；本機符號連結權限略過是另一情境，逐項證據見 [docs/DECISIONS.md](docs/DECISIONS.md)。

## 近期：可以直接動手
| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |

## 中期：等條件成立再做
| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 重評 2026-11-24 延後的上游項目 | baseline 監看的 PR head／狀態變動，或本次決策表的實際需求／缺陷觸發；Kling MCP #944 與 Parallel search #961 依需求及前置條件觸發 | 依 [docs/DECISIONS.md](docs/DECISIONS.md) 本次逐筆條件重現、測試、採用或續延；#970 必須先通過技能包靜態稽核才可安裝；任何修正先紅後綠，Windows gate 通過 | Codex | [tools/upstream_baseline.json](tools/upstream_baseline.json) 的 monitored 與本次決策表 |
| 重評 Pillow 與 torch 下限的例外 | 上游調高對應下限、Pillow 或 torch 出現可用的修正版本資訊，或 2026-12-21（先到者） | 重查 OSV；有乾淨且不跳主版本的下限就調高，並在乾淨環境測該下限、`tools/dev_check.ps1` 與 `tools/test_fork_regressions.ps1` 通過；否則更新例外理由與日期 | Codex 執行 | [docs/DECISIONS.md](docs/DECISIONS.md)（2026-11-22：「其餘四筆宣告下限」） |
| 驗證語料 Dependabot 排除設定 | 語料依賴再次收到安全公告 | 查該目錄的 Dependabot job，確認不再產生 `update_files` 失敗；若設定未生效，修正後重驗且保留 composer 的安全更新 | Codex | [docs/DECISIONS.md:449](docs/DECISIONS.md) |
| 驗證 google-genai 3.x 在 API key 模式的 `v1` 預設 | 維護者提供 Gemini API key 並同意費用；或有人回報 Lyria／Gemini 圖片在 google-genai 3.x 失敗 | 在 google-genai 3.x 用 API key 各跑一次 `google_music`（`lyria-3.5`、`lyria-3-pro-preview`）與 `google_imagen` 的 Gemini 圖片路徑；失敗就在 `tools/google_credentials.py` 的 `get_genai_client` 明確指定能用的 `api_version` 並補離線回歸；順帶把 Veo 的 `generate_videos(prompt=, image=)` 改成 `source` 參數 | 維護者 | [docs/DECISIONS.md](docs/DECISIONS.md)（2026-11-22：google-genai 3.0.0 的兩項 breaking change，含離線記錄到的 `/v1/interactions` 路徑） |
| 驗證 OpenAI 工具實際呼叫 | 維護者提供測試帳戶並同意費用 | 用一組最小素材驗證 TTS、圖片與影片所需路徑，核對輸出與成本；離線回歸 gate 通過 | 維護者 | [docs/DECISIONS.md:481](docs/DECISIONS.md) |
| 重評慢速剪輯與 PyAV 相容修正 | 上游合併相應修正，或本機重現慢速截斷／新版 PyAV 錯誤 | 先用真實慢速片段或轉錄輸入重現，再做最小修正；避免全域替換 PyAV 函式；相關回歸與 Windows gate 通過 | Codex | [docs/DECISIONS.md:410](docs/DECISIONS.md)；上游 #858、#859 |
| 重評 2026-11-10 延後的上游修正 | 上游合併 #891、#899、#912、#918–#922、#924、#925，或本機遇到混音卡住、小數 KPI、年份刻度、卡片字型不一致 | 先在本機重現缺陷，再取上游版本或最小重做；附先紅後綠測試，`tools/dev_check.ps1` 與 `tools/test_fork_regressions.ps1` 通過 | Codex | [docs/DECISIONS.md:593](docs/DECISIONS.md)（逐項觸發條件見該節 PR／Issue 軸） |
| 重評依賴延後紀錄 | `.github/dependency-deferrals.json` 的 revisit 到期或 freshness 提醒新版 | 在乾淨環境測新版；`tools/dev_check.ps1` 與 `tools/test_fork_regressions.ps1` 通過，採用或續延有理由 | Codex | [docs/DECISIONS.md](docs/DECISIONS.md)（2026-11-05：八筆續延；雲端與 GPU 實測限制見裁決） |

## 刻意不做
| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 為舊語料更新失敗補 lockfile 或 dismiss 告警 | 固定語料的處理理由見 [docs/DECISIONS.md:449](docs/DECISIONS.md)，歷史失敗不代表目前 CI 故障 | 語料納入 CI、開始處理外部輸入或需重跑基線渲染 |
| 直接採用未合併的上游功能與改寫 fork 歷史 | 已有逐筆判斷與 baseline 制度；無共同祖先是已知的歷史整理結果 | 上游合併或實際需求命中，再按既有決策重評 |

## 維護方式
每週從 [tools/upstream_baseline.json](tools/upstream_baseline.json) 水位審查新增 commit、PR 與 issue；Upstream check 紅燈先看未審項目，驗證後才推進水位。每月查依賴新鮮度；採用理由只記 [docs/DECISIONS.md](docs/DECISIONS.md)，本檔只保留下一步。
