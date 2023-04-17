#依托够使
#插件加载 管理 触发 UNFINISHED
from core import message
from core import bot
import logging
import os
import importlib
import sys
import time
import threading
import toml

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
        def __init__(self) -> None:
            self.versionMessage = toml.load("./version.toml")
        def mahiroModule(self,bot:bot.Bot,inbound:message.Chain)->None:
            #Future:后台常驻类模块相关
            #UNFINISHED:权限管理 关于 帮助 模块管理
            pass

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
                        threading.Thread(self.mlist[mnum].mahiroModule(bot=b,evinbound=msg)).run()
    def __subprocess(self,b:bot.Bot,msg:message.Chain,mnum:int)->None:
        match self.mlist[mnum].mahiroModuleInfo["condition"]:
            case "Command":
                for w in self.mlist[mnum].mahiroModuleInfo["command"]:
                    if(msg.commandCheck(w)==True):
                        logging.info("Module triggered. "+self.mlist[mnum].mahiroModuleInfo["name"])
                        if(mnum!=0):threading.Thread(self.mlist[mnum].mahiroModule(bot=b,inbound=msg)).run()
                        else:self.mlist[0].mahiroModule(b,msg)
            case "Plain":
                if("Plain" in msg.chainRead()["containObjs"]):
                    logging.info("Module triggered. "+self.mlist[mnum].mahiroModuleInfo["name"])
                    if(mnum!=0):threading.Thread(self.mlist[mnum].mahiroModule(bot=b,inbound=msg)).run()
                    else:self.mlist[0].mahiroModule(b,msg)
            case "At":
                if(msg.atRead()!=None and b.account in msg.atRead()):
                    logging.info("Module triggered. "+self.mlist[mnum].mahiroModuleInfo["name"])
                    if(mnum!=0):threading.Thread(self.mlist[mnum].mahiroModule(bot=b,inbound=msg)).run()
                    else:self.mlist[0].mahiroModule(b,msg)