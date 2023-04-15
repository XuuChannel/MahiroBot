#插件示例
import time
from core import message
from core import bot

mahiroModuleInfo = {
    "name":"MahiroTime",
    "version":1.0,
    "type":"trigger",#trigger/background
    "condition":["Command"],#Command/Event/Plain/At/Quote/etc.
    "command":["time"],
    #"event":["NudgeEvent"],
    "permission":False,
    "target":"group"#group/friend/target
}

def mahiroModule(inbound:message.Chain,bot:bot.Bot)->None:
    rep = message.Chain()
    rep.setTarget(Group = inbound.target["group"])
    rep.add(message.Plain("现在的时间是 "+time.asctime()+" 喵"))
    rep.send(bot)