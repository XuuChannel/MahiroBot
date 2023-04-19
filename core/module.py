#写的依托够使
#插件加载 管理 触发 UNFINISHED
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
            "command":["about","permcheck","permadd","permdel","ban","unban","mList","mDisable","mEnable","help"],
            "permission":False,
            "target":"all"
        }
        versionMessage = None
        bootTime = None
        def __init__(self) -> None:
            version = toml.load("./version.toml")
            self.bootTime = str(datetime.datetime.utcnow())
            #启动信息还是得改改 美观一点
            self.versionMessage = "关于MahiroBot\n\nGitHub:\n https://github.com/XuuChannel/MahiroBot\n版本:\n %s\n版本说明:\n"%(version["version"])+version["info"]
            
        def mahiroModule(self,bot:bot.Bot,inbound:message.Chain)->None:
            #Future:后台常驻类模块相关
            #UNFINISHED:权限管理 关于
            if(inbound.commandCheck("about")==True):
                inbound.chainClear()
                inbound.add(message.Plain(self.versionMessage))
                inbound.send(bot)
                inbound.chainClear()
                inbound.add(message.Plain("本 MahiroBot 实例于 "+self.bootTime+" UTC 启动。"))
                inbound.send(bot)
                inbound.chainClear()

    def moduleManage(self,inbound:message.Chain,bot:bot.Bot)->None:
        #UNFINISHED:模块管理
        if(inbound.commandCheck("mList")==True):
            msg = message.Chain()
            msg.target = inbound.target
            msg.add(message.Plain("以下为bot目前装载的模块喵:(序号|名称|版本|状态)"))
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
            self.moduleManage(msg,b)
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
                        elif("all" == self.mlist[mnum].mahiroModuleInfo["target"]):
                            if(msgperm == self.mlist[mnum].mahiroModuleInfo["permission"]):self.__subprocess(b,msg,mnum)
                            elif(self.mlist[mnum].mahiroModuleInfo["permission"] == False):self.__subprocess(b,msg,mnum)
                        elif(msgtype == "target" and self.mlist[mnum].mahiroModuleInfo["target"] == "group"):
                            if(msgperm == self.mlist[mnum].mahiroModuleInfo["permission"]):self.__subprocess(b,msg,mnum)
                            elif(self.mlist[mnum].mahiroModuleInfo["permission"] == False):self.__subprocess(b,msg,mnum)
        elif(msg!=None and type(msg) is message.Event):
            for mnum in range(len(self.mlist)):
                if(mnum not in self.disablelist and self.mlist[mnum].mahiroModuleInfo["type"]=="trigger" and self.mlist[mnum].mahiroModuleInfo["condition"]=="Event"):
                    if(msg.typename in self.mlist[mnum].mahiroModuleInfo["event"]):
                        logging.info("Module triggered. "+self.mlist[mnum].mahiroModuleInfo["name"])
                        _thread.start_new_thread(self.mlist[mnum].mahiroModule,(b,None,msg,))
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