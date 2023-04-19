from core import message
from core import bot

mahiroModuleInfo = {
    "name":"权限测试",
    "version":1.1,
    "type":"trigger",
    "condition":"Command",
    "command":["pp"],
    "permission":True,
    "target":"all"
}

def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    inbound.chainClear()
    inbound.add(message.Plain("只有高级用户(t1)以上权限才可以触发本命令喵"))
    inbound.send(bot)