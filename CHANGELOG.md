# Changelog

## 0.6.0 - 2026-09-15

- 新增 `locales/zh_CN_v6.json`，根据实际“未译累计报告”继续补 MiniMax H3 常用界面。
- 重点汉化 H3 长视频 / Sliding Window：窗口大小、窗口重叠、自动启用说明、按行 / 按段落分配滑动窗口等。
- 补充 `An H3 Prompt from Text`、`An H3 Prompt from Text + Start Image`、H3 FL2VA Prompt Structure 等写作增强与帮助文本。
- 补充 H3 Prompt Help 中的镜头连接、硬切、首尾帧、duration / overlap 说明及跨镜头一致性提示。
- 补充 Attention、Memory Profile、DLSS、SeedVR2、VAE、Denoising、生成进度等动态 UI 文本。
- 补充 Add workspace、Extract Settings、Extend this Sample、To Control Video、To Video Source 等高频操作。
- README 增加 WanGP 中文 / WanGP 汉化 / Wan2GP 中文 / MiniMax H3 中文等中英文检索词，并补充 GitHub Topics 建议，改善仓库发现性。
- 插件版本更新为 `0.6.0`。

## 0.5.0 - 2026-09-14

- 重构前端注入：把大型 JavaScript 从 `plugin.py` 拆到 `web/localization.js`，后续维护和 CI 检查更简单。
- 新增 `locales/zh_CN_v5.json`，补充 MiniMax H3 动态模型说明、Prompt 帮助弹窗、Configuration / Guides / Queue / Mask / Audio / Postprocessing 等实际残留词条。
- 动态模型说明支持“精确词条 + 正则 + 安全短语片段”三级翻译，切换模型后会多次延迟重扫，解决模型说明稍后刷新导致仍显示英文的问题。
- 帮助 / Learn More / Prompt Help 等动态弹窗纳入 MutationObserver 与弹窗扫描，长说明也可按词库和短语片段翻译。
- `未译` 扫描器升级为持久累计模式：按 `主栏目 / 子栏目 / 当前模型 / 弹窗` 自动分组，切换页面和模型后不会清空。
- 未译面板新增 `扫描当前并累计`、`复制当前`、`复制累计`、`导出累计 .txt`、`清空累计`。
- 新增 `包含文档 / 长说明` 开关；默认优先收集 UI 文本，避免再次出现几千条文档噪声。
- 新增 `自动累计` 开关：开启后切换栏目、模型、Tab 或动态 UI 后会节流扫描并写入浏览器 `localStorage`。
- 继续优化 Gradio Dropdown：展开时保留真实英文值以保障搜索/选择，收起后自动恢复中文/中英显示，并在模型切换后立即重扫。

## 0.4.0 - 2026-09-14

- 修复 Gradio 下拉框“展开后选项已汉化，但收起后当前选中值仍显示英文”的问题：现在会单独处理 combobox 的已选显示值，同时避免修改真实配置值。
- 下拉框在交互/搜索时会临时恢复原始英文值，关闭后再显示对应中文或中英双语，尽量兼顾本地化与 Gradio 组件稳定性。
- 重做 `未译` 扫描器：只统计当前**真正可见**的界面，隐藏 Tab、`display:none`、`aria-hidden`、折叠内容和不可见 iframe 不再大量误报。
- `未译` 面板拆分为 `UI 文本` 与 `文档 / 长说明` 两组，便于优先补真正影响操作的界面文本。
- 未译扫描同时检查当前可见 combobox 的选中值，因此下拉框残留英文也能直接收集。
- 新增 `locales/zh_CN_v4.json`，根据实际未译文本批量补充 Configuration、Deepy、LoRA、Mask、Queue、Audio、Postprocessing、Finetune 等常见 UI 字段。
- 增加未译扫描噪声过滤，跳过明显的路径、文件名、内部 snake_case 标识、命令参数和过短连接词。

## 0.3.0 - 2026-09-14

- 新增三档界面模式：`中文`、`中英`、`EN`。
- 新增同源 iframe 翻译与监听，重点修复 Motion Designer。
- 新增 `未译` 扫描器。
- 大幅补充 MiniMax H3、Mask Generator、Motion Designer、Guides、Configuration 常用文案。

## 0.2.0 - 2026-09-14

- 针对 WanGP v13.0 主界面补充大量实际 UI 文案翻译。
- 新增正则翻译和 Shadow DOM 监听。

## 0.1.0 - 2026-09-14

- 首个可通过 WanGP Plugins → GitHub URL 安装的版本。
- 中文优先、英文技术参数保留。