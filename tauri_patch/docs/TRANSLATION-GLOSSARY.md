# 翻译规范 / Translation glossary

本项目采用“中文优先 + 英文技术参数保留”的方式，避免中文用户看不懂，同时也避免照英文教程时找不到参数。

| Upstream term | 中文显示 | 说明 |
|---|---|---|
| Auto-Tune | 自动优化 (Auto-Tune) | 保留官方功能名 |
| Video Profile | 视频配置 (Video Profile) | Profile 数字仍保持原值 |
| Image Profile | 图片配置 (Image Profile) | 同上 |
| Audio Profile | 音频配置 (Audio Profile) | 同上 |
| VRAM Safety Coeff | 显存安全系数 (VRAM Safety Coeff) | VRAM 保留英文缩写 |
| VAE Config | VAE 配置 (VAE Config) | VAE 不翻译 |
| Transformer Quant | Transformer 量化 (Transformer Quant) | INT8 / FP8 / NVFP4 保持英文 |
| Int8 Kernels | INT8 内核 (Int8 Kernels) | Triton 保持英文 |
| Failsafe P5 | 故障保护 P5 (Failsafe P5) | P1–P5 档位不翻译 |
| Checkpoints | 模型检查点 (Checkpoints) | 路径名不改 |
| LoRAs | LoRA 模型 (LoRAs) | LoRA 不翻译 |
| No-GPU | No-GPU | 避免误解为“生成不用 GPU” |
| GGUF / CUDA / Triton / SageAttention / FlashAttention | 原样保留 | 标准技术名 |

## 原则

1. 模型名、库名、命令行参数、文件名和 JSON key 不翻译。
2. 对性能/显存相关设置使用“中文说明 + 英文官方名”。
3. 错误信息如无法安全匹配则保持英文，方便搜索 GitHub issue。
4. 翻译层只修改显示文字，不修改任何 Wan2GP 配置值或业务逻辑。
