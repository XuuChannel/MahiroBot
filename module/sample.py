#插件示例
import time
from core import message
from core import bot

mahiroModuleInfo = {
    "name":"MahiroTime",
    "version":1.0,
    "type":"trigger",#trigger/background;目前只有trigger可用
    "condition":"Command",#Command/Event/Plain/At;Event时permission\target无效
    "command":["time"],
    #"event":["NudgeEvent"],
    "permission":False,
    "target":"group"#group/friend/target/all
}

def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    rep = message.Chain()
    rep.setTarget(Group = inbound.target["group"])
    rep.add(message.Plain("现在的时间是 "+time.asctime()+" 喵"))
    rep.send(bot)