# WanGP 简体中文 / 双语界面

面向 **WanGP / Wan2GP v13** 的第三方简体中文本地化插件。

> **非官方项目 / Unofficial community localization.** 上游：<https://github.com/deepbeepmeep/Wan2GP>

## 安装 / 更新

在 WanGP 中打开 **Plugins / Plugin Manager**，从 GitHub URL 安装：

```text
https://github.com/GRUST303/Wan2GP-Desktop-Tauri-ZH-CN
```

安装或更新后请**完全重启 WanGP**；浏览器仍缓存旧前端时再按 `Ctrl + F5`。

## 三种显示模式

右下角提供：

```text
中文 | 中英 | EN | 未译
```

- **中文**：尽量只显示中文；模型名、CUDA、VRAM、VAE、INT8、LoRA 等必要技术名保留。
- **中英**：中文优先，同时保留英文技术字段，方便对照教程和 GitHub Issue。
- **EN**：恢复 WanGP 原始英文界面。

## v0.5.0：动态说明 + 按栏目持久累计的“未译”采集

### 模型切换后的说明

v0.5 增加三层翻译机制：

1. 精确词条；
2. 正则动态词条；
3. 安全的短语片段替换。

切换模型 / finetune 后会在多个时间点重新扫描，因此 MiniMax H3 等模型稍后刷新的描述文字也能被本地化。

### Prompt “深入了解” / 帮助弹窗

动态 `dialog` / help UI 现在同样受监听。`Prompt Help`、`Prompts Guide`、宏、注释、空行拆分规则等已加入 v0.5 词库。

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

建议先不开“文档 / 长说明”，在各栏目和模型里快速点一遍；最后点 **复制累计**，即可一次把按栏目分组的残留发到 GitHub Issue。

## 下拉框安全策略

Gradio Dropdown 展开候选项和收起后的选中值并不是同一层 DOM。插件会：

- 展开 / 搜索时恢复真实英文值，避免破坏 Gradio 匹配；
- 收起后只改变显示值；
- `change` 后延迟多次重扫，以覆盖模型切换带来的动态 UI。

不会修改真实生成参数值。

## 翻译覆盖

目前重点覆盖：

- Media Generator / MiniMax H3
- 动态模型说明与 Prompt Help 弹窗
- Mask Generator / MatAnyone
- Motion Designer（含同源 iframe）
- Guides / Model Overview / Prompts / Processing
- Configuration → General / Performance / Extensions / Prompt Enhancer / Deepy
- Model / Finetune / LoRA / Queue / Audio / Postprocessing
- VRAM / RAM / Quantization / Attention / VAE / Text Encoder 等公共技术字段

词库：

```text
locales/zh_CN.json
locales/zh_CN_v3.json
locales/zh_CN_v4.json
locales/zh_CN_v5.json
```

前端逻辑从 v0.5 起位于：

```text
web/localization.js
```

## 安全边界

插件仅通过 WanGP 插件 API 注入本地化 JavaScript，不修改模型权重、Prompt 内容、CUDA / PyTorch / Triton、`wgp_config.json` 参数值、下载源或 WanGP 核心 Python 文件。

## Tauri Launcher

WanGP 插件只能汉化 WanGP / Gradio 主界面。GKArtist 的 **Wan2GP Desktop Tauri Launcher** 是独立 WebView，补丁保留在：

```text
tauri_patch/
```

## 当前版本

- Plugin：`0.5.0`
- 适配基线：WanGP `13.0`
- 发布日期：2026-09-14

## License

本仓库原创的本地化插件、翻译表、脚本和文档采用 MIT License。上游项目版权与许可证归各自作者所有。
