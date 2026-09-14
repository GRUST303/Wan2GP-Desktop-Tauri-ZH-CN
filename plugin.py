import json
from shared.utils.plugins import WAN2GPPlugin


EXACT_TRANSLATIONS = {
    # Core navigation / common actions
    "Media Generator": "媒体生成器",
    "Video": "视频",
    "Image": "图片",
    "Audio": "音频",
    "TTS": "语音合成 (TTS)",
    "Models": "模型",
    "Model": "模型",
    "Plugins": "插件",
    "Plugin Manager": "插件管理器",
    "Configuration": "配置",
    "Settings": "设置",
    "General": "常规",
    "Advanced": "高级",
    "Basic": "基础",
    "About": "关于",
    "Queue": "队列",
    "Gallery": "图库",
    "Downloads": "下载",
    "Generate": "生成",
    "Start": "开始",
    "Stop": "停止",
    "Pause": "暂停",
    "Resume": "继续",
    "Cancel": "取消",
    "Close": "关闭",
    "Clear": "清空",
    "Reset": "重置",
    "Refresh": "刷新",
    "Reload": "重新加载",
    "Save": "保存",
    "Save As": "另存为",
    "Load": "加载",
    "Browse": "浏览",
    "Upload": "上传",
    "Download": "下载",
    "Install": "安装",
    "Uninstall": "卸载",
    "Update": "更新",
    "Enable": "启用",
    "Disable": "禁用",
    "Enabled": "已启用",
    "Disabled": "已禁用",
    "Apply": "应用",
    "Confirm": "确认",
    "Delete": "删除",
    "Remove": "移除",
    "Add": "添加",
    "Edit": "编辑",
    "Copy": "复制",
    "Paste": "粘贴",
    "Open": "打开",
    "Search": "搜索",
    "Filter": "筛选",
    "Sort": "排序",
    "Name": "名称",
    "Description": "说明",
    "Version": "版本",
    "Author": "作者",
    "Status": "状态",
    "Date": "日期",
    "Type": "类型",
    "None": "无",
    "Default": "默认",
    "Auto": "自动 (Auto)",
    "Automatic": "自动",
    "Custom": "自定义",
    "Recommended": "推荐",
    "Optional": "可选",
    "Required": "必需",
    "Experimental": "实验性",
    "Loading...": "正在加载…",
    "Downloading...": "正在下载…",
    "Generating...": "正在生成…",
    "Processing...": "正在处理…",
    "Ready": "就绪",
    "Failed": "失败",
    "Success": "成功",
    "Error": "错误",
    "Warning": "警告",

    # Generation / prompting
    "Prompt": "提示词 (Prompt)",
    "Negative Prompt": "负面提示词 (Negative Prompt)",
    "Prompt Enhancer": "提示词增强器 (Prompt Enhancer)",
    "Enhance Prompt": "增强提示词 (Enhance Prompt)",
    "Generation Settings": "生成设置",
    "Model Settings": "模型设置",
    "Input": "输入",
    "Output": "输出",
    "Input Image": "输入图片 (Input Image)",
    "Start Image": "起始图片 (Start Image)",
    "End Image": "结束图片 (End Image)",
    "Reference Image": "参考图片 (Reference Image)",
    "Reference Images": "参考图片 (Reference Images)",
    "Reference Video": "参考视频 (Reference Video)",
    "Reference Audio": "参考音频 (Reference Audio)",
    "Source Image": "源图片 (Source Image)",
    "Source Video": "源视频 (Source Video)",
    "Mask": "蒙版 (Mask)",
    "Seed": "随机种子 (Seed)",
    "Random Seed": "随机种子 (Random Seed)",
    "Steps": "采样步数 (Steps)",
    "Guidance": "引导强度 (Guidance)",
    "Guidance Scale": "引导强度 (Guidance Scale)",
    "CFG Scale": "CFG 强度 (CFG Scale)",
    "Flow Shift": "Flow Shift（流偏移）",
    "Sampler": "采样器 (Sampler)",
    "Scheduler": "调度器 (Scheduler)",
    "Batch Size": "批量大小 (Batch Size)",
    "Batch Count": "批次数量 (Batch Count)",
    "Width": "宽度 (Width)",
    "Height": "高度 (Height)",
    "Resolution": "分辨率 (Resolution)",
    "Aspect Ratio": "宽高比 (Aspect Ratio)",
    "Duration": "时长 (Duration)",
    "Frames": "帧数 (Frames)",
    "Frame Count": "帧数 (Frame Count)",
    "FPS": "帧率 (FPS)",
    "Frame Rate": "帧率 (Frame Rate)",
    "Quality": "质量",
    "High Quality": "高质量",
    "Fast": "快速",
    "Speed": "速度",
    "Strength": "强度 (Strength)",
    "Denoise Strength": "降噪强度 (Denoise Strength)",
    "Motion Strength": "运动强度 (Motion Strength)",
    "Camera Motion": "镜头运动 (Camera Motion)",
    "Sliding Window": "滑动窗口 (Sliding Window)",
    "Context Length": "上下文长度 (Context Length)",
    "Overlap": "重叠量 (Overlap)",

    # Video / image post processing
    "Post Processing": "后处理 (Post Processing)",
    "Post-processing": "后处理 (Post-processing)",
    "Upscale": "超分辨率 (Upscale)",
    "Upscaler": "超分模型 (Upscaler)",
    "Interpolation": "补帧 (Interpolation)",
    "Frame Interpolation": "视频补帧 (Frame Interpolation)",
    "Face Refiner": "人脸精修 (Face Refiner)",
    "Face Restore": "人脸修复 (Face Restore)",
    "Background Removal": "背景移除 (Background Removal)",
    "Color Match": "颜色匹配 (Color Match)",
    "Sharpen": "锐化 (Sharpen)",

    # Memory / performance / technical settings
    "Performance": "性能",
    "Memory": "内存",
    "Memory Profile": "内存配置 (Memory Profile)",
    "Video Profile": "视频内存配置 (Video Profile)",
    "Image Profile": "图片内存配置 (Image Profile)",
    "Audio Profile": "音频内存配置 (Audio Profile)",
    "VRAM": "显存 (VRAM)",
    "RAM": "内存 (RAM)",
    "CPU": "处理器 (CPU)",
    "GPU": "显卡 (GPU)",
    "CUDA": "CUDA",
    "Attention": "注意力机制 (Attention)",
    "Attention Mode": "注意力模式 (Attention Mode)",
    "Sage Attention": "Sage Attention",
    "Flash Attention": "Flash Attention",
    "Sparse Attention": "Sparse Attention",
    "Transformer": "Transformer",
    "Transformer Quantization": "Transformer 量化 (Transformer Quantization)",
    "Transformer Quant": "Transformer 量化 (Transformer Quant)",
    "Quantization": "量化 (Quantization)",
    "INT8": "INT8",
    "FP8": "FP8",
    "BF16": "BF16",
    "FP16": "FP16",
    "GGUF": "GGUF",
    "VAE": "VAE",
    "VAE Config": "VAE 配置 (VAE Config)",
    "VAE Tiling": "VAE 分块 (VAE Tiling)",
    "Text Encoder": "文本编码器 (Text Encoder)",
    "CPU Offload": "CPU 卸载 (CPU Offload)",
    "Model Offload": "模型卸载 (Model Offload)",
    "Low VRAM": "低显存模式 (Low VRAM)",
    "VRAM Safety Coeff": "显存安全系数 (VRAM Safety Coeff)",
    "VRAM Safety Coefficient": "显存安全系数 (VRAM Safety Coefficient)",
    "Reserved VRAM": "预留显存 (Reserved VRAM)",
    "Triton": "Triton",
    "Nunchaku": "Nunchaku",
    "Torch": "PyTorch (Torch)",
    "PyTorch": "PyTorch",
    "Diffusers": "Diffusers",
    "Device": "设备 (Device)",
    "GPU Device": "GPU 设备 (GPU Device)",

    # Model / addon management
    "LoRA": "LoRA",
    "LoRAs": "LoRA",
    "Finetune": "微调模型 (Finetune)",
    "Finetunes": "微调模型 (Finetunes)",
    "Checkpoint": "模型权重 (Checkpoint)",
    "Checkpoints": "模型权重 (Checkpoints)",
    "Model Type": "模型类型 (Model Type)",
    "Model Family": "模型家族 (Model Family)",
    "Refresh Models": "刷新模型",
    "Download Model": "下载模型",
    "Model Manager": "模型管理器 (Model Manager)",
    "Models Manager": "模型管理器 (Models Manager)",

    # Queue / files
    "Output Folder": "输出目录 (Output Folder)",
    "Output Directory": "输出目录 (Output Directory)",
    "File Name": "文件名 (File Name)",
    "Task": "任务",
    "Progress": "进度",
    "Pending": "等待中",
    "Running": "运行中",
    "Completed": "已完成",
    "Cancelled": "已取消",
    "Retry": "重试",
    "Clear Queue": "清空队列",

    # Audio / speech
    "Enable Audio": "启用音频 (Enable Audio)",
    "Audio Prompt": "音频提示词 (Audio Prompt)",
    "Voice": "声音 (Voice)",
    "Voice Reference": "声音参考 (Voice Reference)",
    "Speech": "语音",
    "Music": "音乐",
    "Sound Effects": "音效 (Sound Effects)",

    # Plugin UI
    "Community Plugins": "社区插件 (Community Plugins)",
    "Installed Plugins": "已安装插件 (Installed Plugins)",
    "Install Plugin": "安装插件 (Install Plugin)",
    "Enable Plugin": "启用插件 (Enable Plugin)",
    "Disable Plugin": "禁用插件 (Disable Plugin)",
    "Update Plugin": "更新插件 (Update Plugin)",
    "Restart Required": "需要重启 (Restart Required)",
    "Please restart WanGP": "请重启 WanGP",
}

