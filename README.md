# OpenMontage — 開源 AI 全自動影片製作工作室（Windows 11 維護 Fork）

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](LICENSE)
[![Platform: Windows 11 Native](https://img.shields.io/badge/Platform-Windows%2011%20Native-0078D6.svg)](docs/DEVELOPMENT.md)
[![CI](https://github.com/SanHsien/OpenMontage/actions/workflows/ci.yml/badge.svg)](https://github.com/SanHsien/OpenMontage/actions/workflows/ci.yml)
[![Upstream Check](https://github.com/SanHsien/OpenMontage/actions/workflows/upstream-check.yml/badge.svg)](https://github.com/SanHsien/OpenMontage/actions/workflows/upstream-check.yml)

> **本專案為 [`calesthio/OpenMontage`](https://github.com/calesthio/OpenMontage) 之 Windows 11 原生維護 Fork。**
> 
> 英文原版說明請參見 [README.en.md](README.en.md)，簡體中文說明請見 [README_zh-CN.md](README_zh-CN.md)。
> Fork 維護規範、架構與治理原則請見 [FORK.md](FORK.md)。
> 本 repo 遵循 **GNU Affero General Public License v3.0 (AGPL-3.0)** 授權條款。

---

## 專案亮點

OpenMontage 是全球首款開源、代理人導向（Agentic）的 AI 全自動影片製作系統。擁有 12 條端到端製片流水線、100+ 製片工具與 700+ Agent 技能與影視知識庫，讓你的 AI 助手變身為專業電影級製片工作室。

- **丟入參考影片，自動拆解復刻**：貼上社群短影音網址，系統自動拆解節奏腳本、運鏡語言與色彩風格，並生成多個不同創意的改編方向供選擇。
- **視覺化故事板（Backlot）**：內建即時雙向連動的故事板，在進行昂貴的視訊渲染前，先以視覺化卡片審核每鏡畫面、台詞與時長。
- **Remotion 高清合成**：深度整合 Remotion（React-based 程式化動態影像），完成圖表動畫、字幕、字卡與多軌音效之毫秒級無損合成。
- **100% 本機離線生成**：支援本機顯卡執行 Ollama、ComfyUI、Stable Diffusion / Flux 與 Piper TTS，完全無需將商業敏感素材上傳至雲端。
- **雲端百家爭鳴接入**：無縫支援 OpenAI（Sora 2）、Google（Veo 2 / Lyria / Imagen 3）、Kling、Runway、Luma、Minimax、ElevenLabs 等頂尖模型。

---

## 系統架構一覽

```text
[ 創意輸入 / 參考影音網址 ]
            │
            ▼
┌───────────────────────────────── 12 條影片流水線 ─────────────────────────────────┐
│ • 故事短片 (Narrative Short)      • 產品發佈 (Product Reveal)     • 知識解說 (Explainer) │
│ • 概念預告 (Cinematic Teaser)     • 動態標誌 (Motion Logo)        • 復古放映 (Silent Era)│
│ • 水墨劇場 (Ink Theater)         • 播客精華 (Podcast Visualizer) • 社群短影 (Social)   │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │
                                         ▼
┌────────────────── 視覺化故事板 Backlot (FastAPI + WebSocket) ───────────────────┐
│ • 鏡頭分鏡表 (Shot List)   • 旁白腳本 (Voiceover)   • 鏡頭運動與構圖 (Camera Direction) │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
┌──────────────── 本機離線引擎 ────────────────┐ ┌──────────────── 頂尖雲端 API ────────────────┐
│ • 視覺: ComfyUI / SD / Flux (本機顯卡)       │ │ • 影片: Sora 2 / Veo 2 / Kling / Runway    │
│ • 語音: Piper TTS / 本機語音模型             │ │ • 語音: ElevenLabs / Google Cloud TTS      │
│ • 推理: Ollama (本機大語言模型)              │ │ • 視覺: Imagen 3 / DALL-E 3 / Fal.ai       │
└──────────────────────┬───────────────────────┘ └──────────────────────┬───────────────────────┘
                       │                                         │
                       └────────────────────┬────────────────────┘
                                            ▼
┌────────────────────── Remotion Composer (React + Node.js) ───────────────────────┐
│ • 程式化動態圖表與文字合成       • 多音軌自動對齊與淡入淡出     • 高清 MP4/ProRes 導出   │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## Windows 11 原生快速上手

本 fork 針對 Windows 11 原生 PowerShell 環境進行完整硬化與相容性測試。

### 1. 一鍵環境建置（Bootstrap）

在專案目錄下啟動 PowerShell：

```powershell
pwsh -NoProfile -File tools\bootstrap_dev.ps1
```

> **提示**：若需要一併安裝全部 Python 產品依賴，請加上 `-All` 參數：
> ```powershell
> pwsh -NoProfile -File tools\bootstrap_dev.ps1 -All
> ```

### 2. Windows 驗收門禁（Canonical Gate）

提交任何改動前，必須在本機通過門禁檢查：

```powershell
pwsh -NoProfile -File tools\dev_check.ps1
```

門禁將自動執行 Python 編譯檢查、Ruff 語法分析、維護契約測試（pytest）與 14 份維護文件的相對連結驗證。

### 3. 產品基本功能測試

```powershell
pwsh -NoProfile -File tools\test_product.ps1
```

---

## 核心管線一覽

| 管線名稱 | 核心風格與應用場景 | 推薦模型組合 |
|---|---|---|
| `narrative-short` | 具備完整三幕劇架構的微電影、情境劇 | Claude / GPT-4o + Sora / Kling + ElevenLabs |
| `product-reveal` | 3D 質感、科技感十足的產品發布展示 | Remotion + HyperFrames + Flux |
| `explainer-video` | 知識科普、教學圖表、資訊可視化 | Remotion Charts + Piper TTS / Google TTS |
| `ink-theater` | 東方水墨意境、國風山水流體視覺 | ComfyUI ControlNet + Kling |
| `social-cutdown` | 垂直 9:16 短影音、社群快節奏卡點成片 | Remotion + Auto Subtitle + Fast Motion |

---

## 授權與貢獻規範

- 本專案採用 **GNU Affero General Public License v3.0 (AGPL-3.0)** 授權。詳見 [LICENSE](LICENSE) 與 [NOTICE.md](NOTICE.md)。
- 治理與維護決策請見 [docs/DECISIONS.md](docs/DECISIONS.md)。
- 開發指引請見 [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)。
- 上游同步紀錄與水位請見 [docs/UPSTREAM.md](docs/UPSTREAM.md)。
- 貢獻指南請見 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 安全回報請見 [SECURITY.md](SECURITY.md)。