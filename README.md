# WanGP 中文 / Wan2GP 汉化插件

**Simplified Chinese localization for WanGP / Wan2GP / MiniMax H3**

这是一个面向 **WanGP / Wan2GP v13** 的第三方简体中文本地化插件，目标是降低中文用户使用 WanGP、MiniMax H3、本地 AI 视频生成模型时的语言门槛。

如果你正在搜索 **WanGP 中文、WanGP 汉化、Wan2GP 中文、Wan2GP 汉化、MiniMax H3 中文界面、MiniMax H3 汉化、WanGP Chinese、WanGP Simplified Chinese、WanGP localization**，这个项目就是为这些场景准备的。

> **非官方项目 / Unofficial community localization.** 上游项目：<https://github.com/deepbeepmeep/Wan2GP>

## 安装 / 更新

在 WanGP 中打开 **Plugins / Plugin Manager**，从 GitHub URL 安装：

```text
https://github.com/GRUST303/Wan2GP-Desktop-Tauri-ZH-CN
```

安装或更新后请**完全重启 WanGP**；如果浏览器仍缓存旧前端，再按 `Ctrl + F5`。

## 功能概览

右下角提供四种入口：

```text
中文 | 中英 | EN | 未译
```

- **中文**：尽量只显示中文；模型名、CUDA、VRAM、VAE、INT8、LoRA、GGUF、Attention 等必要技术名保留。
- **中英**：中文优先，同时保留英文技术字段，方便对照教程、模型文档与 GitHub Issue。
- **EN**：恢复 WanGP 原始英文界面。
- **未译**：扫描当前页面仍未覆盖的英文 UI，并按栏目 / 模型持续累计，方便继续补翻译。

## v0.6.0：MiniMax H3 长视频 / 滑动窗口重点汉化

v0.6 根据实际使用中的未译累计报告，重点补充 MiniMax H3 长视频与高级生成界面，包括：

- `A Sliding Window allows you to generate video with a duration not limited by the Model`
- `Windows Frames Overlap`
- `All the Lines are Part of the Same Prompt`
- `Each Line Will be used for a new Sliding Window...`
- `Each Paragraph Separated by an Empty line...`
- `An H3 Prompt from Text`
- `An H3 Prompt from Text + Start Image`
- `H3 FL2VA prompt structure`
- H3 Prompt Help 中的镜头连接、滑动窗口长度、硬切、首帧 / 尾帧说明
- Attention / Memory Profile / DLSS / SeedVR2 / VAE / Denoising 等常见动态 UI 与进度文本
- Add workspace、Extract Settings、Extend this Sample、To Control Video、To Video Source 等常用操作

技术名和真实参数值仍保持原样，插件只改变可见文字，不修改 WanGP 的生成参数。

## v0.5.0：动态说明 + 按栏目持久累计的“未译”采集

### 模型切换后的说明

v0.5 增加三层翻译机制：

1. 精确词条；
2. 正则动态词条；
3. 安全的短语片段替换。

切换模型 / finetune 后会在多个时间点重新扫描，因此 MiniMax H3 等模型稍后刷新的描述文字也能被本地化。

### Prompt “深入了解” / 帮助弹窗

动态 `dialog` / help UI 同样受监听。`Prompt Help`、`Prompts Guide`、宏、注释、空行拆分规则等已经加入词库。

### “未译”不再切页清空

点击 `未译` 后，插件会按类似下面的标题累计：

```text
媒体生成器 (Media Generator) / MiniMax H3 / FL2VA Pruned 20B
配置 (Configuration) / Performance
引导工具 (Guides) / Prompts
媒体生成器 (...) / 弹窗：Prompt Help
```

扫描结果保存在浏览器 `localStorage`，**切换栏目、模型、Tab 或刷新后都不会自动清空**。

面板提供：

- `扫描当前并累计`
- `复制当前`
- `复制累计`
- `导出累计 .txt`
- `清空累计`
- `包含文档 / 长说明`
- `自动累计（切换栏目 / 模型后自动记录）`

