#插件示例 UNFINISHED
import time
from core import message

mahiroModuleInfo = {
    "name":"MahiroTime",
    "version":1.0,
    "type":"trigger",#trigger/background
    "condition":["Command"],#Command/Plain/At/Quote/etc.
    "command":["time"],
    "permission":False,
    "target":"group"#group/friend/target
}

def mahiroModule(inbound,bot):
    rep = message.Chain()
    rep.setTarget(Group = inbound.sender["group"])
    rep.add(message.Plain("现在的时间是 "+time.asctime()+" 喵"))
    rep.send(bot)
    return True
