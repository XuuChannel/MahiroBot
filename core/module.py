#写的依托够使
from core import message
from core import bot
import logging
import os
import importlib
import _thread
import toml
import datetime

class Module:
    mlist = []
    disablelist = set()

    class Manage:
        mahiroModuleInfo = {
            "name":"MahiroManage",
            "type":"trigger",
            "condition":"Command",
            "command":["about","permcheck","permadd","permdel","ban","mList","mDisable","mEnable","help","showTarget"],
            "permission":False,
            "target":"all"
        }
        versionMessage = None
        bootTime = None
        def __init__(self) -> None:
            version = toml.load("./version.toml")
            self.bootTime = str(datetime.datetime.utcnow())
            #启动信息还是得改改 美观一点
            self.versionMessage = "MahiroBot %s \nhttps://github.com/XuuChannel/MahiroBot\n版本说明:\n"%(version["version"])+version["info"]
        def mahiroModule(self,bot:bot.Bot,inbound:message.Chain)->None:
            if(inbound.commandCheck("about")==True):
                inbound.chainClear()
                inbound.add(message.Plain(self.versionMessage))
                inbound.send(bot)
                inbound.chainClear()
                inbound.add(message.Plain("本 MahiroBot 实例于 "+self.bootTime+" UTC 启动。"))
                inbound.send(bot)
                inbound.chainClear()
            #↓不知为何 会报错
            #if(inbound.commandCheck("showTarget")==True):
            #    inbound.chainClear()
            #    inbound.add(message.Chain("机盖宁当前的目标群聊为 "+str(bot.target)+" 喵"))
            #    inbound.send(bot)
            #    inbound.chainClear()
            if(inbound.commandCheck("permcheck")==True):
                if(inbound.atRead()==None):
                    checkResult=bot.perm.Check(inbound.target["id"])
                    inbound.chainClear()
                    match checkResult:
                        case 0:inbound.add(message.Plain("您的权限是 管理员(t0) 喵"))
                        case 1:inbound.add(message.Plain("您的权限是 高级用户(t1) 喵"))
                        case 2:inbound.add(message.Plain("您的权限是 普通用户(t2) 喵"))
                        case 3:inbound.add(message.Plain("您被ban了 好似喵"))
                elif(len(inbound.atRead())==1):
                    checkResult=bot.perm.Check(inbound.atRead()[0])
                    user = str(inbound.atRead()[0])
                    inbound.chainClear()
                    match checkResult:
                        case 0:inbound.add(message.Plain("用户 "+user+" 的权限是 管理员(t0) 喵"))
                        case 1:inbound.add(message.Plain("用户 "+user+" 的权限是 高级用户(t1) 喵"))
                        case 2:inbound.add(message.Plain("用户 "+user+" 的权限是 普通用户(t2) 喵"))
                        case 3:inbound.add(message.Plain("用户 "+user+" 被ban了 好似喵"))
                    if(int(user) == bot.account):
                        inbound.chainClear()
                        inbound.add(message.Plain("机盖宁的权限 任君想象喵"))
                else:
                    inbound.chainClear()
                    inbound.add(message.Plain("机盖宁温馨提示:您at的太多力 机盖宁处理不过来喵"))
                inbound.send(bot)
                inbound.chainClear()
            if(inbound.commandCheck("permadd")==True):
                if(bot.perm.Check(inbound.target["id"])!=0):
                    inbound.chainClear()
                    inbound.add(message.Plain("机盖宁温馨提示:您配吗"))
                elif(inbound.atRead()==None):
                    inbound.chainClear()
                    inbound.add(message.Plain("机盖宁温馨提示:您并没有指定任何用户喵"))
                elif(len(inbound.atRead())!=1):
                    inbound.chainClear()
                    inbound.add(message.Plain("机盖宁温馨提示:您at的太多力 机盖宁处理不过来喵"))
                elif(inbound.atRead()[0]==bot.account):
                    inbound.chainClear()
                    inbound.add(message.Plain("机盖宁温馨提示:您无法对机盖宁进行权限操作喵"))
                else:
                    user = inbound.atRead()[0]
                    result = bot.perm.Add(id=user,tier=1)
                    inbound.chainClear()
                    if(result==True):
                        inbound.add(message.Plain("已将用户 "+str(user)+" 设置为高级用户(t1)喵"))
                        bot.perm.Save()
                    else:inbound.add(message.Plain("机盖宁温馨提示:设置失败喵 该用户目前的权限并不是普通用户(t2)喵"))
                inbound.send(bot)
                inbound.chainClear()
            if(inbound.commandCheck("ban")==True):
                if(bot.perm.Check(inbound.target["id"])!=0):
                    inbound.chainClear()
                    inbound.add(message.Plain("机盖宁温馨提示:您配吗"))
                elif(inbound.atRead()==None):
                        inbound.chainClear()
                        inbound.add(message.Plain("机盖宁温馨提示:您并没有指定任何用户喵"))
                elif(len(inbound.atRead())!=1):
                    inbound.chainClear()
                    inbound.add(message.Plain("机盖宁温馨提示:您at的太多力 机盖宁处理不过来喵"))
                elif(inbound.atRead()[0]==bot.account):
                    inbound.chainClear()
                    inbound.add(message.Plain("机盖宁温馨提示:您无法对机盖宁进行权限操作喵"))
                else:
                    user = inbound.atRead()[0]
                    result = bot.perm.Add(id=user,tier=3)
                    inbound.chainClear()
                    if(result==True):
                        inbound.add(message.Plain("已将用户 "+str(user)+" 加入黑名单喵 好似喵"))
                        bot.perm.Save()
                    else:inbound.add(message.Plain("机盖宁温馨提示:设置失败喵 该用户目前的权限并不是普通用户(t2)喵"))
                inbound.send(bot)
                inbound.chainClear()
            if(inbound.commandCheck("permdel")==True):
                if(bot.perm.Check(inbound.target["id"])!=0):
                    inbound.chainClear()
                    inbound.add(message.Plain("机盖宁温馨提示:您配吗"))
                elif(inbound.atRead()==None):
                    inbound.chainClear()
                    inbound.add(message.Plain("机盖宁温馨提示:您并没有指定任何用户喵"))
                elif(len(inbound.atRead())!=1):
                    inbound.chainClear()
                    inbound.add(message.Plain("机盖宁温馨提示:您at的太多力 机盖宁处理不过来喵"))
                elif(inbound.atRead()[0]==bot.account):
                    inbound.chainClear()
                    inbound.add(message.Plain("机盖宁温馨提示:您无法对机盖宁进行权限操作喵"))
                else:
                    user = inbound.atRead()[0]
                    result = bot.perm.Del(id=user)
                    inbound.chainClear()
                    if(result==True):
                        inbound.add(message.Plain("已将用户 "+str(user)+" 设置为普通用户(t2)喵"))
                        bot.perm.Save()
                    else:inbound.add(message.Plain("机盖宁温馨提示:设置失败喵 该用户目前的权限并不是高级用户(t1)或黑名单用户(t3)喵"))
                inbound.send(bot)
                inbound.chainClear()
    def moduleManage(self,inbound:message.Chain,bot:bot.Bot)->None:
        #Future:后台常驻类模块相关
        if(inbound.commandCheck("mList")==True):
            msg = message.Chain()
            msg.target = inbound.target
            msg.add(message.Plain("以下为机盖宁目前装载的模块喵:(序号|名称|版本|状态)"))
            for i in range(1,len(self.mlist)):
                modulestr = "\n"+str(i)+" | "
                modulestr += (self.mlist[i].mahiroModuleInfo["name"]+" | v"+str(self.mlist[i].mahiroModuleInfo["version"])+" | ")
                if(i in self.disablelist):modulestr+="已禁用"
                else:modulestr+="启用中"
                msg.add(message.Plain(modulestr))
            msg.send(bot)
        if(type(inbound.commandCheck("mDisable",True)) is str):
            num = str(inbound.commandCheck("mDisable",True))
            msg = message.Chain()
            msg.target = inbound.target
            if(bot.perm.Check(inbound.target["id"])==0):
                if(num.isdigit()!=True):msg.add(message.Plain("机盖宁温馨提示:您输入的值并不是数字喵"))
                elif(int(num)>len(self.mlist)-1 or int(num)<=0):msg.add(message.Plain("机盖宁温馨提示:您输入的值超出范围了喵"))
                else:
                    num = int(num)
                    self.disablelist.add(num)
                    msg.add(message.Plain("模块 "+self.mlist[num].mahiroModuleInfo["name"]+" 已禁用喵"))
            else:
                msg.add(message.Plain("机盖宁温馨提示:您配吗"))
            msg.send(bot)
        if(type(inbound.commandCheck("mEnable",True)) is str):
            num = str(inbound.commandCheck("mEnable",True))
            msg = message.Chain()
            msg.target = inbound.target
            if(bot.perm.Check(inbound.target["id"])==0):
                if(num.isdigit()!=True):msg.add(message.Plain("机盖宁温馨提示:您输入的值并不是数字喵"))
                elif(int(num)>len(self.mlist)-1 or int(num)<=0):msg.add(message.Plain("机盖宁温馨提示:您输入的值超出范围了喵"))
                else:
                    num = int(num)
                    self.disablelist.discard(num)
                    msg.add(message.Plain("模块 "+self.mlist[num].mahiroModuleInfo["name"]+" 已启用喵"))
            else:
                msg.add(message.Plain("机盖宁温馨提示:您配吗"))
            msg.send(bot)
        if(inbound.commandCheck("help")==True):
            msg = message.Chain()
            msg.target = inbound.target
            msg.add(message.Plain("以下是各个模块可使用的命令喵\n\n"))
            msg.add(message.Plain("[无需权限|无限制] MahiroManage (系统模块):\n #about #permcheck #permadd #permdel #ban #mList #mDisable #mEnable #help #showTarget"))
            for i in range(1,len(self.mlist)):
                msgstr = "\n["
                if(self.mlist[i].mahiroModuleInfo["type"]=="background" or self.mlist[i].mahiroModuleInfo["condition"]!="Command"):
                    msgstr+=("无需权限|无限制] "+self.mlist[i].mahiroModuleInfo["name"]+" :\n 暂无可用命令")
                else:
                    if(self.mlist[i].mahiroModuleInfo["permission"]==True):msgstr+="需要高级用户权限|"
                    else:msgstr+="无需权限|"
                    match self.mlist[i].mahiroModuleInfo["target"]:
                        case "all":msgstr+="无限制] "
                        case "target":msgstr+="仅目标群聊可用] "
                        case "group":msgstr+="仅群聊可用] "
                        case "friend":msgstr+="仅好友聊天可用] "
                    msgstr+=self.mlist[i].mahiroModuleInfo["name"]
                    msgstr+=" :\n"
                    for m in self.mlist[i].mahiroModuleInfo["command"]:msgstr+=(" #"+m)
                msg.add(message.Plain(msgstr))
            msg.send(bot)

    def __init__(self) -> None:
        files = os.listdir("./module/")
        d = self.Manage()
        self.mlist.append(d)
        for file in files:
            if(".py" in file):
                filename = file.strip(".py")
                self.mlist.append(importlib.import_module("module."+filename))
                logging.info("Module detected: "+self.mlist[-1].mahiroModuleInfo["name"]+" v"+str(self.mlist[-1].mahiroModuleInfo["version"]))
        logging.info("Module INIT succeed. "+str(len(self.mlist)-1)+" module(s) detected.")
        #Future:后台常驻类模块相关
    
    def moduleProcess(self,b:bot.Bot)->None:
        msg = b.fetchMessage()
        if(msg!=None and type(msg) is message.Chain):
            msgtype = ""
            if(msg.target["group"]!=None):
                if(msg.target["group"] == b.target):msgtype = "target"
                else:msgtype = "group"
            else:msgtype = "friend"
            msgperm = False
            if(b.perm.Check(msg.target["id"])==0 or b.perm.Check(msg.target["id"])==1):msgperm = True
            for mnum in range(len(self.mlist)):
                if(mnum not in self.disablelist and self.mlist[mnum].mahiroModuleInfo["type"]=="trigger"):
                    if(self.mlist[mnum].mahiroModuleInfo["condition"]!="Event"):
                        if(msgtype == self.mlist[mnum].mahiroModuleInfo["target"]):
                            if(msgperm == self.mlist[mnum].mahiroModuleInfo["permission"]):self.__subprocess(b,msg,mnum)
                            elif(self.mlist[mnum].mahiroModuleInfo["permission"] == False):self.__subprocess(b,msg,mnum)
                            else:self.__trashCommandProcess(b,msg,mnum)
                        elif("all" == self.mlist[mnum].mahiroModuleInfo["target"]):
                            if(msgperm == self.mlist[mnum].mahiroModuleInfo["permission"]):self.__subprocess(b,msg,mnum)
                            elif(self.mlist[mnum].mahiroModuleInfo["permission"] == False):self.__subprocess(b,msg,mnum)
                            else:self.__trashCommandProcess(b,msg,mnum)
                        elif(msgtype == "target" and self.mlist[mnum].mahiroModuleInfo["target"] == "group"):
                            if(msgperm == self.mlist[mnum].mahiroModuleInfo["permission"]):self.__subprocess(b,msg,mnum)
                            elif(self.mlist[mnum].mahiroModuleInfo["permission"] == False):self.__subprocess(b,msg,mnum)
                            else:self.__trashCommandProcess(b,msg,mnum)
            self.moduleManage(msg,b)
        elif(msg!=None and type(msg) is message.Event):
            for mnum in range(len(self.mlist)):
                if(mnum not in self.disablelist and self.mlist[mnum].mahiroModuleInfo["type"]=="trigger" and self.mlist[mnum].mahiroModuleInfo["condition"]=="Event"):
                    if(msg.typename in self.mlist[mnum].mahiroModuleInfo["event"]):
                        logging.info("Module triggered. "+self.mlist[mnum].mahiroModuleInfo["name"])
                        _thread.start_new_thread(self.mlist[mnum].mahiroModule,(b,None,msg,))
    def __trashCommandProcess(self,b:bot.Bot,msg:message.Chain,mnum:int):
        if(self.mlist[mnum].mahiroModuleInfo["condition"]=="Command"):
            for w in self.mlist[mnum].mahiroModuleInfo["command"]:
                if(msg.commandCheck(w)==True):
                    msg.chainClear()
                    msg.add(message.Plain("机盖宁温馨提示:您配吗"))
                    msg.send(b)
    def __subprocess(self,b:bot.Bot,msg:message.Chain,mnum:int)->None:
        match self.mlist[mnum].mahiroModuleInfo["condition"]:
            case "Command":
                for w in self.mlist[mnum].mahiroModuleInfo["command"]:
                    if(msg.commandCheck(w)==True):
                        logging.info("Module triggered. "+self.mlist[mnum].mahiroModuleInfo["name"])
                        if(mnum!=0):_thread.start_new_thread(self.mlist[mnum].mahiroModule,(b,msg,))
                        else:self.mlist[0].mahiroModule(b,msg)
            case "Plain":
                if("Plain" in msg.chainRead()["containObjs"]):
                    logging.info("Module triggered. "+self.mlist[mnum].mahiroModuleInfo["name"])
                    if(mnum!=0):_thread.start_new_thread(self.mlist[mnum].mahiroModule,(b,msg,))
                    else:self.mlist[0].mahiroModule(b,msg)
            case "At":
                if(msg.atRead()!=None and b.account in msg.atRead()):
                    logging.info("Module triggered. "+self.mlist[mnum].mahiroModuleInfo["name"])
                    if(mnum!=0):_thread.start_new_thread(self.mlist[mnum].mahiroModule,(b,msg,))
                    else:self.mlist[0].mahiroModule(b,msg)