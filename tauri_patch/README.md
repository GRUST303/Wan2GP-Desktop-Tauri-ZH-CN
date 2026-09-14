# Wan2GP Desktop Tauri 简体中文双语补丁

面向 **GKartist75/Wan2GP-Desktop-Tauri** 的独立 UI 本地化层：**中文优先，同时保留关键英文技术参数**。

当前基准：upstream **v0.6.5**, commit `3ccb16f872994e0034fbee852e58593d80ba3014`（2026-09-13）。

> 该目录不复制、不再发布上游源代码或二进制文件，只提供独立翻译层与应用脚本。

## 使用方法

```powershell
git clone https://github.com/GKartist75/Wan2GP-Desktop-Tauri.git
git clone https://github.com/GRUST303/Wan2GP-Desktop-Tauri-ZH-CN.git
cd Wan2GP-Desktop-Tauri-ZH-CN
powershell -ExecutionPolicy Bypass -File .\tauri_patch\scripts\apply-localization.ps1 -UpstreamPath D:\AI\Wan2GP-Desktop-Tauri
```

开发模式查看：

```powershell
cd D:\AI\Wan2GP-Desktop-Tauri
npm ci
npm run tauri dev
```

构建 Windows 安装包：

```powershell
powershell -ExecutionPolicy Bypass -File .\tauri_patch\scripts\build-windows.ps1 -UpstreamPath D:\AI\Wan2GP-Desktop-Tauri
```

回滚：

```powershell
powershell -ExecutionPolicy Bypass -File .\tauri_patch\scripts\revert-localization.ps1 -UpstreamPath D:\AI\Wan2GP-Desktop-Tauri
```

## 说明

WanGP 插件与 Tauri Launcher 外层窗口属于两个不同界面：

- 根目录 `plugin.py`：通过 WanGP Plugins → GitHub URL 安装，汉化 WanGP / Gradio 主界面；
- 本目录 `tauri_patch/`：手动应用到 GKartist75/Wan2GP-Desktop-Tauri 源码，汉化 Dashboard / Manage / Auto-Tune 等外层 Launcher UI。
