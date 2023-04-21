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
import random

mahiroModuleInfo = {
    "name":"MahiroClassic",
    "version":1.0,
    "type":"trigger",
    "condition":"Command",
    "command":["入典","出典","语录入典","典","数典"],
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
    global classicList
    while(cLock.locked()):
        time.sleep(0.1)
    cLock.acquire()
    if(inbound.commandCheck("入典")==True and bot.perm.Check(inbound.target["id"])<=1):
        classicIn(bot,inbound,False)
    elif(inbound.commandCheck("语录入典")==True and bot.perm.Check(inbound.target["id"])<=1):
        classicIn(bot,inbound,True)
    elif(inbound.commandCheck("典")==True):
        if(type(inbound.commandCheck("典",True))==str):
            num = inbound.commandCheck("典",True)
            if(num.isdigit()==False):
                inbound.chainClear()
                inbound.add(message.Plain("机盖宁温馨提示：您输入的参数并非数字喵"))
                inbound.send(bot)
            else:
                num=int(num)
                classicOut(bot,num)
        else:classicOut(bot)
    elif(inbound.commandCheck("数典")==True):
        inbound.chainClear()
        inbound.add(message.Plain("当前数据库中共有 "+str(len(classicList))+" 条数据喵"))
        inbound.send(bot)
    elif(inbound.commandCheck("出典")==True and type(inbound.commandCheck("出典",True))==str and bot.perm.Check(inbound.target["id"])==0):
        num = inbound.commandCheck("出典",True)
        if(num.isdigit()==False):
            inbound.chainClear()
            inbound.add(message.Plain("机盖宁温馨提示：您输入的参数并非数字喵"))
            inbound.send(bot)
        else:
            num=int(num)
            classicDel(bot,num)
    elif(inbound.commandCheck("出典")==True and type(inbound.commandCheck("出典",True))!=str and bot.perm.Check(inbound.target["id"])==0):
        inbound.chainClear()
        inbound.add(message.Plain("机盖宁温馨提示：缺少参数喵"))
        inbound.send(bot)
    else:
        inbound.chainClear()
        inbound.add(message.Plain("机盖宁温馨提示：您配吗"))
        inbound.send(bot)
    cLock.release()

#暴力写法 内存空间嗯造
def classicIn(b:bot.Bot,msgin:message.Chain,nameFlag:bool)->None:
    global classicList
    if(msgin.quoteRead()==None):
        msgin.chainClear()
        msgin.add(message.Plain("机盖宁温馨提示：您并没有引用任何内容喵"))
        msgin.send(b)
        return None
    msgread = b.fetchByID(msgin.quoteRead()["messageID"],msgin.quoteRead()["target"])
    if(msgread!=None):
        classic = {"id":msgread.target["id"],"isNamed":nameFlag,"hash":None,"chain":None}
        msgread.quoteDel()
        if(len(msgread.content)==0):
            msgin.chainClear()
            msgin.add(message.Plain("机盖宁温馨提示：引用的内容不在支持范围喵"))
            msgin.send(b)
            return None
        for i in msgread.content:
            if(i["type"]=="Image" or i["type"]=="Voice"):
                u = i["url"]
                i.pop("url")
                try:
                    i["base64"] = base64.b64encode(requests.get(u).content).decode()
                except:
                    msgin.chainClear()
                    msgin.add(message.Plain("机盖宁温馨提示：读取引用消息失败喵"))
                    msgin.send(b)
                    return None
        classichain = json.dumps(msgread.content,ensure_ascii=False)
        classic["hash"] = hashlib.sha256(classichain.encode()).hexdigest()
        if(len(classicList)!=0):
            for i in classicList:
                if(i["hash"]==classic["hash"]):
                    msgin.chainClear()
                    msgin.add(message.Plain("机盖宁温馨提示：消息重复了喵"))
                    msgin.send(b)
                    return None
        chainname = str(int(time.time()))+".chain"
        classic["chain"] = chainname
        classicList.append(classic)
        f = open("./data/classic/"+chainname,"w", encoding="utf-8")
        f.write(classichain)
        f.close()
        f = open("./data/classic/classic.json","w", encoding="utf-8")
        s = {"list":classicList}
        json.dump(s, f, ensure_ascii=False)
        f.close()
    else:
        msgin.chainClear()
        msgin.add(message.Plain("机盖宁温馨提示：读取引用消息失败喵"))
        msgin.send(b)
        return None
    msgin.chainClear()
    msgin.add(message.Plain("批准入典喵"))
    msgin.send(b)
    return None

def classicOut(b:bot.Bot,num:int=None):
    global classicList
    msg = message.Chain()
    msg.setTarget(Group=b.target)
    if(len(classicList)==0):
        msg.add(message.Plain("机盖宁温馨提示：典库空空如也喵"))
        msg.send(b)
        return None
    if(num==None):num = random.randint(1,len(classicList))
    if(num>len(classicList) or num<1):
        msg.add(message.Plain("机盖宁温馨提示：指定数字超出范围喵"))
        msg.send(b)
        return None
    if(classicList[num-1]["isNamed"]==True):
        userinfo = b.fetchMemberInfo(b.target,classicList[num-1]["id"])
        if(userinfo!=None):msg.add(message.Plain(userinfo["nickname"]+"("+str(classicList[num-1]["id"])+") 曾经说过："))
        else:msg.add(message.Plain("某位已经退群的人("+str(classicList[num-1]["id"])+") 曾经说过："))
        msg.send(b)
        msg.chainClear()
    try:
        msg.content = json.loads(open("./data/classic/"+classicList[num-1]["chain"],"r",encoding="utf-8").read())
        msg.send(b)
        msg.chainClear()
    except Exception as e:
        msg.add(message.Plain("机盖宁温馨提示：读取错误喵"))
        msg.send(b)
        return None

def classicDel(b:bot.Bot,num:int):
    global classicList
    msg = message.Chain()
    msg.setTarget(Group=b.target)
    if(num>len(classicList) or num<1):
        msg.add(message.Plain("机盖宁温馨提示：指定数字超出范围喵"))
        msg.send(b)
        return None
    classicOut(b=b,num=num)
    time.sleep(0.1)
    try:
        os.remove("./data/classic/"+classicList[num-1]["chain"])
        classicList.pop(num-1)
        f = open("./data/classic/classic.json","w", encoding="utf-8")
        s = {"list":classicList}
        json.dump(s, f, ensure_ascii=False)
        f.close()
        msg.add(message.Plain("↑以上内容已从数据库移除喵"))
    except Exception as e:
        msg.add(message.Plain("机盖宁温馨提示：删除失败喵"))
    msg.send(b)