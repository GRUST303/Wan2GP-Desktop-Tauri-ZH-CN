# WanGP 简体中文双语汉化 / Chinese Bilingual Localization

一个面向 **WanGP / Wan2GP** 的第三方简体中文本地化插件，目标是：

- 普通界面文字优先显示中文；
- **保留英文技术参数名**，例如 `VRAM`、`CUDA`、`VAE`、`INT8`、`Steps`、`Guidance Scale`、`Flow Shift`、`Sampler`、`Text Encoder`；
- 不修改模型、不修改生成逻辑、不改 `wgp_config.json`；
- 通过 WanGP 的 **Plugins → GitHub URL** 直接安装/更新；
- 对 Gradio 动态生成的 UI 使用 `MutationObserver` 持续翻译，新版 WanGP 新增且尚未收录的文本保持英文，不阻断界面。

> **非官方项目 / Unofficial community localization.** WanGP 上游：<https://github.com/deepbeepmeep/Wan2GP>

## 一键安装（推荐）

在 WanGP 中打开 **Plugins / Plugin Manager**，选择从 GitHub URL 安装，粘贴：

```text
https://github.com/GRUST303/Wan2GP-Desktop-Tauri-ZH-CN
```

安装完成后：

1. 在插件列表中启用本插件；
2. 重启 WanGP；
3. 页面右下角会出现 `中 / EN` 按钮；
4. 点击可在“中文双语 / 原始英文”之间切换。

WanGP 的远程插件安装器会直接 clone GitHub 仓库，并读取根目录 `plugin_info.json`；本仓库按 WanGP `extension` 插件格式提供 `plugin.py`。

## 翻译风格

不是把所有术语机械翻成中文，而是采用“中文解释 + 英文技术名保留”的方式。例如：

| 原文 | 显示 |
|---|---|
| `VRAM` | `显存 (VRAM)` |
| `Video Profile` | `视频内存配置 (Video Profile)` |
| `Transformer Quantization` | `Transformer 量化 (Transformer Quantization)` |
| `Guidance Scale` | `引导强度 (Guidance Scale)` |
| `Flow Shift` | `Flow Shift（流偏移）` |
| `Text Encoder` | `文本编码器 (Text Encoder)` |
| `VAE Tiling` | `VAE 分块 (VAE Tiling)` |

这样看中文更直观，同时仍能直接对照英文教程、GitHub Issue 和模型文档。

## 安全边界

插件只通过 WanGP 官方插件 API `add_custom_js()` 注入 UI 本地化脚本。它不会修改：

- 模型权重 / Checkpoint；
- Prompt 内容；
- CUDA / PyTorch / Triton 环境；
- `wgp_config.json` 的键和值；
- 下载源；
- 生成参数数值；
- WanGP 核心 Python 文件。

翻译采用**精确匹配**为主，避免误改用户 Prompt、模型名和文件名。

## 关于 Tauri Launcher

这个仓库目前首先提供的是 **WanGP 主界面的插件版汉化**，可以直接在 WanGP Plugins 中订阅。

需要特别区分：

- **WanGP / Gradio 主界面**：本插件可以汉化；
- **GKartist75/Wan2GP-Desktop-Tauri 外层 Dashboard / Manage / Auto-Tune 管理窗口**：属于另一个 Tauri WebView，WanGP 插件受同源安全限制，不能直接修改它。

Tauri Launcher 的独立汉化补丁会放在本仓库的 `tauri_patch/` 目录中，和 WanGP 插件版分开维护。

## 当前版本

- Plugin: `0.1.0`
- 初始公开版日期：2026-09-14
- WanGP：采用动态 UI 翻译层设计，未硬锁版本

## 反馈 / 贡献

遇到未翻译、翻译不准确或新版 WanGP 新增文字：请直接开 Issue，最好附截图和英文原文。

欢迎 PR 补充词条。技术名原则上保留英文，避免与英文教程脱节。

## License

本仓库原创的本地化插件、翻译表、脚本和文档采用 MIT License。上游 WanGP 与 Tauri Launcher 的版权和许可证归各自作者所有。
