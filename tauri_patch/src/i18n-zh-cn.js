/**
 * Wan2GP Desktop Launcher — Simplified Chinese bilingual UI overlay
 * Target upstream: GKartist75/Wan2GP-Desktop-Tauri v0.6.5
 * Commit: 3ccb16f872994e0034fbee852e58593d80ba3014
 *
 * This file is an independent runtime translation layer. It does not include
 * upstream source code. Technical terms are intentionally kept in English.
 */
(() => {
  'use strict';

  const STORAGE_KEY = 'wan2gp.zhcn.ui';
  const MODE_BILINGUAL = 'zh-en';
  const MODE_ENGLISH = 'en';
  const currentMode = localStorage.getItem(STORAGE_KEY) || MODE_BILINGUAL;

  const exact = new Map(Object.entries({
    'Checking installation...': '正在检查安装状态… (Checking installation...)',
    'Manage': '管理 (Manage)',
    'General': '常规 (General)',
    'Launch': '启动 (Launch)',
    'System': '系统 (System)',
    '⚡ Auto-Tune': '⚡ 自动优化 (Auto-Tune)',
    '🧩 Plugins': '🧩 插件 (Plugins)',
    'GitHub Token': 'GitHub Token（令牌）',
    'HuggingFace Token': 'HuggingFace Token（令牌）',
    'Claude / Anthropic API Key': 'Claude / Anthropic API Key（密钥）',
    'Default Browser': '默认浏览器 (Default Browser)',
    'Floating Terminal Default': '浮动终端默认位置 (Floating Terminal Default)',
    'Desktop': '桌面 (Desktop)',
    'Auto-start with Windows': '随 Windows 自动启动 (Auto-start with Windows)',
    'Follow system theme': '跟随系统主题 (Follow system theme)',
    'Desktop notifications': '桌面通知 (Desktop notifications)',
    'Check for updates on launch': '启动时检查更新 (Check for updates on launch)',
    'Queue Notifier': '队列通知器 (Queue Notifier)',
    'Enable notifier': '启用通知器 (Enable notifier)',
    'On completion': '完成时通知 (On completion)',
    'On failure': '失败时通知 (On failure)',
    'On progress (every N%)': '进度通知（每 N%）(On progress)',
    'Progress step': '进度步长 (Progress step)',
    'Apprise URL': 'Apprise URL',
    'Send test': '发送测试 (Send test)',
    'Install Apprise': '安装 Apprise (Install Apprise)',
    'Xet Storage (hf_xet)': 'Xet 存储 (hf_xet)',
    'Install hf_xet': '安装 hf_xet',
    'GGUF CUDA Kernel': 'GGUF CUDA 内核 (Kernel)',
    'Enable GGUF CUDA kernels': '启用 GGUF CUDA 内核 (Enable GGUF CUDA kernels)',
    'Matmul mode': '矩阵乘法模式 (Matmul mode)',
    'Enable Stream-K (CUDA graphs)': '启用 Stream-K（CUDA graphs）',
    'BF16 → FP16 (legacy cuBLAS path)': 'BF16 → FP16（旧版 cuBLAS 路径）',
    'Save GGUF settings': '保存 GGUF 设置 (Save GGUF settings)',
    'AMD ROCm': 'AMD ROCm',
    'Disable MIOpen (unset MIOPEN_FIND_MODE)': '禁用 MIOpen（取消设置 MIOPEN_FIND_MODE）',
    'Save AMD settings': '保存 AMD 设置 (Save AMD settings)',
    'Repair Settings': '修复设置 (Repair Settings)',
    'Scan & Repair Settings': '扫描并修复设置 (Scan & Repair Settings)',
    'Share Link': '共享链接 (Share Link)',
    'Enable public share link (--share)': '启用公开共享链接 (--share)',
    'Extra Launch Args': '额外启动参数 (Extra Launch Args)',
    'Server Port': '服务器端口 (Server Port)',
    'GPU Device': 'GPU 设备 (GPU Device)',
    'Bind Address': '绑定地址 (Bind Address)',
    'Launcher GPU': '启动器 GPU (Launcher GPU)',
    'Save': '保存 (Save)',
    'Clear': '清除 (Clear)',
    'Refresh': '刷新 (Refresh)',
    'Install': '安装 (Install)',
    'Update': '更新 (Update)',
    'Restore': '恢复 (Restore)',
    'Reinstall': '重新安装 (Reinstall)',
    'Uninstall': '卸载 (Uninstall)',
    'Detect': '检测 (Detect)',
    'Apply': '应用 (Apply)',
    'Apply Overrides': '应用覆盖设置 (Apply Overrides)',
    'Close settings': '关闭设置 (Close settings)',
    'Bottom': '底部 (Bottom)',
    'Left': '左侧 (Left)',
    'Top': '顶部 (Top)',
    'Right': '右侧 (Right)',
    'Minimised': '最小化 (Minimised)',
    'Dashboard': '仪表盘 (Dashboard)',
    'Paths': '路径 (Paths)',
    'Models': '模型 (Models)',
    'Updates': '更新 (Updates)',
    'About': '关于 (About)',
    'Console': '控制台 (Console)',
    'Follow': '跟随滚动 (Follow)',
    'Terminal': '终端 (Terminal)',
    'Terminal No-GPU': '终端 No-GPU (Terminal No-GPU)',
    'Browser No-GPU': '浏览器 No-GPU (Browser No-GPU)',
    'Launch Wan2GP in Desktop': '在桌面模式启动 Wan2GP (Launch Wan2GP in Desktop)',
    'Create Desktop Shortcut': '创建桌面快捷方式 (Create Desktop Shortcut)',
    'Check Desktop Updates': '检查启动器更新 (Check Desktop Updates)',
    'Update Wan2GP (DeepBeepMeep)': '更新 Wan2GP (DeepBeepMeep)',
    'Wan2GP Updates': 'Wan2GP 更新 (Wan2GP Updates)',
    'Check for updates': '检查更新 (Check for updates)',
    'Full changelog on GitHub →': '在 GitHub 查看完整更新日志 →',
    'SYSTEM': '系统 (SYSTEM)',
    'PATHS & MODEL FOLDERS': '路径与模型目录 (PATHS & MODEL FOLDERS)',
    'GPU KERNEL WHEELS': 'GPU 内核组件 (GPU KERNEL WHEELS)',
    'ACTIVE ENVIRONMENT': '当前环境 (ACTIVE ENVIRONMENT)',
    'HARDWARE': '硬件 (HARDWARE)',
    'PERFORMANCE SETTINGS': '性能设置 (PERFORMANCE SETTINGS)',
    '⚡ Performance Auto-Tune': '⚡ 性能自动优化 (Performance Auto-Tune)',
    'Video Profile': '视频配置 (Video Profile)',
    'Image Profile': '图片配置 (Image Profile)',
    'Audio Profile': '音频配置 (Audio Profile)',
    'VRAM Safety Coeff (0.1–1)': '显存安全系数 (VRAM Safety Coeff, 0.1–1)',
    'VRAM Safety Coeff': '显存安全系数 (VRAM Safety Coeff)',
    'VAE Config': 'VAE 配置 (VAE Config)',
    'Transformer Quant': 'Transformer 量化 (Transformer Quant)',
    'Int8 Kernels (Experimental, ~10% faster, needs Triton)': 'INT8 内核（实验性，约快 10%，需要 Triton）',
    'Prefer failsafe (P5 — maximum compatibility)': '优先故障保护（P5 — 最大兼容性）(Prefer failsafe)',
    'Profile matrix (reference)': '配置档位矩阵（参考）(Profile matrix)',
    'VRAM \\ RAM': '显存 VRAM \\ 内存 RAM',
    'high': '高 (high)',
    'low': '低 (low)',
    'very low': '很低 (very low)',
    'tight': '紧张 (tight)',
    'auto': '自动 (auto)',
    'Enabled if Triton available': '检测到 Triton 时启用 (Enabled if Triton available)',
    'Disabled': '禁用 (Disabled)',
    'Enabled': '启用 (Enabled)',
    'recommended': '推荐 (recommended)',
    'saved': '已保存 (saved)',
    'recommended + saved': '推荐 + 已保存 (recommended + saved)',
    'INSTALL LOCATION': '安装位置 (INSTALL LOCATION)',
    'Checkpoints': '模型检查点 (Checkpoints)',
    'LoRAs': 'LoRA 模型 (LoRAs)',
    'Output': '输出目录 (Output)',
    'Environment': '环境 (Environment)',
    'Downloads': '下载 (Downloads)',
    'Resolved Install Stack': '已解析安装组件 (Resolved Install Stack)',
    'Free disk': '磁盘可用空间 (Free disk)',
    'Python': 'Python',
    'PyTorch': 'PyTorch',
    'CUDA build': 'CUDA 构建版本 (CUDA build)',
    'Profile': '配置档位 (Profile)',
    'Using Python environment': '正在使用 Python 环境 (Using Python environment)',
    'Validate installation': '验证安装 (Validate installation)',
    'Copy diagnostics': '复制诊断信息 (Copy diagnostics)',
    'Clone Wan2GP repository': '克隆 Wan2GP 仓库 (Clone repository)',
    'Create Python virtual environment': '创建 Python 虚拟环境 (Create virtual environment)',
    'Install PyTorch + CUDA': '安装 PyTorch + CUDA',
    'Install Python dependencies': '安装 Python 依赖 (Python dependencies)',
    'Install Triton compiler': '安装 Triton 编译器 (Triton compiler)',
    'Install Sage Attention kernel': '安装 SageAttention 内核 (kernel)',
    'Install Flash Attention': '安装 FlashAttention',
    'Install GPU kernels (nunchaku/GGUF)': '安装 GPU 内核（Nunchaku/GGUF）',
    'Finalize installation': '完成安装 (Finalize installation)',
    'PENDING': '等待中 (PENDING)',
    'READY': '就绪 (READY)',
    'Working...': '处理中… (Working...)',
    'Starting... (see console)': '正在启动…（查看控制台 / see console）',
    'Fetching latest updates...': '正在获取最新更新… (Fetching latest updates...)',
    'Installing...': '正在安装… (Installing...)',
    'Installation complete!': '安装完成！(Installation complete!)',
    'Starting Wan2GP': '正在启动 Wan2GP (Starting Wan2GP)'
  }));

  const longExact = new Map(Object.entries({
    'Detects your hardware and recommends optimal performance settings for Wan2GP. These settings are written directly to wgp_config.json.':
      '检测你的硬件，并为 Wan2GP 推荐合适的性能设置。这些设置会直接写入 wgp_config.json。',
    'Detect scans your hardware and calculates these mmgp knobs in wgp_config.json. Each dropdown defaults to the recommended value — change any to override.':
      '“检测 (Detect)”会扫描硬件，并计算 wgp_config.json 中的 MMGP 参数。每个下拉框默认使用推荐值，你也可以手动修改来覆盖。',
    'Optional — needed for gated models. Saved to desktop-config.json and passed as HF_TOKEN to Wan2GP on launch.':
      '可选 — 部分受限模型需要。会保存到 desktop-config.json，并在启动 Wan2GP 时作为 HF_TOKEN 传入。',
    'Used when launching Wan2GP in your browser ("Launch in Browser" opens the OS default).':
      '用于在浏览器中启动 Wan2GP；“Launch in Browser”会打开系统默认浏览器。',
    'Where the console opens when launching Wan2GP in Desktop. "Minimised" keeps it closed until you toggle it.':
      '在 Desktop 模式启动 Wan2GP 时，控制台默认出现的位置。“Minimised”会保持关闭，直到你手动打开。',
    'Launch Wan2GP Desktop automatically when you log in.':
      '登录 Windows 后自动启动 Wan2GP Desktop。',
    'Automatically switch between dark and light themes based on your Windows setting. Disables manual theme toggle.':
      '根据 Windows 设置自动切换深色/浅色主题；启用后会禁用手动主题切换。',
    'Show a notification when Wan2GP server is ready or stops.':
      'Wan2GP 服务器就绪或停止时显示桌面通知。',
    'Port for the Wan2GP web interface. Default: 7860. Changes apply on next launch.':
      'Wan2GP Web 界面的端口。默认：7860。修改后在下次启动时生效。'
  }));

  const patterns = [
    [/^rec:\s*(.+)$/i, '推荐 (rec): $1'],
    [/^saved:\s*(.+)$/i, '已保存 (saved): $1'],
    [/^(\d+(?:\.\d+)?)\s*GB free$/i, '可用空间 (Free): $1 GB'],
    [/^RAM\s*(.+)$/i, 'RAM 内存 $1'],
    [/^VRAM\s*(.+)$/i, 'VRAM 显存 $1'],
    [/^GPU\s*(.+)$/i, 'GPU $1'],
    [/^CPU\s*(.+)$/i, 'CPU $1'],
    [/^Status:\s*(.+)$/i, '状态 (Status): $1'],
    [/^Detection complete\. Review the recommendation below, then Apply to write settings \(Wan2GP must be restarted for them to take effect\)\.$/i,
      '检测完成。请检查下方推荐值，然后点击“应用 (Apply)”写入设置；需要重启 Wan2GP 才会生效。'],
    [/^This folder holds unknown files — install into an empty folder, or wipe it first\.$/i,
      '此文件夹包含未知文件 — 请安装到空文件夹，或先清空该文件夹。'],
    [/^This installs Wan2GP inside the Desktop app\. Once installed, you can launch, update, change settings, and browse generated files — all from the Dashboard\.$/i,
      '这会把 Wan2GP 安装到 Desktop 应用中。安装完成后，可从 Dashboard 启动、更新、修改设置并浏览生成文件。']
  ];

  const attrNames = ['title', 'aria-label'];

  function splitWhitespace(s) {
    const m = String(s).match(/^(\s*)([\s\S]*?)(\s*)$/);
    return m ? [m[1], m[2], m[3]] : ['', String(s), ''];
  }

  function translateCore(core) {
    if (!core || !/[A-Za-z]/.test(core)) return core;
    if (exact.has(core)) return exact.get(core);
    if (longExact.has(core)) return longExact.get(core);
    for (const [re, replacement] of patterns) {
      if (re.test(core)) return core.replace(re, replacement);
    }
    return core;
  }

  function translateTextNode(node) {
    if (!node || node.nodeType !== Node.TEXT_NODE) return;
    const parent = node.parentElement;
    if (!parent || ['SCRIPT', 'STYLE', 'CODE', 'PRE', 'TEXTAREA'].includes(parent.tagName)) return;
    const [pre, core, post] = splitWhitespace(node.nodeValue);
    const translated = translateCore(core);
    if (translated !== core) node.nodeValue = pre + translated + post;
  }

  function translateAttributes(el) {
    if (!(el instanceof Element)) return;
    for (const attr of attrNames) {
      const value = el.getAttribute(attr);
      if (!value) continue;
      const translated = translateCore(value);
      if (translated !== value) el.setAttribute(attr, translated);
    }
    const ph = el.getAttribute('placeholder');
    if (ph && exact.has(ph)) el.setAttribute('placeholder', exact.get(ph));
  }

  function translateTree(root) {
    if (!root) return;
    if (root.nodeType === Node.TEXT_NODE) {
      translateTextNode(root);
      return;
    }
    if (root instanceof Element) translateAttributes(root);
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = walker.nextNode())) translateTextNode(n);
    if (root.querySelectorAll) root.querySelectorAll('*').forEach(translateAttributes);
  }

  function installChineseFontFallback() {
    const style = document.createElement('style');
    style.id = 'wan2gp-zhcn-font-fallback';
    style.textContent = `
      body { font-family: "Segoe UI", "Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC", sans-serif; }
      code, pre, .console, .terminal, [class*="mono"] { font-family: "Cascadia Mono", "Consolas", monospace; }
      .zhcn-lang-toggle { margin-left:auto; min-width:88px; white-space:nowrap; }
    `;
    document.head.appendChild(style);
  }

  function installModeButton() {
    const add = () => {
      if (document.getElementById('zhcnLangToggle')) return true;
      const bar = document.querySelector('.settings-topbar');
      if (!bar) return false;
      const btn = document.createElement('button');
      btn.id = 'zhcnLangToggle';
      btn.className = 'btn btn-ghost small zhcn-lang-toggle';
      btn.type = 'button';
      btn.title = '切换界面语言 (Switch UI language)';
      btn.textContent = currentMode === MODE_BILINGUAL ? '中文+EN' : 'English';
      btn.addEventListener('click', () => {
        localStorage.setItem(STORAGE_KEY, currentMode === MODE_BILINGUAL ? MODE_ENGLISH : MODE_BILINGUAL);
        location.reload();
      });
      bar.appendChild(btn);
      return true;
    };
    if (!add()) {
      const timer = setInterval(() => { if (add()) clearInterval(timer); }, 300);
      setTimeout(() => clearInterval(timer), 15000);
    }
  }

  function boot() {
    installModeButton();
    if (currentMode !== MODE_BILINGUAL) return;
    document.documentElement.lang = 'zh-CN';
    installChineseFontFallback();
    translateTree(document.body);

    let scheduled = false;
    const pending = new Set();
    const flush = () => {
      scheduled = false;
      for (const node of pending) translateTree(node);
      pending.clear();
    };
    const observer = new MutationObserver((mutations) => {
      for (const m of mutations) {
        if (m.type === 'characterData') pending.add(m.target);
        for (const node of m.addedNodes || []) pending.add(node);
      }
      if (!scheduled && pending.size) {
        scheduled = true;
        queueMicrotask(flush);
      }
    });
    observer.observe(document.body, {subtree:true, childList:true, characterData:true});
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, {once:true});
  else boot();
})();
