# 安全政策

## 支援範圍

安全修正以本 fork 的最新 `main` 為主；上游版本的問題也會視需要回報原作者。

## 私下回報

若發現針對本 fork 維護骨架或衍生程式的安全漏洞，請使用 GitHub Security Advisories 的 **Report a vulnerability** 私下回報：
<https://github.com/SanHsien/OpenMontage/security/advisories/new>。
若該入口不可用，請透過 GitHub 個人檔案聯絡維護者，不要先建立公開 Issue。

若問題屬於上游核心邏輯，亦可向原作者 calesthio 通報。

回報請包含影響範圍、重現步驟、受影響版本與最小必要證據。請勿在回報中附上真實 API key、token、商業機密影片素材或帳密。

## 特別注意

- **防範假冒二進位安裝檔（Issue #626 安全警示）**：OpenMontage 專案目前**僅以 Python 及 Node.js 原生原始碼**形式發布，**官方從未發布任何已編譯的二進位安裝檔（如 `.exe`、`.msi`、`.pkg`、`.dmg`）**。網路上流傳之「OpenMontage Desktop」或「OpenMontage-app」執行檔均為第三方假冒並夾帶惡意後門木馬的釣魚軟體。請務必直接自 GitHub 官方或本 fork 原始碼環境克隆並使用 `python` / `npx` 啟動，切勿下載執行來路不明的二進位檔案。
- **API 金鑰安全**：OpenMontage 支援接入 OpenAI、Google、ElevenLabs、Kling 等雲端服務，所有憑證皆透過 `.env` 管理，絕對不可提交至版本控制。
- **本機執行隔離**：使用 ComfyUI、Ollama 或本機顯卡執行時，注意本機服務埠存取控制，避免未授權網路請求。
- **檔案處理防護**：影片合成與暫存涉及多種多媒體格式處理（MP4, WAV, JSON, Remotion bundles），注意防範路徑遍歷與非預期覆寫。