ATTRIBUTE_TRANSLATIONS = {
    "Enter prompt": "输入提示词 (Prompt)",
    "Enter prompt...": "输入提示词 (Prompt)…",
    "Negative prompt": "负面提示词 (Negative Prompt)",
    "Search...": "搜索…",
    "Search plugins...": "搜索插件…",
    "Select model": "选择模型",
    "Select a model": "选择模型",
    "Choose file": "选择文件",
}


class WanGPChineseBilingualPlugin(WAN2GPPlugin):
    """Simplified Chinese UI localization that preserves English technical terms."""

    def __init__(self):
        super().__init__()
        self.name = "WanGP 简体中文双语汉化"
        self.version = "0.1.0"
        self.description = "简体中文 UI 本地化；保留 VRAM/CUDA/VAE/INT8/Steps/Guidance 等英文技术术语。"
        self.type = ["extension"]

    def setup_ui(self):
        exact_json = json.dumps(EXACT_TRANSLATIONS, ensure_ascii=False)
        attr_json = json.dumps(ATTRIBUTE_TRANSLATIONS, ensure_ascii=False)
        self.add_custom_js(self._build_js(exact_json, attr_json))

    @staticmethod
    def _build_js(exact_json: str, attr_json: str) -> str:
        template = r'''(function () {
  "use strict";

  const PLUGIN_ID = "wangp-zh-cn-bilingual";
  const STORAGE_KEY = "wangp_zh_cn_enabled";
  const EXACT = __EXACT__;
  const ATTR = __ATTR__;
  const DEBUG = false;

  if (window.__wangpZhCnBilingualLoaded) return;
  window.__wangpZhCnBilingualLoaded = true;

  function enabled() {
    return localStorage.getItem(STORAGE_KEY) !== "0";
  }

  function normaliseText(s) {
    return (s || "").replace(/\s+/g, " ").trim();
  }

  function translateTextNode(node) {
    if (!enabled() || !node || node.nodeType !== Node.TEXT_NODE) return;
    const raw = node.nodeValue;
    const trimmed = normaliseText(raw);
    if (!trimmed || !EXACT[trimmed]) return;

    const leading = raw.match(/^\s*/)?.[0] || "";
    const trailing = raw.match(/\s*$/)?.[0] || "";
    node.nodeValue = leading + EXACT[trimmed] + trailing;
  }

  function translateAttributes(el) {
    if (!enabled() || !el || el.nodeType !== Node.ELEMENT_NODE) return;
    for (const attr of ["placeholder", "title", "aria-label"]) {
      const value = el.getAttribute && el.getAttribute(attr);
      if (!value) continue;
      const key = normaliseText(value);
      if (ATTR[key]) el.setAttribute(attr, ATTR[key]);
      else if (EXACT[key]) el.setAttribute(attr, EXACT[key]);
    }
  }

  function shouldSkip(el) {
    if (!el || el.nodeType !== Node.ELEMENT_NODE) return false;
    const tag = el.tagName;
    if (["SCRIPT", "STYLE", "TEXTAREA", "CODE", "PRE"].includes(tag)) return true;
    if (el.closest && el.closest("#wangp-zh-cn-toggle")) return true;
    return false;
  }

  function translateTree(root) {
    if (!enabled() || !root) return;
    if (root.nodeType === Node.TEXT_NODE) {
      translateTextNode(root);
      return;
    }
    if (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_NODE && root.nodeType !== Node.DOCUMENT_FRAGMENT_NODE) return;
    if (root.nodeType === Node.ELEMENT_NODE && shouldSkip(root)) return;

    if (root.nodeType === Node.ELEMENT_NODE) translateAttributes(root);

    const walker = document.createTreeWalker(
      root,
      NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT,
      {
        acceptNode(node) {
          if (node.nodeType === Node.ELEMENT_NODE && shouldSkip(node)) return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );

    let node;
    while ((node = walker.nextNode())) {
      if (node.nodeType === Node.TEXT_NODE) translateTextNode(node);
      else translateAttributes(node);
    }
  }

  let queued = false;
  const pendingRoots = new Set();
  function schedule(root) {
    if (!enabled()) return;
    if (root) pendingRoots.add(root);
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      const roots = Array.from(pendingRoots);
      pendingRoots.clear();
      if (!roots.length) roots.push(document.body);
      for (const r of roots) {
        try { translateTree(r); } catch (e) { if (DEBUG) console.warn("[WanGP ZH-CN]", e); }
      }
    });
  }

  function addToggle() {
    if (document.getElementById("wangp-zh-cn-toggle")) return;
    const btn = document.createElement("button");
    btn.id = "wangp-zh-cn-toggle";
    btn.type = "button";
    btn.textContent = enabled() ? "中 / EN" : "中文";
    btn.title = enabled() ? "切换到英文界面 (Switch to English)" : "启用简体中文 (Enable Chinese)";
    btn.setAttribute("aria-label", btn.title);
    btn.style.cssText = [
      "position:fixed",
      "right:12px",
      "bottom:12px",
      "z-index:2147483647",
      "padding:7px 11px",
      "border-radius:8px",
      "border:1px solid rgba(127,127,127,.45)",
      "background:rgba(24,24,27,.92)",
      "color:#fff",
      "font-size:12px",
      "font-weight:600",
      "cursor:pointer",
      "box-shadow:0 4px 16px rgba(0,0,0,.28)",
      "backdrop-filter:blur(8px)"
    ].join(";");
    btn.addEventListener("click", () => {
      localStorage.setItem(STORAGE_KEY, enabled() ? "0" : "1");
      location.reload();
    });
    document.body.appendChild(btn);
  }

  function boot() {
    addToggle();
    if (enabled()) translateTree(document.body);

    const observer = new MutationObserver((mutations) => {
      if (!enabled()) return;
      for (const m of mutations) {
        if (m.type === "characterData") schedule(m.target);
        for (const n of m.addedNodes || []) schedule(n);
        if (m.type === "attributes") schedule(m.target);
      }
    });
    observer.observe(document.documentElement, {
      subtree: true,
      childList: true,
      characterData: true,
      attributes: true,
      attributeFilter: ["placeholder", "title", "aria-label"]
    });

    setTimeout(() => schedule(document.body), 800);
    setTimeout(() => schedule(document.body), 2500);
    console.info("[WanGP ZH-CN] bilingual localization active");
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot, { once: true });
  else boot();
})();'''
        return template.replace("__EXACT__", exact_json).replace("__ATTR__", attr_json)
