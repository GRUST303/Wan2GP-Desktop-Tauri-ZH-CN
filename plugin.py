import json
import os

from shared.utils.plugins import WAN2GPPlugin


PLUGIN_VERSION = "0.2.0"
LOCALE_PATH = os.path.join(os.path.dirname(__file__), "locales", "zh_CN.json")


class WanGPChineseBilingualPlugin(WAN2GPPlugin):
    """Simplified Chinese UI localization while preserving English technical terms."""

    def __init__(self):
        super().__init__()
        self.name = "WanGP 简体中文双语汉化"
        self.version = PLUGIN_VERSION
        self.description = (
            "WanGP 简体中文本地化。中文优先显示，同时保留 VRAM / CUDA / VAE / INT8 / "
            "Steps / Guidance 等英文技术术语。"
        )
        self.type = ["extension"]

    def setup_ui(self):
        with open(LOCALE_PATH, "r", encoding="utf-8") as locale_file:
            locale_pack = json.load(locale_file)
        locale_json = json.dumps(locale_pack, ensure_ascii=False)
        self.add_custom_js(self._build_js(locale_json))

    @staticmethod
    def _build_js(locale_json: str) -> str:
        template = r'''(function () {
  "use strict";

  const PLUGIN_ID = "wangp-zh-cn-bilingual";
  const STORAGE_KEY = "wangp_zh_cn_enabled";
  const PACK = __LOCALE__;
  const EXACT = PACK.exact || {};
  const ATTR = PACK.attributes || {};
  const PATTERNS = (PACK.patterns || []).map((rule) => ({
    re: new RegExp(rule.regex, rule.flags || ""),
    replacement: rule.replacement || ""
  }));
  const DEBUG = false;

  if (window.__wangpZhCnBilingualLoaded) return;
  window.__wangpZhCnBilingualLoaded = true;

  const observedRoots = new WeakSet();
  const pendingRoots = new Set();
  let queued = false;

  function enabled() {
    return localStorage.getItem(STORAGE_KEY) !== "0";
  }

  function normaliseText(value) {
    return (value || "").replace(/\s+/g, " ").trim();
  }

  function translateString(value) {
    const key = normaliseText(value);
    if (!key) return null;
    if (Object.prototype.hasOwnProperty.call(EXACT, key)) return EXACT[key];
    for (const rule of PATTERNS) {
      rule.re.lastIndex = 0;
      if (rule.re.test(key)) {
        rule.re.lastIndex = 0;
        return key.replace(rule.re, rule.replacement);
      }
    }
    return null;
  }

  function shouldSkipElement(el) {
    if (!el || el.nodeType !== Node.ELEMENT_NODE) return false;
    const tag = el.tagName;
    if (["SCRIPT", "STYLE", "TEXTAREA", "INPUT", "CODE", "PRE"].includes(tag)) return true;
    if (el.isContentEditable || el.closest?.('[contenteditable="true"]')) return true;
    if (el.closest?.("#wangp-zh-cn-toggle")) return true;
    return false;
  }

  function translateTextNode(node) {
    if (!enabled() || !node || node.nodeType !== Node.TEXT_NODE) return;
    const parent = node.parentElement;
    if (parent && shouldSkipElement(parent)) return;

    const raw = node.nodeValue || "";
    const translated = translateString(raw);
    if (!translated) return;

    const leading = raw.match(/^\s*/)?.[0] || "";
    const trailing = raw.match(/\s*$/)?.[0] || "";
    node.nodeValue = leading + translated + trailing;
  }

  function translateAttributes(el) {
    if (!enabled() || !el || el.nodeType !== Node.ELEMENT_NODE) return;
    for (const attr of ["placeholder", "title", "aria-label", "aria-description"]) {
      const value = el.getAttribute?.(attr);
      if (!value) continue;
      const key = normaliseText(value);
      const translated =
        (Object.prototype.hasOwnProperty.call(ATTR, key) && ATTR[key]) ||
        translateString(value);
      if (translated && translated !== value) el.setAttribute(attr, translated);
    }
  }

  function translateTree(root) {
    if (!enabled() || !root) return;

    if (root.nodeType === Node.TEXT_NODE) {
      translateTextNode(root);
      return;
    }

    const validRoot =
      root.nodeType === Node.ELEMENT_NODE ||
      root.nodeType === Node.DOCUMENT_NODE ||
      root.nodeType === Node.DOCUMENT_FRAGMENT_NODE;
    if (!validRoot) return;

    if (root.nodeType === Node.ELEMENT_NODE) {
      if (shouldSkipElement(root)) return;
      translateAttributes(root);
      if (root.shadowRoot) observeRoot(root.shadowRoot);
    }

    const walker = document.createTreeWalker(
      root,
      NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT,
      {
        acceptNode(node) {
          if (node.nodeType === Node.ELEMENT_NODE && shouldSkipElement(node)) {
            return NodeFilter.FILTER_REJECT;
          }
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );

    let node;
    while ((node = walker.nextNode())) {
      if (node.nodeType === Node.TEXT_NODE) {
        translateTextNode(node);
      } else {
        translateAttributes(node);
        if (node.shadowRoot) observeRoot(node.shadowRoot);
      }
    }
  }

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
      for (const rootNode of roots) {
        try {
          translateTree(rootNode);
        } catch (error) {
          if (DEBUG) console.warn("[WanGP ZH-CN]", error);
        }
      }
    });
  }

  function observeRoot(root) {
    if (!root || observedRoots.has(root)) return;
    observedRoots.add(root);

    try {
      translateTree(root);
    } catch (error) {
      if (DEBUG) console.warn("[WanGP ZH-CN] initial root scan", error);
    }

    const observer = new MutationObserver((mutations) => {
      if (!enabled()) return;
      for (const mutation of mutations) {
        if (mutation.type === "characterData") schedule(mutation.target);
        if (mutation.type === "attributes") schedule(mutation.target);
        for (const node of mutation.addedNodes || []) schedule(node);
      }
    });

    observer.observe(root, {
      subtree: true,
      childList: true,
      characterData: true,
      attributes: true,
      attributeFilter: ["placeholder", "title", "aria-label", "aria-description"]
    });
  }

  function discoverShadowRoots() {
    if (!enabled()) return;
    const all = document.querySelectorAll("*");
    for (const el of all) {
      if (el.shadowRoot) observeRoot(el.shadowRoot);
    }
  }

  function addToggle() {
    if (document.getElementById("wangp-zh-cn-toggle")) return;

    const button = document.createElement("button");
    button.id = "wangp-zh-cn-toggle";
    button.type = "button";
    button.textContent = enabled() ? "中 / EN" : "中文";
    button.title = enabled()
      ? "切换到英文界面 (Switch to English)"
      : "启用简体中文 (Enable Chinese)";
    button.setAttribute("aria-label", button.title);
    button.style.cssText = [
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

    button.addEventListener("click", () => {
      localStorage.setItem(STORAGE_KEY, enabled() ? "0" : "1");
      location.reload();
    });

    document.body.appendChild(button);
  }

  function boot() {
    if (enabled()) {
      document.documentElement.lang = "zh-CN";
    }

    addToggle();
    observeRoot(document.documentElement);
    discoverShadowRoots();

    // Gradio builds/replaces controls asynchronously; rescan a few times after startup.
    [250, 800, 1600, 3000, 6000].forEach((delay) => {
      setTimeout(() => {
        schedule(document.body);
        discoverShadowRoots();
      }, delay);
    });

    // Low-frequency fallback for lazily mounted tabs/components.
    setInterval(discoverShadowRoots, 5000);
    console.info("[WanGP ZH-CN] localization v0.2.0 active");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();'''
        return template.replace("__LOCALE__", locale_json)
