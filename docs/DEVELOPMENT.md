# 開發環境

維護者與 AI 接手用的開發文件。產品使用方式在 [`README.md`](../README.md)；上游同步在 [`UPSTREAM.md`](UPSTREAM.md)；決策在 [`DECISIONS.md`](DECISIONS.md)。

## 架構

```text
pipeline_defs/                 12 條影片生產流水線定義 (YAML / JSON)
backlot/                       視覺化故事板伺服器 (FastAPI + WebSocket)
remotion-composer/             Remotion 程式化動態影像合成專案 (React + TypeScript)
skills/                        影視知識與 Agent Skill 庫
tools/                         工具庫與 fork 維護工具
  ├── base_tool.py             工具基底架構
  ├── tool_registry.py         工具註冊中心
  ├── cost_tracker.py          成本追蹤器
  ├── dev_check.ps1            Windows gate
  ├── bootstrap_dev.ps1        環境初始化
  ├── test_product.ps1         產品健康度驗證
  ├── check_links.py           相對連結檢查
  ├── check_upstream_updates.py 上游檢查
  ├── check_dependency_freshness.py 依賴新鮮度
  └── tests/                   維護契約測試
docs/                          fork 維護與治理文件
```

## 本機開發（Windows 11 原生）

### 維護骨架（必跑）

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
$env:PYTHONUTF8 = "1"
pwsh -NoProfile -File tools\dev_check.ps1
```

等價一鍵指令：

```powershell
pwsh -NoProfile -File tools\bootstrap_dev.ps1
```

若需一併安裝產品執行依賴：

```powershell
pwsh -NoProfile -File tools\bootstrap_dev.ps1 -All
```

### 執行產品測試

本 repo 提供專用 Windows 原生產品測試腳本 `tools/test_product.ps1`：

```powershell
pwsh -NoProfile -File tools\test_product.ps1
```

## Canonical Gate

`tools\dev_check.ps1` 會依序執行：

1. `python -m compileall`（`tools`）
2. `ruff check`（E9 + F，僅檢查 `tools`）
3. `pytest tools/tests`（使用獨立的 `tools/pytest.ini`）
4. `python tools/check_links.py`（驗證所有維護文件相對連結）

CI 專注於 Windows 原生環境，在 `windows-latest` 執行完整 Python 3.10–3.14 矩陣並跑過 gate。推至 `main` 前請務必在本機跑過 gate。

## 依賴新鮮度

`tools/check_dependency_freshness.py` 納管 `requirements-dev.txt`、`requirements.txt` 與 `requirements-gpu.txt`。

紅燈只有兩條誠實的出口：

| 出口 | 寫在哪 | 什麼時候用 |
| --- | --- | --- |
| `# freshness-hold: <理由>` | requirements 文件行末 | 這個下限就是我們要的 |
| `.github/dependency-deferrals.json` 的 `deferredLatest` + `reason` | 獨立檔案 | 已看過、這個月不升；PyPI 超過該版本會恢復提醒 |

不要用調高下限讓報告變綠。

## 不要做的事

- 不要提交含有個人憑證、API key 或敏感商業影片的檔案。
- 不要把 PR 指向上游 `calesthio/OpenMontage`。