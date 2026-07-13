"""
Entry point for Pterodactyl / ACLClouds hosting
MyBot is defined here and registered as sys.modules["main"] so run.py finds it.
"""
import sys
import os
import types
import subprocess
import importlib.util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── تثبيت الحزم الضرورية في /tmp (لا تأكل مساحة القرص) ─────────────────
DEPS_DIR = "/tmp/deps"
os.makedirs(DEPS_DIR, exist_ok=True)
sys.path.insert(0, DEPS_DIR)

ESSENTIAL = ["highrise-bot-sdk==24.1.0", "python-dotenv"]
try:
    import highrise  # noqa
except ImportError:
    print(f"📦 تثبيت: {ESSENTIAL}")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "--quiet", "--no-cache-dir", f"--target={DEPS_DIR}"
    ] + ESSENTIAL)
    print("✅ تم التثبيت")

# ── محاكاة Flask (غير مطلوبة على Pterodactyl) ────────────────────────────
class _FakeFlask:
    def __init__(self, *a, **kw): pass
    def route(self, *a, **kw): return lambda f: f
    def run(self, *a, **kw): pass

_flask_mod = types.ModuleType("flask")
_flask_mod.Flask = _FakeFlask
_flask_mod.render_template = lambda *a, **kw: ""
_flask_mod.jsonify = lambda *a, **kw: {}
_flask_mod.request = type("request", (), {})()
sys.modules.setdefault("flask", _flask_mod)

# ── إعداد مسار البوت ─────────────────────────────────────────────────────
BOT_DIR = os.path.join(BASE_DIR, "Fgb564", "bot")
if not os.path.exists(BOT_DIR):
    BOT_DIR = BASE_DIR

sys.path.insert(0, BOT_DIR)
os.chdir(BOT_DIR)

print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print(f"📂 مجلد البوت: {BOT_DIR}")
print("🚀 تشغيل البوت بدون خادم الويب...")

# ── تعريف MyBot هنا مباشرة ───────────────────────────────────────────────
from highrise import BaseBot, User
from highrise.models import Position, AnchorPosition

from modules.user_manager import UserManager
from modules.emotes_manager import EmotesManager
from modules.responses_manager import ResponsesManager
from modules.commands_handler import CommandsHandler
from modules.position_manager import PositionManager


class MyBot(BaseBot):

    def __init__(self):
        super().__init__()
        self.user_manager      = UserManager()
        self.emotes_manager    = EmotesManager()
        self.responses_manager = ResponsesManager()
        self.position_manager  = PositionManager()
        self.commands_handler  = None
        self.connection_info   = {}
        self.cached_room_users = []
        print("🤖 MyBot جاهز للاتصال...")

    async def on_start(self, session_metadata) -> None:
        try:
            self.commands_handler = CommandsHandler(self)
            self.connection_info = {
                "room_id":      getattr(getattr(session_metadata, "room_info", None), "room_id", "unknown"),
                "user_id":      getattr(getattr(session_metadata, "user_info", None), "user_id", "unknown"),
                "connected_at": __import__("time").time(),
            }
            print("✅ البوت متصل بالغرفة!")
            print(f"   🏠 {self.connection_info['room_id']}")
            try:
                with open("bot_status.txt", "w", encoding="utf-8") as f:
                    f.write(f"CONNECTED:{__import__('time').time()}\n")
                    f.write(f"ROOM_ID:{self.connection_info['room_id']}\n")
            except Exception:
                pass
        except Exception as e:
            print(f"❌ خطأ في on_start: {e}")

    async def on_chat(self, user: User, message: str) -> None:
        try:
            if self.commands_handler:
                result = await self.commands_handler.handle_command(user, message)
                if result:
                    await self.highrise.chat(result)
        except Exception as e:
            print(f"❌ خطأ on_chat ({user.username}): {e}")

    async def on_whisper(self, user: User, message: str) -> None:
        try:
            if self.commands_handler:
                result = await self.commands_handler.handle_command(user, message, source="whisper")
                if result:
                    await self.highrise.send_whisper(user.id, result)
        except Exception as e:
            print(f"❌ خطأ on_whisper ({user.username}): {e}")

    async def on_user_join(self, user: User, position=None) -> None:
        try:
            user_info = await self.user_manager.add_user_to_room(user, self)
            print(f"👋 {user.username} دخل الغرفة")
            welcome_msg = self.responses_manager.get_welcome_response(user)
            if welcome_msg:
                await self.highrise.chat(welcome_msg)
        except Exception as e:
            print(f"❌ خطأ on_user_join ({user.username}): {e}")

    async def on_user_leave(self, user: User) -> None:
        try:
            farewell_msg = self.responses_manager.get_farewell_message(user)
            if farewell_msg:
                await self.highrise.chat(farewell_msg)
            print(f"🚪 {user.username} غادر")
        except Exception as e:
            print(f"❌ خطأ on_user_leave ({user.username}): {e}")

    async def on_user_move(self, user: User, position=None) -> None:
        try:
            if hasattr(self.user_manager, "update_user_position"):
                self.user_manager.update_user_position(user.id, position)
        except Exception:
            pass

    async def on_emote(self, user: User, emote_id: str, receiver=None) -> None:
        try:
            if self.commands_handler and hasattr(self.commands_handler, "handle_emote"):
                await self.commands_handler.handle_emote(user, emote_id, receiver)
        except Exception as e:
            print(f"❌ خطأ on_emote: {e}")

    async def on_tip(self, sender: User, receiver: User, tip) -> None:
        try:
            if self.commands_handler and hasattr(self.commands_handler, "handle_tip"):
                await self.commands_handler.handle_tip(sender, receiver, tip)
        except Exception as e:
            print(f"❌ خطأ on_tip: {e}")


# ── تسجيل هذا الملف كـ "main" في sys.modules حتى يجده run.py ────────────
_this_module = types.ModuleType("main")
_this_module.MyBot = MyBot
sys.modules["main"] = _this_module

# ── تحميل وتشغيل run.py ──────────────────────────────────────────────────
run_path = os.path.join(BOT_DIR, "run.py")
spec = importlib.util.spec_from_file_location("run", run_path)
run_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_module)

bot = run_module.RunBot()
bot.run_loop()
