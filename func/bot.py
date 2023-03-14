import os
import importlib
import toml
import requests
import json
import sys
from func import log

class Bot:  #储存api地址 bot信息 密钥
    api = ""
    bot = 0
    target = 0
    session  = ""
    def __init__(self) -> None:
        #读取配置文件并尝试连接api
        configs = toml.load("./config.toml")
        self.api = configs["api_url"]+":"+str(configs["api_port"])+"/"
        self.bot = configs["bot_account"]
        self.target = configs["target_group"]
        try:
            verifyMessage = {"verifyKey": configs["api_key"]}
            verifyPost = requests.post(self.api+"verify",json.dumps(verifyMessage,ensure_ascii=False))
            sessionMessage = json.loads(verifyPost.text)
            verifyPost.close()
            if(sessionMessage["code"]!=0):
                raise Exception("SessionVerify_Error")
            bindMessage = {"sessionKey": sessionMessage["session"],"qq": self.bot}
            bindPost = requests.post(self.api+"bind",json.dumps(bindMessage,ensure_ascii=False))
            bindPost.close()
            bindResult = json.loads(bindPost.text)
            if(bindResult["code"]!=0):
                raise Exception("SessionBind_Error")
            self.session = sessionMessage["session"]
            self.success = True
            log.wprint("BotConnection: Verify & Bind success.",1)
        except Exception as e:
            log.wprint(e)
            sys.exit()

#初始化插件部分 UNFINISHED

def pluginload():
    files = os.listdir("./plugins/")
    d = []
    for file in files:
        if(".py" in file):
            filename = file.strip(".py")
            d.append(importlib.import_module("plugins."+filename))
    log.wprint("Detected "+str(len(d))+" plugin(s).",1)
    return d

class PluginLib:#UNFINISHED
    syncPlugin = []
    passPlugin = []
    stopPlugin = []
    def __init__(self) -> None:
        pluginraw = pluginload()
        for plugin in pluginraw:
            plugininfo = {}
            plugininfo["run"] = plugin
            self.syncPlugin.append(plugininfo)
        

