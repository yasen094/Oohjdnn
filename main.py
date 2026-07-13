"""
Entry point for Pterodactyl / ACLClouds hosting
Runs the Highrise bot WITHOUT Flask (not needed on Pterodactyl)
"""
import sys
import os
import types

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# مسار مجلد البوت
BOT_DIR = os.path.join(BASE_DIR, "Fgb564", "bot")
if not os.path.exists(BOT_DIR):
    BOT_DIR = BASE_DIR

sys.path.insert(0, BOT_DIR)
os.chdir(BOT_DIR)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# محاكاة Flask لتجنب خطأ ModuleNotFoundError
# (لا نحتاج خادم الويب على Pterodactyl)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class _FakeFlask:
    def __init__(self, *a, **kw): pass
    def route(self, *a, **kw):
        return lambda f: f
    def run(self, *a, **kw): pass

class _FakeModule(types.ModuleType):
    Flask = _FakeFlask
    def render_template(self, *a, **kw): return ""
    def jsonify(self, *a, **kw): return {}
    def __getattr__(self, name):
        return lambda *a, **kw: None

flask_mod = _FakeModule("flask")
flask_mod.Flask = _FakeFlask
flask_mod.render_template = lambda *a, **kw: ""
flask_mod.jsonify = lambda *a, **kw: {}
flask_mod.request = type("request", (), {})()
sys.modules.setdefault("flask", flask_mod)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print(f"📂 مجلد البوت: {BOT_DIR}")
print("🚀 تشغيل البوت بدون خادم الويب...")

import importlib.util

run_path = os.path.join(BOT_DIR, "run.py")
spec = importlib.util.spec_from_file_location("run", run_path)
run_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_module)

# تشغيل البوت مباشرة (بدون WebServer)
bot = run_module.RunBot()
bot.run_loop()
