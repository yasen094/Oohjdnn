"""
نقطة دخول البوت - مخصصة لـ Pterodactyl / ACLClouds
يشغّل Flask + الهايرايز بوت بشكل متواصل
"""
import sys
import os

# إضافة مجلد البوت لمسار الاستيراد
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# التحقق من إصدار Python
if sys.version_info < (3, 10):
    print("❌ يتطلب Python 3.10 أو أحدث")
    sys.exit(1)

if sys.version_info >= (3, 11):
    print(f"⚠️ تحذير: Python {sys.version_info.major}.{sys.version_info.minor} غير مدعوم رسمياً")
    print("⚠️ يُنصح باستخدام Python 3.10")

print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

# تثبيت المكتبات الناقصة تلقائياً عند الحاجة
def install_requirements():
    import subprocess
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(req_file):
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "--prefix", ".local",
                "-r", req_file,
                "-q"
            ])
        except Exception as e:
            print(f"⚠️ تحذير في تثبيت المكتبات: {e}")

try:
    from highrise import BaseBot
except ImportError:
    print("📦 تثبيت المكتبات المطلوبة...")
    install_requirements()

# تشغيل البوت الرئيسي (حلقة مستمرة — لا تخرج)
if __name__ == "__main__":
    # استيراد وتشغيل run.py مباشرة
    import importlib.util
    run_path = os.path.join(os.path.dirname(__file__), "run.py")
    spec = importlib.util.spec_from_file_location("run", run_path)
    run_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(run_module)

    # تشغيل الخادم والبوت
    run_module.WebServer().keep_alive()
    bot_runner = run_module.RunBot()
    bot_runner.run_loop()
