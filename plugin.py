import json
import os

from shared.utils.plugins import WAN2GPPlugin


PLUGIN_VERSION = "0.4.0"
PLUGIN_DIR = os.path.dirname(__file__)
LOCALE_PATHS = [
    os.path.join(PLUGIN_DIR, "locales", "zh_CN.json"),
    os.path.join(PLUGIN_DIR, "locales", "zh_CN_v3.json"),
    os.path.join(PLUGIN_DIR, "locales", "zh_CN_v4.json"),
]


def _load_locale_pack():
    merged = {
        "schema": 1,
        "locale": "zh-CN",
        "exact": {},
        "attributes": {},
        "patterns": [],
        "pure_overrides": {},
    }
    for path in LOCALE_PATHS:
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as locale_file:
            pack = json.load(locale_file)
        merged["exact"].update(pack.get("exact") or {})
        merged["attributes"].update(pack.get("attributes") or {})
        merged["patterns"].extend(pack.get("patterns") or [])
        merged["pure_overrides"].update(pack.get("pure_overrides") or {})
    return merged


class WanGPChineseBilingualPlugin(WAN2GPPlugin):
    "WanGP Simplified Chinese localization with Chinese/bilingual/English modes."

    def __init__(self):
        super().__init__()
        self.name = "WanGP 简体中文 / 双语界面"
        self.version = PLUGIN_VERSION
        self.description = (
            "WanGP v13 简体中文本地化。支持纯中文 / 中英双语 / 原始英文三种模式；"
            "支持 Shadow DOM、同源 iframe、下拉框已选值本地化与可见 UI 未译扫描。"
        )
        self.type = ["extension"]

    def setup_ui(self):
        locale_json = json.dumps(_load_locale_pack(), ensure_ascii=False)
        self.add_custom_js(self._build_js(locale_json))

    @staticmethod
    def _build_js(locale_json: str) -> str:
        template = r'''(function () {
  "use strict";

  const MODE_KEY = "wangp_zh_cn_mode";
  const LEGACY_KEY = "wangp_zh_cn_enabled";
  const VALID_MODES = new Set(["zh", "bi", "en"]);
  const PACK = __LOCALE__;
  const EXACT = PACK.exact || {};
  const ATTR = PACK.attributes || {};
  const PURE_OVERRIDES = PACK.pure_overrides || {};
  const PATTERNS = (PACK.patterns || []).map((rule) => ({
    re: new RegExp(rule.regex, rule.flags || ""),
    replacement: rule.replacement || ""
  }));

  if (window.__wangpZhCnLocalizationV4Loaded) return;
  window.__wangpZhCnLocalizationV4Loaded = true;

  const observedRoots = new WeakSet();
  const observedFrames = new WeakSet();
  const boundDocs = new WeakSet();
  const pendingRoots = new Set();
  let queued = false;

  function getMode() {
    const stored = localStorage.getItem(MODE_KEY);
    if (VALID_MODES.has(stored)) return stored;
    return localStorage.getItem(LEGACY_KEY) === "0" ? "en" : "bi";
  }

  function setMode(mode) {
    if (!VALID_MODES.has(mode)) return;
    localStorage.setItem(MODE_KEY, mode);
    localStorage.removeItem(LEGACY_KEY);
    location.reload();
  }

  function enabled() { return getMode() !== "en"; }
  function norm(v) { return (v || "").replace(/\s+/g, " ").trim(); }
  function hasCJK(v) { return /[\u3400-\u9fff]/.test(v || ""); }

  function looksEnglish(v) {
    const s = norm(v);
    if (!s || s.length < 2 || hasCJK(s) || !/[A-Za-z]{2,}/.test(s)) return false;
    if (/^(https?:\/\/|file:|data:|blob:)/i.test(s)) return false;
    if (/^[A-Z0-9_.+\-/]{1,16}$/.test(s)) return false;
    return true;
  }

  function scannerNoise(v) {
    const s = norm(v);
    if (!s) return true;
    const lower = s.toLowerCase();
    if (["and","or","for","in","of","by","over","select","the","to","from"].includes(lower)) return true;
    if (/^[_$]{1,2}[A-Za-z0-9_.-]+$/.test(s)) return true;
    if (/^--[A-Za-z0-9-]+$/.test(s)) return true;
    if (/^[A-Za-z0-9_.-]+\.(json|jsonc|py|js|css|safetensors|ckpt|pt|pth|bin|dll|exe)$/i.test(s)) return true;
    if (/^[A-Za-z]:[\\/]/.test(s) || /^[/\\][^ ]+/.test(s)) return true;
    if (/^[a-z0-9]+(?:_[a-z0-9]+)+$/.test(s)) return true;
    return false;
  }

  function stripEnglishParentheticals(v) {
    let out = String(v || "");
    out = out.replace(/\s*[（(][^()（）]*[A-Za-z][^()（）]*[)）]\s*/g, " ");
    out = out.replace(/\s+/g, " ").trim();
    return out || String(v || "");
  }

  function pureTranslation(source, bilingual) {
    const key = norm(source);
    if (Object.prototype.hasOwnProperty.call(PURE_OVERRIDES, key)) return PURE_OVERRIDES[key];
    return stripEnglishParentheticals(bilingual);
  }

  function translateString(value) {
    if (!enabled()) return null;
    const key = norm(value);
    if (!key) return null;
    let translated = null;
    if (Object.prototype.hasOwnProperty.call(EXACT, key)) {
      translated = EXACT[key];
    } else {
      for (const rule of PATTERNS) {
        rule.re.lastIndex = 0;
        if (rule.re.test(key)) {
          rule.re.lastIndex = 0;
          translated = key.replace(rule.re, rule.replacement);
          break;
        }
      }
    }
    if (!translated) return null;
    return getMode() === "zh" ? pureTranslation(key, translated) : translated;
  }

  function isOurUi(el) {
    return !!el?.closest?.("#wangp-zh-cn-control, #wangp-zh-cn-untranslated-panel");
  }

  function shouldSkip(el) {
    if (!el || el.nodeType !== Node.ELEMENT_NODE) return false;
    if (["SCRIPT", "STYLE", "TEXTAREA", "CODE", "PRE"].includes(el.tagName)) return true;
    if (el.isContentEditable || el.closest?.('[contenteditable="true"]')) return true;
    return isOurUi(el);
  }

  function isEffectivelyVisible(el) {
    if (!el || el.nodeType !== Node.ELEMENT_NODE || !el.isConnected) return false;
    if (el.closest?.("[hidden], [aria-hidden='true'], [inert]")) return false;
    let cur = el;
    const view = el.ownerDocument?.defaultView;
    while (cur && cur.nodeType === Node.ELEMENT_NODE) {
      let style = null;
      try { style = view?.getComputedStyle?.(cur); } catch (_e) {}
      if (style && (style.display === "none" || style.visibility === "hidden" || style.visibility === "collapse")) return false;
      cur = cur.parentElement;
    }
    try {
      if (el.getClientRects && el.getClientRects().length === 0) return false;
    } catch (_e) {}
    return true;
  }

  function translateTextNode(node) {
    if (!enabled() || !node || node.nodeType !== Node.TEXT_NODE) return;
    if (node.parentElement && shouldSkip(node.parentElement)) return;
    const raw = node.nodeValue || "";
    const translated = translateString(raw);
    if (!translated || translated === norm(raw)) return;
    const lead = raw.match(/^\s*/)?.[0] || "";
    const tail = raw.match(/\s*$/)?.[0] || "";
    node.nodeValue = lead + translated + tail;
  }

  function translateAttributes(el) {
    if (!enabled() || !el || el.nodeType !== Node.ELEMENT_NODE || isOurUi(el)) return;
    for (const attr of ["placeholder", "title", "aria-label", "aria-description"]) {
      const value = el.getAttribute?.(attr);
      if (!value) continue;
      const key = norm(value);
      let translated = null;
      if (Object.prototype.hasOwnProperty.call(ATTR, key)) {
        translated = getMode() === "zh" ? pureTranslation(key, ATTR[key]) : ATTR[key];
      } else {
        translated = translateString(value);
      }
      if (translated && translated !== value) el.setAttribute(attr, translated);
    }
  }

  function isComboboxInput(el) {
    if (!el || el.nodeType !== Node.ELEMENT_NODE || el.tagName !== "INPUT") return false;
    const type = (el.getAttribute("type") || "text").toLowerCase();
    if (!["text", "search", ""].includes(type)) return false;
    return (
      el.getAttribute("role") === "combobox" ||
      el.getAttribute("aria-haspopup") === "listbox" ||
      !!el.closest?.('[role="combobox"]')
    );
  }

  function sourceComboValue(el) {
    const current = norm(el.value || "");
    const oldSource = el.dataset.wangpI18nSourceValue || "";
    const oldTranslated = el.dataset.wangpI18nTranslatedValue || "";
    if (oldTranslated && current === oldTranslated && oldSource) return oldSource;
    return current;
  }

  function translateComboboxDisplay(el) {
    if (!enabled() || !isComboboxInput(el) || isOurUi(el)) return;
    if (el.ownerDocument?.activeElement === el && el.getAttribute("aria-expanded") === "true") return;
    const source = sourceComboValue(el);
    if (!source || !Object.prototype.hasOwnProperty.call(EXACT, source)) return;
    const translated = translateString(source);
    if (!translated || translated === source) return;
    el.dataset.wangpI18nSourceValue = source;
    el.dataset.wangpI18nTranslatedValue = translated;
    if (el.value !== translated) el.value = translated;
  }

  function restoreComboboxForInteraction(el) {
    if (!isComboboxInput(el)) return;
    const source = el.dataset.wangpI18nSourceValue;
    const translated = el.dataset.wangpI18nTranslatedValue;
    if (source && translated && el.value === translated) el.value = source;
  }

  function acceptComboboxChange(el) {
    if (!isComboboxInput(el)) return;
    const current = norm(el.value || "");
    const oldTranslated = el.dataset.wangpI18nTranslatedValue || "";
    if (current && current !== oldTranslated) {
      el.dataset.wangpI18nSourceValue = current;
      delete el.dataset.wangpI18nTranslatedValue;
    }
    setTimeout(() => {
      if (el.getAttribute("aria-expanded") !== "true") translateComboboxDisplay(el);
    }, 80);
  }

  function refreshComboboxes(doc) {
    if (!enabled() || !doc) return;
    let inputs = [];
    try { inputs = Array.from(doc.querySelectorAll("input")); } catch (_e) {}
    for (const input of inputs) translateComboboxDisplay(input);
  }

  function bindDocumentEvents(doc) {
    if (!doc || boundDocs.has(doc)) return;
    boundDocs.add(doc);
    doc.addEventListener("focusin", (event) => {
      const el = event.target;
      if (isComboboxInput(el)) restoreComboboxForInteraction(el);
    }, true);
    doc.addEventListener("focusout", (event) => {
      const el = event.target;
      if (isComboboxInput(el)) setTimeout(() => translateComboboxDisplay(el), 80);
    }, true);
    doc.addEventListener("change", (event) => acceptComboboxChange(event.target), true);
    doc.addEventListener("input", (event) => {
      if (!isComboboxInput(event.target)) return;
      const el = event.target;
      const current = norm(el.value || "");
      const translated = el.dataset.wangpI18nTranslatedValue || "";
      if (current && current !== translated) {
        el.dataset.wangpI18nSourceValue = current;
        delete el.dataset.wangpI18nTranslatedValue;
      }
    }, true);
  }

  function walkNode(root, fn) {
    if (!root) return;
    if (root.nodeType === Node.TEXT_NODE) { fn(root); return; }
    if (![Node.ELEMENT_NODE, Node.DOCUMENT_NODE, Node.DOCUMENT_FRAGMENT_NODE].includes(root.nodeType)) return;
    if (root.nodeType === Node.ELEMENT_NODE && shouldSkip(root)) return;
    const doc = root.ownerDocument || (root.nodeType === Node.DOCUMENT_NODE ? root : document);
    const walker = doc.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        if (node.nodeType === Node.ELEMENT_NODE && shouldSkip(node)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    fn(root);
    let node;
    while ((node = walker.nextNode())) fn(node);
  }

  function translateTree(root) {
    if (!enabled() || !root) return;
    const doc = root.ownerDocument || (root.nodeType === Node.DOCUMENT_NODE ? root : document);
    bindDocumentEvents(doc);
    walkNode(root, (node) => {
      if (node.nodeType === Node.TEXT_NODE) {
        translateTextNode(node);
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        translateAttributes(node);
        translateComboboxDisplay(node);
        if (node.shadowRoot) observeRoot(node.shadowRoot);
        if (node.tagName === "IFRAME") observeIframe(node);
      }
    });
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
      if (!roots.length && document.body) roots.push(document.body);
      for (const r of roots) {
        try { translateTree(r); } catch (e) { console.debug("[WanGP ZH-CN] scan skipped", e); }
      }
    });
  }

  function observeRoot(root) {
    if (!root || observedRoots.has(root)) return;
    observedRoots.add(root);
    const doc = root.ownerDocument || (root.nodeType === Node.DOCUMENT_NODE ? root : document);
    bindDocumentEvents(doc);
    try { translateTree(root); } catch (e) { console.debug("[WanGP ZH-CN] initial scan skipped", e); }
    const observer = new MutationObserver((mutations) => {
      if (!enabled()) return;
      for (const m of mutations) {
        if (m.type === "characterData" || m.type === "attributes") schedule(m.target);
        for (const n of m.addedNodes || []) schedule(n);
      }
    });
    try {
      observer.observe(root, {
        subtree: true,
        childList: true,
        characterData: true,
        attributes: true,
        attributeFilter: ["placeholder", "title", "aria-label", "aria-description", "aria-expanded", "value"]
      });
    } catch (e) {
      console.debug("[WanGP ZH-CN] observer skipped", e);
    }
  }

  function iframeDocument(frame) {
    try { return frame.contentDocument || frame.contentWindow?.document || null; }
    catch (_e) { return null; }
  }

  function observeIframe(frame) {
    if (!frame || observedFrames.has(frame)) return;
    observedFrames.add(frame);
    const attach = () => {
      const doc = iframeDocument(frame);
      if (!doc?.documentElement) return;
      if (enabled()) doc.documentElement.lang = "zh-CN";
      bindDocumentEvents(doc);
      observeRoot(doc.documentElement);
      discoverNestedRoots(doc);
      refreshComboboxes(doc);
    };
    frame.addEventListener("load", () => setTimeout(attach, 0));
    attach();
  }

  function discoverNestedRoots(doc = document) {
    let all = [];
    try { all = Array.from(doc.querySelectorAll("*")); } catch (_e) { return; }
    bindDocumentEvents(doc);
    for (const el of all) {
      if (el.shadowRoot) observeRoot(el.shadowRoot);
      if (el.tagName === "IFRAME") observeIframe(el);
    }
    refreshComboboxes(doc);
  }

  function getAccessibleDocuments(visibleOnly = false) {
    const docs = [], seen = new Set();
    function add(doc) {
      if (!doc || seen.has(doc)) return;
      seen.add(doc);
      docs.push(doc);
      let frames = [];
      try { frames = Array.from(doc.querySelectorAll("iframe")); } catch (_e) {}
      for (const frame of frames) {
        if (visibleOnly && !isEffectivelyVisible(frame)) continue;
        const child = iframeDocument(frame);
        if (child) add(child);
      }
    }
    add(document);
    return docs;
  }

  function isDocumentLikeText(parent, text) {
    if (!parent) return false;
    if (text.length > 140) return true;
    const tag = parent.tagName;
    const markdownHost = parent.closest?.(
      ".prose, .markdown, .md, [class*='markdown'], [data-testid*='markdown'], .html-container"
    );
    if (!markdownHost) return false;
    return ["P", "LI", "BLOCKQUOTE", "TD", "TH", "DIV", "SPAN"].includes(tag) && text.length > 70;
  }

  function collectUntranslated() {
    const ui = new Set();
    const docs = new Set();
    for (const doc of getAccessibleDocuments(true)) {
      const root = doc.body || doc.documentElement;
      if (!root) continue;
      walkNode(root, (node) => {
        if (node.nodeType !== Node.TEXT_NODE) return;
        const parent = node.parentElement;
        if (!parent || shouldSkip(parent) || !isEffectivelyVisible(parent)) return;
        const text = norm(node.nodeValue || "");
        if (!looksEnglish(text) || scannerNoise(text) || translateString(text) || text.length > 260) return;
        (isDocumentLikeText(parent, text) ? docs : ui).add(text);
      });
      let inputs = [];
      try { inputs = Array.from(doc.querySelectorAll("input")); } catch (_e) {}
      for (const input of inputs) {
        if (!isComboboxInput(input) || !isEffectivelyVisible(input)) continue;
        const text = sourceComboValue(input);
        if (!looksEnglish(text) || scannerNoise(text) || translateString(text)) continue;
        ui.add(text);
      }
    }
    const sorter = (a, b) => a.localeCompare(b, "en");
    return { ui: Array.from(ui).sort(sorter), docs: Array.from(docs).sort(sorter) };
  }

  function showUntranslatedPanel() {
    let panel = document.getElementById("wangp-zh-cn-untranslated-panel");
    if (panel) { panel.remove(); return; }
    const groups = collectUntranslated();
    let active = "ui";
    panel = document.createElement("div");
    panel.id = "wangp-zh-cn-untranslated-panel";
    panel.innerHTML = [
      '<div class="title"></div>',
      '<div class="note">只统计当前真正可见的页面；隐藏 Tab 不再计入。UI 与长文档分开复制。</div>',
      '<div class="scan-tabs"></div>',
      '<textarea readonly></textarea>',
      '<div class="actions"></div>'
    ].join("");

    const title = panel.querySelector(".title");
    const area = panel.querySelector("textarea");
    const tabs = panel.querySelector(".scan-tabs");

    function renderGroup() {
      const items = groups[active];
      title.textContent = `当前可见未翻译：UI ${groups.ui.length} / 文档 ${groups.docs.length}`;
      area.value = items.join("\n");
      for (const btn of tabs.querySelectorAll("button")) {
        btn.classList.toggle("active", btn.dataset.group === active);
      }
    }

    for (const [key, label] of [["ui", "UI 文本"], ["docs", "文档 / 长说明"]]) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.dataset.group = key;
      btn.textContent = `${label} (${groups[key].length})`;
      btn.onclick = () => { active = key; renderGroup(); };
      tabs.appendChild(btn);
    }

    const copy = document.createElement("button");
    copy.textContent = "复制当前列表";
    copy.onclick = async () => {
      const value = area.value;
      try {
        await navigator.clipboard.writeText(value);
        copy.textContent = "已复制";
      } catch (_e) {
        area.select();
        document.execCommand("copy");
      }
      setTimeout(() => copy.textContent = "复制当前列表", 1200);
    };

    const close = document.createElement("button");
    close.textContent = "关闭";
    close.onclick = () => panel.remove();
    panel.querySelector(".actions").append(copy, close);
    document.body.appendChild(panel);
    renderGroup();
  }

  function injectStyles() {
    if (document.getElementById("wangp-zh-cn-style")) return;
    const style = document.createElement("style");
    style.id = "wangp-zh-cn-style";
    style.textContent = `
      #wangp-zh-cn-control{position:fixed;right:12px;bottom:12px;z-index:2147483646;display:flex;align-items:center;gap:3px;padding:4px;border:1px solid rgba(120,160,200,.38);border-radius:10px;background:rgba(10,18,31,.94);box-shadow:0 6px 20px rgba(0,0,0,.3);backdrop-filter:blur(9px);font-family:system-ui,"Microsoft YaHei UI",sans-serif}
      #wangp-zh-cn-control button{min-width:42px;border:0;border-radius:7px;padding:6px 8px;background:transparent;color:#d9e8f7;cursor:pointer;font-size:12px;line-height:1}
      #wangp-zh-cn-control button:hover{background:rgba(66,139,202,.22)}
      #wangp-zh-cn-control button.active{background:#24679c;color:#fff;font-weight:700}
      #wangp-zh-cn-control button:disabled{opacity:.45;cursor:default}
      #wangp-zh-cn-control .sep{width:1px;height:20px;margin:0 1px;background:rgba(180,210,235,.24)}
      #wangp-zh-cn-untranslated-panel{position:fixed;right:12px;bottom:58px;z-index:2147483647;width:min(560px,calc(100vw - 24px));max-height:68vh;box-sizing:border-box;padding:12px;border:1px solid rgba(120,160,200,.45);border-radius:12px;background:rgba(10,18,31,.98);color:#e8f2fb;box-shadow:0 12px 34px rgba(0,0,0,.42);font-family:system-ui,"Microsoft YaHei UI",sans-serif}
      #wangp-zh-cn-untranslated-panel .title{font-weight:800;margin-bottom:4px}
      #wangp-zh-cn-untranslated-panel .note{font-size:12px;opacity:.78;margin-bottom:8px}
      #wangp-zh-cn-untranslated-panel .scan-tabs{display:flex;gap:6px;margin-bottom:8px}
      #wangp-zh-cn-untranslated-panel textarea{width:100%;height:min(42vh,420px);resize:vertical;box-sizing:border-box;padding:9px;border:1px solid rgba(120,160,200,.34);border-radius:8px;background:#07111e;color:#e8f2fb;font:12px/1.45 ui-monospace,Consolas,monospace}
      #wangp-zh-cn-untranslated-panel .actions{display:flex;justify-content:flex-end;gap:8px;margin-top:8px}
      #wangp-zh-cn-untranslated-panel button{border:1px solid rgba(120,160,200,.38);border-radius:7px;padding:6px 10px;background:#173755;color:#fff;cursor:pointer}
      #wangp-zh-cn-untranslated-panel button.active{background:#24679c;font-weight:700}
    `;
    document.head.appendChild(style);
  }

  function addModeControl() {
    if (document.getElementById("wangp-zh-cn-control")) return;
    injectStyles();
    const wrap = document.createElement("div");
    wrap.id = "wangp-zh-cn-control";
    const mode = getMode();

    for (const [value, label, title] of [
      ["zh", "中文", "纯中文"],
      ["bi", "中英", "中文 + 英文技术术语"],
      ["en", "EN", "原始英文"]
    ]) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = label;
      btn.title = title;
      if (value === mode) btn.classList.add("active");
      btn.onclick = () => setMode(value);
      wrap.appendChild(btn);
    }

    const sep = document.createElement("span");
    sep.className = "sep";
    wrap.appendChild(sep);

    const missing = document.createElement("button");
    missing.id = "wangp-zh-cn-untranslated";
    missing.type = "button";
    missing.textContent = "未译";
    missing.title = "扫描当前真正可见页面仍未覆盖的文本";
    missing.disabled = mode === "en";
    missing.onclick = showUntranslatedPanel;
    wrap.appendChild(missing);

    document.body.appendChild(wrap);
  }

  function boot() {
    const mode = getMode();
    if (mode !== "en") document.documentElement.lang = "zh-CN";
    addModeControl();

    if (mode !== "en") {
      bindDocumentEvents(document);
      observeRoot(document.documentElement);
      discoverNestedRoots(document);
      [200, 600, 1200, 2200, 4000, 7000].forEach((delay) => {
        setTimeout(() => {
          schedule(document.body);
          discoverNestedRoots(document);
          for (const doc of getAccessibleDocuments(false)) refreshComboboxes(doc);
        }, delay);
      });
      setInterval(() => {
        discoverNestedRoots(document);
        for (const doc of getAccessibleDocuments(false)) refreshComboboxes(doc);
      }, 3500);
    }

    console.info(`[WanGP ZH-CN] localization v0.4.0 active; mode=${mode}`);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();'''
        return template.replace("__LOCALE__", locale_json)
