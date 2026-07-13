"""
Entry point for Pterodactyl / ACLClouds hosting
"""
import sys
import os

# إضافة مسار المكتبات من /tmp/deps (يثبّتها أمر الستارتب)
sys.path.insert(0, "/tmp/deps")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# مسار مجلد البوت
BOT_DIR = os.path.join(BASE_DIR, "Fgb564", "bot")
if not os.path.exists(BOT_DIR):
    BOT_DIR = BASE_DIR

sys.path.insert(0, BOT_DIR)
os.chdir(BOT_DIR)

print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print(f"📂 مجلد البوت: {BOT_DIR}")

# تشغيل البوت
import importlib.util

run_path = os.path.join(BOT_DIR, "run.py")
spec = importlib.util.spec_from_file_location("run", run_path)
run_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_module)