建议先不开“文档 / 长说明”，在各栏目和模型里快速点一遍；最后点 **复制累计**，即可一次获得按栏目分组的残留文本。

## 下拉框安全策略

Gradio Dropdown 展开候选项和收起后的选中值并不是同一层 DOM。插件会：

- 展开 / 搜索时恢复真实英文值，避免破坏 Gradio 匹配；
- 收起后只改变显示值；
- `change` 后延迟多次重扫，以覆盖模型切换带来的动态 UI。

不会修改真实生成参数值。

## 翻译覆盖

目前重点覆盖：

- **Media Generator / 媒体生成器**
- **MiniMax H3 FL2VA / Ref2VA / PDD / VDN**
- **H3 Sliding Window / 长视频滑动窗口**
- **H3 Prompt Help / Prompt Enhancer / 写作增强**
- 动态模型说明与帮助弹窗
- Mask Generator / MatAnyone
- Motion Designer（含同源 iframe）
- Guides / Model Overview / Prompts / Processing
- Configuration → General / Performance / Extensions / Prompt Enhancer / Deepy
- Model / Finetune / LoRA / Queue / Audio / Postprocessing
- VRAM / RAM / Quantization / Attention / VAE / Text Encoder / GGUF 等公共技术字段

词库：

```text
locales/zh_CN.json
locales/zh_CN_v3.json
locales/zh_CN_v4.json
locales/zh_CN_v5.json
locales/zh_CN_v6.json
```

前端逻辑从 v0.5 起位于：

```text
web/localization.js
```

## 谁适合使用

这个插件主要面向：

- 使用 **WanGP / Wan2GP** 的中文用户；
- 在本地运行 **MiniMax H3**、Wan、Hunyuan Video 等视频生成模型的用户；
- 使用 RTX 30 / 40 / 50 系显卡进行本地 AI 视频生成的人；
- 想理解 Sliding Window、PDD、VDN、SeedVR2、DLSS、GGUF、Text Encoder 等设置，但不想完全依赖英文界面的人；
- 想保留英文技术名方便对照 B 站、YouTube、GitHub、Hugging Face 教程的人。

## 搜索关键词 / Search Keywords

下面这些关键词也是本项目覆盖的常见搜索叫法，方便 GitHub 与搜索引擎理解项目主题：

```text
WanGP 中文
WanGP 汉化
WanGP 中文插件
WanGP 简体中文
WanGP Chinese
WanGP Chinese localization
WanGP Simplified Chinese
Wan2GP 中文
Wan2GP 汉化
Wan2GP Chinese
MiniMax H3 中文
MiniMax H3 汉化
MiniMax H3 WanGP
MiniMax H3 Chinese UI
AI 视频生成 中文界面
local AI video generation Chinese localization
```

> README 中增加关键词可以提升 GitHub 站内搜索和搜索引擎理解项目主题的机会，但是否、何时被 Google / Bing / 百度等收录仍由各搜索引擎决定，项目本身无法强制保证即时收录。

## 建议的 GitHub Topics

如果仓库设置页面允许，建议为项目添加这些 Topics，可进一步提高 GitHub 站内发现率：

```text
wangp
wan2gp
minimax-h3
localization
i18n
chinese
simplified-chinese
translation
video-generation
gradio
ai-video
```

## 安全边界

插件仅通过 WanGP 插件 API 注入本地化 JavaScript，不修改模型权重、Prompt 内容、CUDA / PyTorch / Triton、`wgp_config.json` 参数值、下载源或 WanGP 核心 Python 文件。

## Tauri Launcher

WanGP 插件只能汉化 WanGP / Gradio 主界面。GKArtist 的 **Wan2GP Desktop Tauri Launcher** 是独立 WebView，补丁保留在：

```text
tauri_patch/
```

## 当前版本

- Plugin：`0.6.0`
- 适配基线：WanGP `13.0`
- 发布日期：2026-09-15

## License

本仓库原创的本地化插件、翻译表、脚本和文档采用 MIT License。上游项目版权与许可证归各自作者所有。