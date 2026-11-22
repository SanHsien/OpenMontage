# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `500484e343d4` 查的快照，開工前先重查 GitHub。

## 現況
這是 Windows 原生的 AI 影片製作維護 fork（[AGENTS.md:7](AGENTS.md)、[README.md:62](README.md)）。2026-10-29 `gh` 查詢顯示 CI、CodeQL、Dependency freshness、Upstream check 最近結果成功，Dependabot 與 code scanning 開啟告警皆為 0；issues 停用，未查到 issue，不能當成零筆（2026-10-29 `gh` 查詢）。目前限制是雲端 OpenAI 工具只有 mock 驗證，語料 Dependabot 新設定仍待下一次適用事件驗證（[docs/DECISIONS.md:462](docs/DECISIONS.md)、[docs/DECISIONS.md:481](docs/DECISIONS.md)）。2026-10-30 已核對最近 CI 的七項略過，皆為 FFmpeg／ffprobe 在 PATH 不可用；本機符號連結權限略過是另一情境，逐項證據見 [docs/DECISIONS.md](docs/DECISIONS.md)。

## 近期：可以直接動手
| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 重評 7 筆因 PyPI 出新版而失效的依賴延後（ruff 0.17.6、pydantic 2.14.4、certifi 2026.11.20、google-auth 2.63.0、google-genai 3.6.1、openai 3.57.0、fastapi 0.165.0） | 2026-11-21 `python tools/check_dependency_freshness.py --strict` 對這 7 筆回報 `REVIEW UPDATE`（exit 1），所以 `Dependency freshness` workflow 在處理完之前是紅的。同日的八筆重評沒有處理它們：ruff 依審查政策第 3 點要獨立落地，google-genai／openai 跨了多個版本要讀 changelog，certifi 要讀信任根異動 | 逐筆讀 release notes；在乾淨環境測該版；`tools/dev_check.ps1` 與 `tools/test_fork_regressions.ps1` 通過；每筆採用或續延有理由，strict 檢查回到 exit 0 | Codex | [docs/DECISIONS.md](docs/DECISIONS.md)（2026-11-21：這 7 筆在乾淨 venv 的實裝版本與 gate 結果已記錄，可沿用為起點） |
| 裁決四筆落在已知弱點範圍內的宣告下限（pydantic 2.0、pytest 8.0、Pillow 10.0、torch 2.0） | 維護者 2026-11-21 裁決「下限不得落在已知弱點範圍內」，已套用到 requests 與 python-dotenv；2026-11-22 對所有下限查 OSV，還有這四筆在範圍內。沒有已知弱點的最低版本分別是 pydantic 2.4.0、pytest 9.0.3、Pillow 13.0.0（即現行版，要跳三個主版本），torch 有數筆 OSV 沒列修正版本 | 逐筆決定調高到哪一版或記下例外理由；調高的在乾淨環境測該下限版本，`tools/dev_check.ps1` 與 `tools/test_fork_regressions.ps1` 通過；`requirements*.txt` 與 `setup.py` 一起改，並記入 `FORK.md` | 維護者裁決，Codex 執行 | [docs/DECISIONS.md](docs/DECISIONS.md)（2026-11-22：「同一規則下還沒處理的下限」表） |

## 中期：等條件成立再做
| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
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
