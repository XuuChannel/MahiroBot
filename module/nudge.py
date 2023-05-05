from core import message
from core import bot
import time,_thread

mahiroModuleInfo = {
    "name":"MahiroNudge",
    "version":2.0,
    "type":"trigger",
    "condition":"Event",
    "event":["NudgeEvent"],
}

cLock = _thread.allocate_lock()
startTime = int(time.time())
nudgeCount = 0

def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    global cLock,startTime,nudgeCount
    while(cLock.locked()):
        time.sleep(0.1)
    cLock.acquire()
    ret = message.Chain()
    if(evinbound.content["subject"]["kind"]=="Group" and evinbound.content["subject"]["id"]==bot.target):
        currentTime = int(time.time())
        if(currentTime-startTime<=90):
            nudgeCount+=1
        else:
            nudgeCount=0
        if(nudgeCount>=5):
            nudgeCount=0
            ret.setTarget(Group=bot.target)
            ret.add(message.Plain("男同别戳了"))
            ret.send(bot)
            ret.chainClear()
        startTime=currentTime
    if(evinbound.content["target"]==bot.account and evinbound.content["subject"]["kind"]=="Group"):
        ret.setTarget(Group=evinbound.content["subject"]["id"])
        ret.add(message.At(evinbound.content["fromId"]))
        ret.add(message.Plain(" 喵"))
        ret.send(bot)
        ret.chainClear()
    cLock.release()