# WanGP 简体中文 / 双语界面

一个面向 **WanGP / Wan2GP v13** 的第三方简体中文本地化插件。

现在支持三种显示模式：

- **中文**：尽量只显示中文；模型名、CUDA、VRAM、VAE、INT8、LoRA 等必要技术名仍按实际名称保留。
- **中英**：中文优先，同时保留英文技术字段，方便对照教程和 GitHub Issue。
- **EN**：恢复 WanGP 原始英文界面。

> **非官方项目 / Unofficial community localization.** WanGP 上游：<https://github.com/deepbeepmeep/Wan2GP>

## 一键安装 / 更新

在 WanGP 中打开 **Plugins / Plugin Manager**，选择从 GitHub URL 安装：

```text
https://github.com/GRUST303/Wan2GP-Desktop-Tauri-ZH-CN
```

安装后启用插件并**完全重启 WanGP**。如果浏览器仍缓存旧界面，可再按 `Ctrl + F5`。

已安装旧版本时，优先在 Plugin Manager 中点 **Update**；如果没有出现更新按钮，可卸载插件后使用同一个 GitHub URL 重新安装。

## v0.3.0：三档语言切换

页面右下角会显示：

```text
中文 | 中英 | EN | 未译
```

- `中文`：纯中文模式。
- `中英`：中文 + 英文技术术语模式，也是推荐模式。
- `EN`：原始英文，不执行翻译。
- `未译`：扫描**当前已打开页面**仍未覆盖的英文 UI，并提供“一键复制”。把结果贴到 GitHub Issue 即可补词，不需要把每个页面都截图。

语言模式保存在浏览器本地，刷新或重启后会继续使用上次选择。

## 翻译覆盖

当前重点覆盖：

- Media Generator / MiniMax H3 常用生成参数
- Mask Generator / MatAnyone
- Motion Designer
- Guides / Model Overview
- Configuration → General
- Configuration → Performance
- Configuration → Extensions
- Configuration → Prompt Enhancer / Deepy 常用项
- 模型 / LoRA / 队列 / 音频 / 后处理 / VRAM / 量化 / Attention 等公共字段

### Motion Designer 为什么 v0.3 改善很大？

Motion Designer 实际运行在 WanGP 页面内部的独立同源 `iframe` 中。v0.1/v0.2 的主页面 DOM 翻译无法完整进入这个 iframe；v0.3 增加了 iframe 文档发现、`load` 监听和独立 `MutationObserver`，因此可以翻译其中的 `Scene Settings`、`Object Animation`、`Trajectory`、`Preview Mask` 等界面文本。

## 翻译风格

`中英` 模式采用“中文解释 + 英文技术名”的方式，例如：

| 原文 | 中英模式 |
|---|---|
| `VRAM` | `显存 (VRAM)` |
| `Transformer Quantization` | `Transformer 量化 (Transformer Quantization)` |
| `Guidance Scale` | `引导强度 (Guidance Scale)` |
| `Text Encoder` | `文本编码器 (Text Encoder)` |
| `VAE Tiling` | `VAE 分块 (VAE Tiling)` |

这样中文用户容易理解，也能直接对应英文教程。

## 安全边界

本插件只通过 WanGP 插件 API 注入界面本地化 JavaScript，不修改：

- 模型权重 / Checkpoint
- 用户 Prompt 内容
- CUDA / PyTorch / Triton 环境
- `wgp_config.json` 参数值
- 下载源
- 生成参数数值
- WanGP 核心 Python 文件

词库主要位于：

```text
locales/zh_CN.json
locales/zh_CN_v3.json
```

欢迎通过 PR / Issue 补充翻译。

## Tauri Launcher 与 WanGP 主界面的区别

本插件安装在 **WanGP Plugins** 中，因此主要汉化 WanGP / Gradio 主界面。

GKArtist 的 **Wan2GP Desktop Tauri Launcher** 外层 Dashboard / Manage / Auto-Tune 是另一个 WebView，WanGP 插件不能跨页面直接修改。Tauri Launcher 的独立汉化补丁放在：

```text
tauri_patch/
```

后续可以单独维护 Tauri 中文版或向上游提交 i18n PR。

## 当前版本

- Plugin：`0.3.0`
- 适配基线：WanGP `13.0`
- 发布日期：2026-09-14

## License

本仓库原创的本地化插件、翻译表、脚本和文档采用 MIT License。上游 WanGP 与 Tauri Launcher 的版权和许可证归各自作者所有。
