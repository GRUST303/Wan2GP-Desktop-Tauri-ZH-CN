# Changelog

## 0.4.0 - 2026-09-14

- 修复 Gradio 下拉框“展开后选项已汉化，但收起后当前选中值仍显示英文”的问题：现在会单独处理 combobox 的已选显示值，同时避免修改真实配置值。
- 下拉框在交互/搜索时会临时恢复原始英文值，关闭后再显示对应中文或中英双语，尽量兼顾本地化与 Gradio 组件稳定性。
- 重做 `未译` 扫描器：只统计当前**真正可见**的界面，隐藏 Tab、`display:none`、`aria-hidden`、折叠内容和不可见 iframe 不再大量误报。
- `未译` 面板拆分为 `UI 文本` 与 `文档 / 长说明` 两组，便于优先补真正影响操作的界面文本。
- 未译扫描同时检查当前可见 combobox 的选中值，因此下拉框残留英文也能直接收集。
- 新增 `locales/zh_CN_v4.json`，根据实际未译文本批量补充 Configuration、Deepy、LoRA、Mask、Queue、Audio、Postprocessing、Finetune 等常见 UI 字段。
- 增加未译扫描噪声过滤，跳过明显的路径、文件名、内部 snake_case 标识、命令参数和过短连接词。

## 0.3.0 - 2026-09-14

- 新增三档界面模式：`中文`（纯中文）、`中英`（中文 + 英文技术术语）、`EN`（原始英文）。
- 新增右下角分段语言切换 UI，模式保存在浏览器 `localStorage`，刷新/重启后保持。
- 新增同源 `iframe` 翻译与监听，重点修复 **Motion Designer** 独立 iframe 内大量文字无法汉化的问题。
- 新增 `未译` 扫描器：自动收集当前页面仍未覆盖的英文 UI，可一键复制，用于 Issue/词库补充，不再要求逐页截图。
- 大幅补充 MiniMax H3 主生成页、Mask Generator、Motion Designer、Guides Overview、Configuration → General / Performance / Extensions / Prompt Enhancer 常用文案。
- 对 Guides 中较长的英文说明使用中文摘要式翻译，避免界面过度拥挤。
- 保留模型名、CUDA、VRAM、VAE、INT8、LoRA 等必要技术名；纯中文模式会尽量移除普通字段后的英文括注。

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
