import json
import os

from shared.utils.plugins import WAN2GPPlugin


PLUGIN_VERSION = "0.5.0"
ROOT = os.path.dirname(__file__)
LOCALE_PATHS = (
    os.path.join(ROOT, "locales", "zh_CN.json"),
    os.path.join(ROOT, "locales", "zh_CN_v3.json"),
    os.path.join(ROOT, "locales", "zh_CN_v4.json"),
    os.path.join(ROOT, "locales", "zh_CN_v5.json"),
)
JS_PATH = os.path.join(ROOT, "web", "localization.js")


def _load_locale_pack():
    merged = {
        "schema": 2,
        "locale": "zh-CN",
        "exact": {},
        "attributes": {},
        "patterns": [],
        "pure_overrides": {},
        "fragments": {},
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
        merged["fragments"].update(pack.get("fragments") or {})
    return merged


def _load_js(locale_json: str) -> str:
    with open(JS_PATH, "r", encoding="utf-8") as js_file:
        template = js_file.read()
    return template.replace("__LOCALE__", locale_json).replace("__PLUGIN_VERSION__", PLUGIN_VERSION)


class WanGPChineseBilingualPlugin(WAN2GPPlugin):
    """WanGP Simplified Chinese localization with Chinese/bilingual/English modes."""

    def __init__(self):
        super().__init__()
        self.name = "WanGP 简体中文 / 双语界面"
        self.version = PLUGIN_VERSION
        self.description = (
            "WanGP v13 简体中文本地化。支持纯中文 / 中英双语 / 原始英文三种模式；"
            "支持动态模型说明、帮助弹窗、同源 iframe、下拉框选中值，以及按栏目持久累计的未译扫描器。"
        )
        self.type = ["extension"]

    def setup_ui(self):
        locale_json = json.dumps(_load_locale_pack(), ensure_ascii=False)
        self.add_custom_js(_load_js(locale_json))
