"""
Entry point for Pterodactyl / ACLClouds hosting
Runs the Highrise bot from Fgb564/bot/
"""
import sys
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# إضافة مسار المكتبات المحلية (Pterodactyl يثبّت في .local)
for py_ver in ["python3.10", "python3", "python"]:
    _local_pkg = os.path.join(BASE_DIR, ".local", "lib", py_ver, "site-packages")
    if os.path.exists(_local_pkg):
        sys.path.insert(0, _local_pkg)

# تثبيت المكتبات تلقائياً إذا لم تكن موجودة
REQUIRED = [
    "flask",
    "highrise-bot-sdk==24.1.0",
    "google-generativeai",
    "python-dotenv",
]

def ensure_packages():
    missing = []
    for pkg in REQUIRED:
        name = pkg.split("==")[0].replace("-", "_").lower()
        try:
            __import__(name)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"📦 تثبيت المكتبات الناقصة: {missing}")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--quiet"
        ] + missing)
        print("✅ تم تثبيت المكتبات")

ensure_packages()

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
