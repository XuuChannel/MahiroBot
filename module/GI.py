from core import message
from core import bot
import time,_thread

mahiroModuleInfo = {
    "name":"InviteManager",
    "version":0.1,
    "type":"trigger",
    "condition":"Event",
    "event":["BotInvitedJoinGroupRequestEvent","NewFriendRequestEvent"],
}

cLock = _thread.allocate_lock()


def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    global cLock
    while(cLock.locked()):
        time.sleep(0.1)
    cLock.acquire()
    ret = message.Chain()
    ret.setTarget(Group=bot.target)
    if(evinbound.typename=="BotInvitedJoinGroupRequestEvent"):
        bot.replyGroupInvite(eventid=evinbound.content["eventId"],fromid=evinbound.content["fromId"],groupid=evinbound.content["groupId"])
        ret.add(message.Plain("机盖宁收到一封入群邀请喵：\n群聊："+evinbound.content["groupName"]+"("+str(evinbound.content["groupId"])+")\n邀请人；"+evinbound.content["nick"]+"("+str(evinbound.content["fromId"])+")\n已自动同意喵"))
        ret.send(bot)
    elif(evinbound.typename=="NewFriendRequestEvent"):
        bot.replyFriendInvite(eventid=evinbound.content["eventId"],fromid=evinbound.content["fromId"],groupid=evinbound.content["groupId"])
        ret.add(message.Plain("机盖宁收到一封好友申请喵："+evinbound.content["nick"]+"("+str(evinbound.content["fromId"])+")\n已自动同意喵"))
        ret.send(bot)
    del ret
    cLock.release()