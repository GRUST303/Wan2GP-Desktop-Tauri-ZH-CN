(function () {
  "use strict";

  const VERSION = "__PLUGIN_VERSION__";
  const MODE_KEY = "wangp_zh_cn_mode";
  const LEGACY_KEY = "wangp_zh_cn_enabled";
  const SCAN_KEY = "wangp_zh_cn_untranslated_accumulator_v2";
  const SCAN_DOCS_KEY = "wangp_zh_cn_scan_include_docs";
  const AUTO_SCAN_KEY = "wangp_zh_cn_auto_scan";
  const VALID_MODES = new Set(["zh", "bi", "en"]);
  const PACK = __LOCALE__;
  const EXACT = PACK.exact || {};
  const ATTR = PACK.attributes || {};
  const PURE_OVERRIDES = PACK.pure_overrides || {};
  const FRAGMENTS = PACK.fragments || {};
  const PATTERNS = (PACK.patterns || []).map((rule) => ({
    re: new RegExp(rule.regex, rule.flags || ""),
    replacement: rule.replacement || ""
  }));

  if (window.__wangpZhCnLocalizationV5Loaded) return;
  window.__wangpZhCnLocalizationV5Loaded = true;

  const observedRoots = new WeakSet();
  const observedFrames = new WeakSet();
  const pendingRoots = new Set();
  const comboboxBindings = new WeakSet();
  let queued = false;
  let autoScanTimer = 0;
  let lastCurrentScan = null;

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
  function norm(v) { return String(v || "").replace(/\s+/g, " ").trim(); }
  function hasCJK(v) { return /[\u3400-\u9fff]/.test(String(v || "")); }

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

  function applyFragments(key) {
    if (!key || hasCJK(key)) return null;
    let out = key;
    let changed = false;
    const entries = Object.entries(FRAGMENTS).sort((a, b) => b[0].length - a[0].length);
    for (const [source, target] of entries) {
      if (!source || !out.includes(source)) continue;
      out = out.split(source).join(target);
      changed = true;
    }
    return changed ? out : null;
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
      if (!translated) translated = applyFragments(key);
    }
    if (!translated || translated === key) return null;
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

  function translateTextNode(node) {
    if (!enabled() || !node || node.nodeType !== Node.TEXT_NODE) return;
    if (node.parentElement && shouldSkip(node.parentElement)) return;
    const raw = node.nodeValue || "";
    const translated = translateString(raw);
    if (!translated) return;
    const lead = raw.match(/^\s*/)?.[0] || "";
    const tail = raw.match(/\s*$/)?.[0] || "";
    node.nodeValue = lead + translated + tail;
  }

  function translateAttributes(el) {
    if (!enabled() || !el || el.nodeType !== Node.ELEMENT_NODE || isOurUi(el)) return;
    for (const attr of ["placeholder", "title", "aria-label", "aria-description", "data-tooltip"]) {
      const value = el.getAttribute?.(attr);
      if (!value) continue;
      const key = norm(value);
      let translated = null;
      if (Object.prototype.hasOwnProperty.call(ATTR, key)) {
        translated = getMode() === "zh" ? pureTranslation(key, ATTR[key]) : ATTR[key];
      } else translated = translateString(value);
      if (translated && translated !== value) el.setAttribute(attr, translated);
    }
  }

  function nativeValueSetter(input, value) {
    const proto = input instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    const setter = Object.getOwnPropertyDescriptor(proto, "value")?.set;
    if (setter) setter.call(input, value); else input.value = value;
  }

  function comboboxSourceValue(input) {
    return input.dataset.wangpZhSourceValue || input.value || input.getAttribute("value") || "";
  }

  function restoreComboboxSource(input) {
    const source = input.dataset.wangpZhSourceValue;
    if (!source) return;
    if (input.value !== source) nativeValueSetter(input, source);
    input.dataset.wangpZhLocalized = "0";
  }

  function localizeClosedCombobox(input) {
    if (!enabled() || !input || input.nodeType !== Node.ELEMENT_NODE) return;
    const role = (input.getAttribute("role") || "").toLowerCase();
    const component = (input.getAttribute("data-testid") || input.getAttribute("data-component") || "").toLowerCase();
    const looksCombo = role === "combobox" || component.includes("dropdown") || input.closest?.('[role="combobox"]');
    if (!looksCombo || input.tagName !== "INPUT") return;
    if (input === input.ownerDocument.activeElement) return;
    if (input.type && !["text", "search", ""].includes(input.type)) return;
    const current = input.value || "";
    if (!input.dataset.wangpZhSourceValue || input.dataset.wangpZhLocalized !== "1") {
      if (current && !hasCJK(current)) input.dataset.wangpZhSourceValue = current;
    }
    const source = comboboxSourceValue(input);
    const translated = translateString(source);
    if (translated && translated !== current) {
      nativeValueSetter(input, translated);
      input.dataset.wangpZhLocalized = "1";
    }
    if (!comboboxBindings.has(input)) {
      comboboxBindings.add(input);
      const open = () => restoreComboboxSource(input);
      const close = () => setTimeout(() => localizeClosedCombobox(input), 80);
      input.addEventListener("pointerdown", open, true);
      input.addEventListener("focus", open, true);
      input.addEventListener("blur", close, true);
      input.addEventListener("change", () => {
        const raw = input.value || "";
        if (raw && !hasCJK(raw)) input.dataset.wangpZhSourceValue = raw;
        close(); scheduleModelRefresh(input.ownerDocument || document);
      }, true);
      input.addEventListener("input", () => {
        if (input === input.ownerDocument.activeElement) return;
        const raw = input.value || "";
        if (raw && !hasCJK(raw)) input.dataset.wangpZhSourceValue = raw;
        close();
      }, true);
    }
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
    fn(root); let node; while ((node = walker.nextNode())) fn(node);
  }

  function translateTree(root) {
    if (!enabled() || !root) return;
    walkNode(root, (node) => {
      if (node.nodeType === Node.TEXT_NODE) translateTextNode(node);
      else if (node.nodeType === Node.ELEMENT_NODE) {
        translateAttributes(node);
        if (node.tagName === "INPUT") localizeClosedCombobox(node);
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
      const roots = Array.from(pendingRoots); pendingRoots.clear();
      if (!roots.length && document.body) roots.push(document.body);
      for (const r of roots) try { translateTree(r); } catch (e) { console.debug("[WanGP ZH-CN] scan skipped", e); }
    });
  }

  function scheduleModelRefresh(doc) {
    if (!enabled()) return;
    [0, 120, 350, 800, 1500].forEach((delay) => setTimeout(() => {
      try { schedule(doc?.body || document.body); discoverNestedRoots(doc || document); } catch (_e) {}
    }, delay));
    scheduleAutoCapture(1000);
  }

  function observeRoot(root) {
    if (!root || observedRoots.has(root)) return;
    observedRoots.add(root);
    try { translateTree(root); } catch (e) { console.debug("[WanGP ZH-CN] initial scan skipped", e); }
    const observer = new MutationObserver((mutations) => {
      if (!enabled()) return;
      let meaningful = false;
      for (const m of mutations) {
        if (m.type === "characterData" || m.type === "attributes") { schedule(m.target); meaningful = true; }
        for (const n of m.addedNodes || []) { schedule(n); meaningful = true; }
      }
      if (meaningful) scheduleAutoCapture(1200);
    });
    try {
      observer.observe(root, {subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:["placeholder","title","aria-label","aria-description","data-tooltip","value","aria-selected","class","open"]});
    } catch (e) { console.debug("[WanGP ZH-CN] observer skipped", e); }
  }

  function iframeDocument(frame) {
    try { return frame.contentDocument || frame.contentWindow?.document || null; } catch (_e) { return null; }
  }

  function observeIframe(frame) {
    if (!frame || observedFrames.has(frame)) return;
    observedFrames.add(frame);
    const attach = () => {
      const doc = iframeDocument(frame); if (!doc?.documentElement) return;
      if (enabled()) doc.documentElement.lang = "zh-CN";
      observeRoot(doc.documentElement); discoverNestedRoots(doc);
    };
    frame.addEventListener("load", () => setTimeout(attach, 0)); attach();
  }

  function discoverNestedRoots(doc = document) {
    let all = []; try { all = Array.from(doc.querySelectorAll("*")); } catch (_e) { return; }
    for (const el of all) { if (el.shadowRoot) observeRoot(el.shadowRoot); if (el.tagName === "IFRAME") observeIframe(el); }
  }

  function getAccessibleDocuments() {
    const docs = [], seen = new Set();
    function add(doc) {
      if (!doc || seen.has(doc)) return; seen.add(doc); docs.push(doc);
      let frames = []; try { frames = Array.from(doc.querySelectorAll("iframe")); } catch (_e) {}
      for (const frame of frames) { if (!isElementVisible(frame)) continue; const child = iframeDocument(frame); if (child) add(child); }
    }
    add(document); return docs;
  }

  function isElementVisible(el) {
    if (!el || !el.isConnected) return false;
    if (el.hidden || el.closest?.("[hidden], [inert], [aria-hidden='true']")) return false;
    const details = el.closest?.("details:not([open])"); if (details && el.tagName !== "SUMMARY") return false;
    const win = el.ownerDocument?.defaultView || window; const style = win.getComputedStyle?.(el);
    if (style && (style.display === "none" || style.visibility === "hidden" || Number(style.opacity) === 0)) return false;
    const rects = el.getClientRects?.(); if (rects && rects.length === 0 && !["OPTION","OPTGROUP"].includes(el.tagName)) return false;
    return true;
  }

  function looksEnglish(v) { const s=norm(v); return !!(s && s.length>=2 && !hasCJK(s) && /[A-Za-z]{2,}/.test(s) && !/^(https?:\/\/|file:|data:|blob:)/i.test(s)); }
  function looksLikeNoise(text) {
    const s=norm(text); if (!s) return true;
    if (/^[,.;:(){}\[\]<>/\\|_+*=!?#$%^&@~-]+$/.test(s)) return true;
    if (/^[A-Za-z]:\\/.test(s) || /[\\/](?:Program Files|AppData|Users|ckpts|loras|outputs)[\\/]/i.test(s)) return true;
    if (/^(?:--|\/)[A-Za-z0-9_-]+/.test(s)) return true;
    if (/\.(?:json|safetensors|pth|pt|bin|gguf|py|js|css|md|txt|zip|whl)$/i.test(s)) return true;
    if (/^[a-z0-9]+(?:_[a-z0-9]+){1,}$/i.test(s) && !/\s/.test(s)) return true;
    if (/^[A-Fa-f0-9]{16,}$/.test(s)) return true;
    if (/^(?:and|or|of|in|for|to|by|on|with|from|as|at)$/i.test(s)) return true;
    if (/^[A-Z0-9_.+\-/]{1,15}$/.test(s) && !/\s/.test(s)) return true;
    return false;
  }

  function isInteractiveText(parent) { return !!parent?.closest?.("button,label,summary,[role='button'],[role='tab'],[role='menuitem'],[role='option'],[role='combobox'],[role='dialog'],.gradio-dropdown,.gradio-checkbox,.gradio-radio"); }
  function classifyUntranslated(text,parent) { if (isInteractiveText(parent)) return "ui"; if (text.length<=105 && (parent?.matches?.("h1,h2,h3,h4,h5,h6,p,span,div,strong,b") || parent?.closest?.("form"))) return "ui"; return "docs"; }

  const MAIN_SECTION_MAP = [[/Media Generator|媒体生成器/i,"媒体生成器 (Media Generator)"],[/Mask Generator|蒙版生成器/i,"蒙版生成器 (Mask Generator)"],[/Motion Designer|运动设计器/i,"运动设计器 (Motion Designer)"],[/Guides|引导工具/i,"引导工具 (Guides)"],[/Configuration|配置/i,"配置 (Configuration)"],[/Plugins|插件/i,"插件 (Plugins)"],[/About|关于/i,"关于 (About)"]];
  function selectedTabTexts(doc) {
    const out=[]; const nodes=Array.from(doc.querySelectorAll?.('[role="tab"][aria-selected="true"], .selected, .active') || []);
    for (const el of nodes) { if (!isElementVisible(el)) continue; const text=norm(el.textContent || el.getAttribute?.("aria-label") || ""); if (text && text.length<=80 && !out.includes(text)) out.push(text); }
    return out;
  }
  function detectMainSection(doc=document) {
    const selected=selectedTabTexts(doc); for (const text of selected) for (const [re,label] of MAIN_SECTION_MAP) if (re.test(text)) return label;
    const bodyText=norm(doc.body?.innerText || "").slice(0,1200); for (const [re,label] of MAIN_SECTION_MAP) if (re.test(bodyText)) return label; return "其他界面 (Other)";
  }
  function detectSubSection(doc, main) {
    const selected=selectedTabTexts(doc); for (const text of selected) { if (MAIN_SECTION_MAP.some(([re])=>re.test(text))) continue; if (text.length<=42 && !main.includes(text)) return text; } return "";
  }
  function activeModelSuffix(doc) {
    const main=detectMainSection(doc); if (!main.startsWith("媒体生成器")) return "";
    const values=[]; const inputs=Array.from(doc.querySelectorAll?.('input[role="combobox"]') || []);
    for (const input of inputs) { if (!isElementVisible(input)) continue; const raw=norm(input.dataset.wangpZhSourceValue || input.value || ""); if (!raw || raw.length>60 || /^Default$/i.test(raw) || /Enter here|Name for a Lora|Preset|Settings/i.test(raw)) continue; if (!values.includes(raw)) values.push(raw); if (values.length>=2) break; }
    return values.length ? values.join(" / ") : "";
  }
  function detectSectionLabel(doc=document) {
    const main=detectMainSection(doc), sub=detectSubSection(doc,main), model=activeModelSuffix(doc), pieces=[main]; if (sub && !main.includes(sub)) pieces.push(sub); if (model) pieces.push(model);
    const dialog=Array.from(doc.querySelectorAll?.('[role="dialog"], dialog[open], .modal') || []).find(isElementVisible); if (dialog) { const title=norm(dialog.querySelector?.("h1,h2,h3,h4,.title,[role='heading']")?.textContent || ""); pieces.push(title ? `弹窗：${title}` : "弹窗 / 帮助"); }
    return pieces.join(" / ");
  }

  function collectUntranslated(includeDocs=false) {
    const ui=new Set(), docs=new Set();
    for (const doc of getAccessibleDocuments()) {
      const root=doc.body || doc.documentElement; if (!root) continue;
      walkNode(root,(node)=>{ if (node.nodeType!==Node.TEXT_NODE) return; const parent=node.parentElement; if (!parent || shouldSkip(parent) || !isElementVisible(parent)) return; const text=norm(node.nodeValue || ""); if (!looksEnglish(text) || looksLikeNoise(text) || translateString(text) || text.length>700) return; const bucket=classifyUntranslated(text,parent); if (bucket==="ui") ui.add(text); else if (includeDocs) docs.add(text); });
      for (const input of Array.from(doc.querySelectorAll?.('input[role="combobox"]') || [])) { if (!isElementVisible(input)) continue; const text=norm(input.dataset.wangpZhSourceValue || input.value || ""); if (looksEnglish(text) && !looksLikeNoise(text) && !translateString(text)) ui.add(text); }
    }
    return {section:detectSectionLabel(document),ui:Array.from(ui).sort((a,b)=>a.localeCompare(b,"en")),docs:Array.from(docs).sort((a,b)=>a.localeCompare(b,"en")),timestamp:new Date().toISOString()};
  }

  function emptyAccumulator(){return{schema:2,updatedAt:null,sections:{}};}
  function loadAccumulator(){try{const p=JSON.parse(localStorage.getItem(SCAN_KEY)||"null");if(p&&p.schema===2&&p.sections&&typeof p.sections==="object")return p;}catch(_e){}return emptyAccumulator();}
  function saveAccumulator(acc){acc.updatedAt=new Date().toISOString();try{localStorage.setItem(SCAN_KEY,JSON.stringify(acc));}catch(e){console.warn("[WanGP ZH-CN] Could not save untranslated accumulator",e);}}
  function mergeUnique(base,incoming){const s=new Set(Array.isArray(base)?base:[]);for(const item of incoming||[])s.add(item);return Array.from(s).sort((a,b)=>a.localeCompare(b,"en"));}
  function addScanToAccumulator(scan){const acc=loadAccumulator(),key=scan.section||"其他界面 (Other)",target=acc.sections[key]||{ui:[],docs:[],updatedAt:null};target.ui=mergeUnique(target.ui,scan.ui);target.docs=mergeUnique(target.docs,scan.docs);target.updatedAt=scan.timestamp||new Date().toISOString();acc.sections[key]=target;saveAccumulator(acc);return acc;}
  function accumulatorCounts(acc){let sections=0,ui=0,docs=0;for(const data of Object.values(acc.sections||{})){sections++;ui+=(data.ui||[]).length;docs+=(data.docs||[]).length;}return{sections,ui,docs};}
  function formatScan(scan){const lines=[`## ${scan.section}`,"",`[UI 文本] (${scan.ui.length})`,...(scan.ui||[])];if((scan.docs||[]).length)lines.push("",`[文档 / 长说明] (${scan.docs.length})`,...(scan.docs||[]));return lines.join("\n");}
  function formatAccumulator(acc){const c=accumulatorCounts(acc),lines=["WanGP ZH-CN 未译累计报告",`Plugin v${VERSION}`,`栏目: ${c.sections} | UI: ${c.ui} | 文档: ${c.docs}`,`更新时间: ${acc.updatedAt||"-"}`,""];for(const section of Object.keys(acc.sections||{}).sort((a,b)=>a.localeCompare(b,"zh-CN"))){const d=acc.sections[section];lines.push(`## ${section}`,"",`[UI 文本] (${(d.ui||[]).length})`,...(d.ui||[]));if((d.docs||[]).length)lines.push("",`[文档 / 长说明] (${d.docs.length})`,...d.docs);lines.push("");}return lines.join("\n");}

  async function copyText(text,button){try{await navigator.clipboard.writeText(text);}catch(_e){const ta=document.createElement("textarea");ta.value=text;ta.style.position="fixed";ta.style.opacity="0";document.body.appendChild(ta);ta.select();document.execCommand("copy");ta.remove();}if(button){const old=button.textContent;button.textContent="已复制";setTimeout(()=>button.textContent=old,1100);}}
  function downloadText(filename,text){const blob=new Blob([text],{type:"text/plain;charset=utf-8"}),url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download=filename;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  function scanCurrentAndAccumulate(forceDocs=null){const includeDocs=forceDocs==null?localStorage.getItem(SCAN_DOCS_KEY)==="1":!!forceDocs,scan=collectUntranslated(includeDocs);lastCurrentScan=scan;const acc=addScanToAccumulator(scan);refreshUntranslatedPanel(scan,acc);return{scan,acc};}
  function scheduleAutoCapture(delay=900){if(localStorage.getItem(AUTO_SCAN_KEY)!=="1")return;clearTimeout(autoScanTimer);autoScanTimer=setTimeout(()=>{try{scanCurrentAndAccumulate();}catch(e){console.debug("[WanGP ZH-CN] auto capture skipped",e);}},delay);}

  function injectStyles(){if(document.getElementById("wangp-zh-cn-style"))return;const style=document.createElement("style");style.id="wangp-zh-cn-style";style.textContent=`#wangp-zh-cn-control{position:fixed;right:12px;bottom:12px;z-index:2147483646;display:flex;align-items:center;gap:3px;padding:4px;border:1px solid rgba(120,160,200,.38);border-radius:10px;background:rgba(10,18,31,.94);box-shadow:0 6px 20px rgba(0,0,0,.3);backdrop-filter:blur(9px);font-family:system-ui,"Microsoft YaHei UI",sans-serif}#wangp-zh-cn-control button{min-width:42px;border:0;border-radius:7px;padding:6px 8px;background:transparent;color:#d9e8f7;cursor:pointer;font-size:12px;line-height:1}#wangp-zh-cn-control button:hover{background:rgba(66,139,202,.22)}#wangp-zh-cn-control button.active{background:#24679c;color:#fff;font-weight:700}#wangp-zh-cn-control button:disabled{opacity:.45;cursor:default}#wangp-zh-cn-control .sep{width:1px;height:20px;margin:0 1px;background:rgba(180,210,235,.24)}#wangp-zh-cn-untranslated-panel{position:fixed;right:12px;bottom:58px;z-index:2147483647;width:min(720px,calc(100vw - 24px));max-height:78vh;box-sizing:border-box;padding:12px;border:1px solid rgba(120,160,200,.45);border-radius:12px;background:rgba(10,18,31,.985);color:#e8f2fb;box-shadow:0 12px 34px rgba(0,0,0,.42);font-family:system-ui,"Microsoft YaHei UI",sans-serif}#wangp-zh-cn-untranslated-panel .title{font-weight:800;margin-bottom:4px}#wangp-zh-cn-untranslated-panel .note{font-size:12px;opacity:.8;margin-bottom:8px}#wangp-zh-cn-untranslated-panel .toolbar,#wangp-zh-cn-untranslated-panel .actions{display:flex;align-items:center;gap:7px;flex-wrap:wrap;margin:8px 0}#wangp-zh-cn-untranslated-panel label{display:flex;align-items:center;gap:5px;font-size:12px}#wangp-zh-cn-untranslated-panel textarea{width:100%;height:min(45vh,500px);resize:vertical;box-sizing:border-box;padding:9px;border:1px solid rgba(120,160,200,.34);border-radius:8px;background:#07111e;color:#e8f2fb;font:12px/1.45 ui-monospace,Consolas,monospace}#wangp-zh-cn-untranslated-panel button{border:1px solid rgba(120,160,200,.38);border-radius:7px;padding:6px 10px;background:#173755;color:#fff;cursor:pointer}#wangp-zh-cn-untranslated-panel button:hover{background:#23527e}#wangp-zh-cn-untranslated-panel button.danger{background:#5b2630}#wangp-zh-cn-untranslated-panel .counts{font-size:12px;opacity:.9;padding:4px 0}#wangp-zh-cn-untranslated-panel .view-tabs button.active{background:#24679c;font-weight:700}`;document.head.appendChild(style);}
  function refreshUntranslatedPanel(scan=lastCurrentScan,acc=loadAccumulator()){const panel=document.getElementById("wangp-zh-cn-untranslated-panel");if(!panel)return;const view=panel.dataset.view||"current",c=accumulatorCounts(acc);panel.querySelector(".title").textContent=scan?`未译采集：${scan.section}`:"未译采集";panel.querySelector(".counts").textContent=scan?`当前：UI ${scan.ui.length} / 文档 ${scan.docs.length} ｜ 累计：${c.sections} 个栏目，UI ${c.ui} / 文档 ${c.docs}`:`累计：${c.sections} 个栏目，UI ${c.ui} / 文档 ${c.docs}`;panel.querySelector("textarea").value=view==="all"?formatAccumulator(acc):(scan?formatScan(scan):"尚未扫描当前页面。\n点击“扫描当前并累计”开始。");for(const btn of panel.querySelectorAll(".view-tabs button"))btn.classList.toggle("active",btn.dataset.view===view);}
  function showUntranslatedPanel(){let panel=document.getElementById("wangp-zh-cn-untranslated-panel");if(panel){panel.remove();return;}injectStyles();panel=document.createElement("div");panel.id="wangp-zh-cn-untranslated-panel";panel.dataset.view="current";panel.innerHTML=`<div class="title">未译采集</div><div class="note">按当前栏目 / 模型分组并持久累计。切到其他页面后不会清空，最后可一次性复制或导出。</div><div class="toolbar"><label><input id="wangp-zh-include-docs" type="checkbox"> 包含文档 / 长说明</label><label><input id="wangp-zh-auto-scan" type="checkbox"> 自动累计（切换栏目 / 模型后自动记录）</label></div><div class="view-tabs"><button data-view="current" class="active">当前页面</button><button data-view="all">累计结果</button></div><div class="counts"></div><textarea readonly></textarea><div class="actions"></div>`;const includeDocs=panel.querySelector("#wangp-zh-include-docs");includeDocs.checked=localStorage.getItem(SCAN_DOCS_KEY)==="1";includeDocs.onchange=()=>localStorage.setItem(SCAN_DOCS_KEY,includeDocs.checked?"1":"0");const autoScan=panel.querySelector("#wangp-zh-auto-scan");autoScan.checked=localStorage.getItem(AUTO_SCAN_KEY)==="1";autoScan.onchange=()=>{localStorage.setItem(AUTO_SCAN_KEY,autoScan.checked?"1":"0");if(autoScan.checked)scanCurrentAndAccumulate();};for(const btn of panel.querySelectorAll(".view-tabs button"))btn.onclick=()=>{panel.dataset.view=btn.dataset.view;refreshUntranslatedPanel();};const actions=panel.querySelector(".actions"),scanBtn=document.createElement("button"),copyCurrent=document.createElement("button"),copyAll=document.createElement("button"),exportAll=document.createElement("button"),clear=document.createElement("button"),close=document.createElement("button");scanBtn.textContent="扫描当前并累计";scanBtn.onclick=()=>scanCurrentAndAccumulate();copyCurrent.textContent="复制当前";copyCurrent.onclick=()=>copyText(lastCurrentScan?formatScan(lastCurrentScan):"",copyCurrent);copyAll.textContent="复制累计";copyAll.onclick=()=>copyText(formatAccumulator(loadAccumulator()),copyAll);exportAll.textContent="导出累计 .txt";exportAll.onclick=()=>downloadText(`WanGP-untranslated-${new Date().toISOString().slice(0,10)}.txt`,formatAccumulator(loadAccumulator()));clear.className="danger";clear.textContent="清空累计";clear.onclick=()=>{if(!confirm("确认清空所有已累计的未译记录？此操作只清除浏览器本地扫描记录，不会影响 WanGP。"))return;localStorage.removeItem(SCAN_KEY);lastCurrentScan=null;refreshUntranslatedPanel(null,emptyAccumulator());};close.textContent="关闭";close.onclick=()=>panel.remove();actions.append(scanBtn,copyCurrent,copyAll,exportAll,clear,close);document.body.appendChild(panel);scanCurrentAndAccumulate();}
  function addModeControl(){if(document.getElementById("wangp-zh-cn-control"))return;injectStyles();const wrap=document.createElement("div");wrap.id="wangp-zh-cn-control";const mode=getMode();for(const [value,label,title] of [["zh","中文","纯中文"],["bi","中英","中文 + 英文技术术语"],["en","EN","原始英文"]]){const btn=document.createElement("button");btn.type="button";btn.textContent=label;btn.title=title;if(value===mode)btn.classList.add("active");btn.onclick=()=>setMode(value);wrap.appendChild(btn);}const sep=document.createElement("span");sep.className="sep";wrap.appendChild(sep);const missing=document.createElement("button");missing.id="wangp-zh-cn-untranslated";missing.type="button";missing.textContent="未译";missing.title="扫描并累计当前栏目仍未覆盖的英文文本";missing.disabled=mode==="en";missing.onclick=showUntranslatedPanel;wrap.appendChild(missing);document.body.appendChild(wrap);}
  function bindGlobalRefreshEvents(){const handler=(event)=>{const target=event.target;if(target?.closest?.("#wangp-zh-cn-control, #wangp-zh-cn-untranslated-panel"))return;if(event.type==="change"||target?.getAttribute?.("role")==="tab"||target?.closest?.('[role="tab"], [role="option"], button'))scheduleModelRefresh(target?.ownerDocument||document);};document.addEventListener("change",handler,true);document.addEventListener("click",handler,true);}
  function boot(){const mode=getMode();if(mode!=="en")document.documentElement.lang="zh-CN";addModeControl();bindGlobalRefreshEvents();if(mode!=="en"){observeRoot(document.documentElement);discoverNestedRoots(document);[150,450,900,1600,2800,5000,8000].forEach((delay)=>setTimeout(()=>{schedule(document.body);discoverNestedRoots(document);},delay));setInterval(()=>discoverNestedRoots(document),5000);if(localStorage.getItem(AUTO_SCAN_KEY)==="1")scheduleAutoCapture(1800);}console.info(`[WanGP ZH-CN] localization v${VERSION} active; mode=${mode}`);}
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",boot,{once:true});else boot();
})();
