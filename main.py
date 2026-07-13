"""
Entry point for Pterodactyl / ACLClouds hosting
Runs the Highrise bot from Fgb564/bot/
"""
import sys
import os

# إضافة مسار المكتبات المحلية (Pterodactyl يثبّت في .local)
_local_packages = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".local", "lib", "python3.10", "site-packages")
if os.path.exists(_local_packages):
    sys.path.insert(0, _local_packages)

# مسار مجلد البوت
BOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Fgb564", "bot")

if not os.path.exists(BOT_DIR):
    # محاولة ثانية: إذا كانت الملفات في نفس المجلد
    BOT_DIR = os.path.dirname(os.path.abspath(__file__))

# إضافة مسار البوت لـ Python path
sys.path.insert(0, BOT_DIR)
os.chdir(BOT_DIR)  # تغيير مجلد العمل لمجلد البوت

print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print(f"📂 مجلد البوت: {BOT_DIR}")

# تشغيل البوت
import importlib.util

run_path = os.path.join(BOT_DIR, "run.py")
spec = importlib.util.spec_from_file_location("run", run_path)
run_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_module)

run_module.WebServer().keep_alive()
bot_runner = run_module.RunBot()
bot_runner.run_loop()
