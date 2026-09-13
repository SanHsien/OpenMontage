# 上游維護

## Remote

- Fork：`origin` → `https://github.com/SanHsien/OpenMontage.git`（預設分支 `main`）
- 原作者：`upstream` → `https://github.com/calesthio/OpenMontage.git`（預設分支 `main`）
- 追蹤分支：`main`

## 檢查新提交

```powershell
git fetch upstream main
python tools\check_upstream_updates.py --strict
```

工具以 `tools/upstream_baseline.json` 的 `reviewed_through` 為起點，列出所有未審查提交、PR 與 Issues。
有新變更或檢查失敗時，`--strict` 回傳非零；排程 workflow 也會因此明確亮紅燈提醒。

CI 沒有 `upstream` remote，所以 baseline 的 `repo` 寫完整 clone URL，不要寫遠端短名。

## 審查清冊

每次只做一次批次審查：

1. 讀 commit 主旨與變更檔案（open PR 必須讀 diff，禁止只憑標題結案）。
2. 判斷是否與繁中 README、Windows gate、發佈閘門或測試衝突。
3. 可直接同步的提交用 merge；只需要部分修正時 cherry-pick 或最小重做。
4. 跑 `pwsh -NoProfile -File tools\dev_check.ps1`。
5. 在 `docs/DECISIONS.md` 記錄採用／略過理由。
6. 驗證完成後才把 baseline 推進到已審查的完整 40 字元 SHA 與更新 PR/Issue 水位。

Baseline 代表「已審查」，不代表「全部已合併」。

## 2026-09-12：fork 起點

本 fork 自上游 `main` `08e2151fa02de28a5d6a312b3d575692bf147ad7`
（短 SHA 為 `08e2151`）建立。
此 SHA 設為第一個 `reviewed_through`。
之後的上游 commit 才需要進入審查清冊。

---

## 2026-09-12：上游 PR、Issue、分支全面盤點

2026-09-12 對 [`calesthio/OpenMontage`](https://github.com/calesthio/OpenMontage) 進行完整盤點：
上游活躍度極高，累積超過 649 筆 PR 與 Issues。

### 一、上游分支清理

Fork 自動複製了 27 個非 main 分支，已自 `origin` 全數清理刪除。
本 fork **唯一長期跟隨分支為 `upstream/main`**。

### 二、防重複評估機制（Watermark 機制）

為避免每次巡檢重複評估既有項目，本專案實施嚴格的水位線（Watermark）機制：

1. **基準水位鎖定**：
   - Commit 水位：`08e2151fa02de28a5d6a312b3d575692bf147ad7`（短 SHA `08e2151`）
   - PR 水位：`649`
   - Issue 水位：`649`
   - 記錄於 [`tools/upstream_baseline.json`](../tools/upstream_baseline.json)。

2. **增量巡檢機制**：
   - 每次執行 `tools/check_upstream_updates.py` 或 GitHub Actions 每週排程時，檢查器會自動過濾 `number <= watermark` 的項目。
    - 只有編號大於 **#649** 的新開 PR / Issue，或 `main` 上高於 `08e2151` 的新 Commit，才會出現在待審報告中。
    - 當新項目被審查完畢並於 `docs/DECISIONS.md` 記錄結論後，再遞增更新 baseline 水位。

### 三、首次上游未合併分支與待處理 PR 處理紀錄

| 項目 | 類型 | 評估結論 | 處置方式 |
|---|---|---|---|
| `upstream/fix/backlot-ui-layout` | Branch | 經查其修訂（no-cache、9:16 portrait video 樣式、媒體欄排版）已在 `main` 完整落實 | 判定為過期陳舊分支，不需重複處理 |
| `upstream/docs/readme-add-alexandria-remove-abyss` | Branch | 僅更新 Star 歷史圖表與徽章 | 略過，無功能性價值 |
| PR `#640` | PR | 修復 `diagram_gen` Mermaid CLI 可用性假陽性 | **引進合併**至本 fork |
| PR `#641` | PR | 修復 `source_media_review` 影片技術探針被音訊覆蓋與抽樣 key 錯誤 | **引進合併**至本 fork |
| PR `#642` | PR | 修復 `video_trimmer` concat 輸入 seek、編碼器選擇與 videoless 檢驗 | **引進合併**至本 fork |
| PR `#649` | PR | Remotion 支援 CJK / 繁體中文與非拉丁字型載入，修復模擬門禁 | **引進合併**至本 fork |
| PR `#650` | PR | Remotion 字幕單字間距保持（non-breaking space）與深色主題卡片對比修復 | **引進合併**至本 fork |
| Issue `#626` | Issue | 防範網路假冒二進位安裝檔（`OpenMontage-app`）木馬釣魚 | 寫入 `SECURITY.md` 警示宣告 |