from core import bot
from core import message
import _thread

mahiroModuleInfo = {
    "name":"MahiroSocialCredit",
    "version":1.0,
    "type":"trigger",
    "condition":"Plain",
    "permission":False,
    "target":"target"
}

cLock = _thread.allocate_lock()

def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    pass