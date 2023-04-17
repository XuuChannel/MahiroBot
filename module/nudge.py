from core import message
from core import bot

mahiroModuleInfo = {
    "name":"MahiroNudge",
    "version":1.0,
    "type":"trigger",
    "condition":"Event",
    "event":["NudgeEvent"],
}

def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    if(evinbound.content["target"]==bot.account and evinbound.content["subject"]["kind"]=="Group"):
        ret = message.Chain()
        ret.setTarget(Group=evinbound.content["subject"]["id"])
        ret.add(message.At(evinbound.content["fromId"]))
        ret.add(message.Plain(" 喵"))
        ret.send(bot)