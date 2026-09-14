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

## v0.4.0：下拉框已选值 + 更可靠的“未译”扫描

页面右下角仍显示：

```text
中文 | 中英 | EN | 未译
```

- `中文`：纯中文模式。
- `中英`：中文 + 英文技术术语模式，也是推荐模式。
- `EN`：原始英文，不执行翻译。
- `未译`：扫描当前**真正可见**的页面，并把残留分成 `UI 文本` 与 `文档 / 长说明` 两组。

### 为什么下拉框以前“展开有中文、收起又变英文”？

Gradio 的很多 Dropdown / ComboBox 实际上有两套显示层：

1. 展开的候选列表是普通文本节点，所以之前已经能被翻译；
2. 收起后的当前选中值通常放在独立的 `input/combobox` value 中，不属于普通文本节点。

v0.4.0 增加了对 combobox 当前显示值的单独本地化。插件只改**显示值**，不会改下拉框对应的真实配置值；当用户打开下拉框进行搜索/选择时，会临时恢复原始英文值，关闭后再显示中文或中英版本，尽量避免影响 Gradio 的选择逻辑。

### “2599 条未译”为什么会这么多？

旧扫描器会把隐藏 Tab、折叠区域、帮助文档、Guides 长文章甚至部分内部字符串一起算进去，因此数量远大于当前屏幕上真正需要翻译的 UI。

v0.4.0 现在会过滤：

- 隐藏 Tab / `display:none`
- `aria-hidden` / `hidden` / `inert`
- 没有可见布局区域的元素
- 当前不可见 iframe
- 明显路径、文件名、命令参数、内部 snake_case 标识和连接词

并把结果拆成：

- **UI 文本**：优先处理，按钮、标签、选项、当前下拉值等；
- **文档 / 长说明**：Guides、帮助文章、长解释单独处理。

以后反馈时优先复制 `UI 文本` 就够了，通常会比旧版的几千条小很多。

## 翻译覆盖

当前重点覆盖：

- Media Generator / MiniMax H3 常用生成参数
- Mask Generator / MatAnyone
- Motion Designer（含同源 iframe）
- Guides / Model Overview
- Configuration → General
- Configuration → Performance
- Configuration → Extensions
- Configuration → Prompt Enhancer / Deepy
- Model / Finetune / LoRA / Queue / Audio / Postprocessing
- VRAM / RAM / Quantization / Attention / VAE / Text Encoder 等公共技术字段

v0.4.0 新增了大量实际页面残留词条，并继续采用“安全精确匹配优先”的策略；模型名、文件名和用户输入不会被机械翻译。

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
locales/zh_CN_v4.json
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

- Plugin：`0.4.0`
- 适配基线：WanGP `13.0`
- 发布日期：2026-09-14

## License

本仓库原创的本地化插件、翻译表、脚本和文档采用 MIT License。上游 WanGP 与 Tauri Launcher 的版权和许可证归各自作者所有。
