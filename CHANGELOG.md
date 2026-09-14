# Changelog

## 0.2.0 - 2026-09-14

- 针对 WanGP v13.0 主界面补充大量实际 UI 文案翻译。
- 覆盖 `Mask Generator`、`Motion Designer`、`Guides`、`Text to Video`、`New Video`、图库、分辨率预算、Prompt 帮助等当前生成页常见文本。
- 新增正则翻译，支持 `Attention mode ... Data Type ...`、动态帧数/时长等运行时文本。
- 新增 Shadow DOM 扫描与监听，提升 Gradio 动态挂载组件的翻译覆盖率。
- 翻译词库拆分到 `locales/zh_CN.json`，方便社区提交词条和后续维护。
- 继续跳过 Prompt 文本框、代码块和可编辑内容，避免误改用户输入。

## 0.1.0 - 2026-09-14

- 首个可通过 WanGP Plugins → GitHub URL 安装的版本。
- 新增 `plugin_info.json` 与标准 `extension` 插件入口 `plugin.py`。
- 中文优先、英文技术参数保留。
- 使用精确文本匹配 + MutationObserver 处理 Gradio 动态 UI。
- 右下角提供 `中 / EN` 开关，状态保存在浏览器 localStorage。
- 初始覆盖生成、模型、LoRA、队列、音频、后处理、显存/量化/Attention 等常见术语。
