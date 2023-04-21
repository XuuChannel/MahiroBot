from core import message
from core import bot
import json
import logging
import _thread
import time
import os
import base64
import requests
import hashlib

mahiroModuleInfo = {
    "name":"MahiroClassic",
    "version":1.0,
    "type":"trigger",
    "condition":"Command",
    "command":["入典","出典","语录入典","典"],
    "permission":False,
    "target":"target"
}

classicList = []
cLock = _thread.allocate_lock()
if(os.path.exists("./data/classic")==False):
    os.mkdir("./data/classic")
try:
    f = open("./data/classic/classic.json","r", encoding="utf-8")
    classicList = json.load(f)["list"]
    f.close()
except FileNotFoundError:
    f = open("./data/classic/classic.json","w", encoding="utf-8")
    s = {"list":[]}
    json.dump(s, f, ensure_ascii=False)
    f.close()
logging.info("Module MahiroClassic INIT succeed.")

def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    global cLock
    while(cLock.locked()):
        time.sleep(0.1)
    cLock.acquire()
    if(inbound.commandCheck("入典")==True and bot.perm.Check(inbound.target["id"])<=1):
        classicIn(bot,inbound,False)
    elif(inbound.commandCheck("语录入典")==True and bot.perm.Check(inbound.target["id"])<=1):
        classicIn(bot,inbound,True)
    elif(type(inbound.commandCheck("出典",True))==str and bot.perm.Check(inbound.target["id"])==0):
        pass
    elif(type(inbound.commandCheck("出典",True))!=str and bot.perm.Check(inbound.target["id"])==0):
        inbound.chainClear()
        inbound.add(message.Plain("机盖宁温馨提示：缺少参数喵"))
        inbound.send(bot)
    elif(inbound.commandCheck("典")==True):
        pass
    elif(type(inbound.commandCheck("典"))==str):
        pass
    else:
        inbound.chainClear()
        inbound.add(message.Plain("机盖宁温馨提示：您配吗"))
        inbound.send(bot)
    cLock.release()

def classicIn(b:bot.Bot,msgin:message.Chain,nameFlag:bool)->None:
    global classicList
    if(msgin.quoteRead()==None):
        msgin.chainClear()
        msgin.add(message.Plain("机盖宁温馨提示：您并没有引用任何内容喵"))
        msgin.send(bot)
        return None
    msgread = b.fetchByID(msgin.quoteRead()["messageID"],msgin.quoteRead()["target"])
    if(msgread!=None):
        classic = {"id":msgread.target["id"],"isNamed":nameFlag,"hash":None,"chain":None}
        msgread.quoteDel()
        if(len(msgread.content)==0):
            msgin.chainClear()
            msgin.add(message.Plain("机盖宁温馨提示：引用的内容不在支持范围喵"))
            msgin.send(bot)
            return None
        for i in msgread.content:
            if(i["type"]=="Image" or i["type"]=="Voice"):
                u = i["url"]
                i.clear()
                try:
                    i["base64"] = base64.b64encode(requests.get(u).content).decode()
                except:
                    msgin.chainClear()
                    msgin.add(message.Plain("机盖宁温馨提示：读取引用消息失败喵"))
                    msgin.send(bot)
                    return None
        classchain = json.dumps(msgread.content,ensure_ascii=False)
        classic["hash"] = hashlib.sha256(classchain.encode()).hexdigest()
        if(len(classicList)!=0):
            for i in classicList:
                if(i["hash"]==classic["hash"]):
                    msgin.chainClear()
                    msgin.add(message.Plain("机盖宁温馨提示：消息重复了喵"))
                    msgin.send(bot)
                    return None
            #unfinished
