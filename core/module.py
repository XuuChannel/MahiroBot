#插件加载 管理 触发 UNFINISHED
from core import message
from core import bot
import os
import importlib
import sys
import time
import threading
import toml

class Module:
    mlist = []

    class MahiroAbout:
        mahiroModuleInfo = {
            "name":"About",
            "version":1.0,
            "type":"trigger",
            "condition":["Command"],
            "command":["about"],
            "permission":False,
            "target":"all"
        }
        versionMessage = None
        def __init__(self) -> None:
            self.versionMessage = toml.load("./version.toml")
        def MahiroModule(bot:bot.Bot)->None:
            #UNFINISHED
            pass

    def __init__(self) -> None:
        files = os.listdir("./module/")
        d = self.MahiroAbout
        self.mlist.append(d)
        for file in files:
            if(".py" in file):
                filename = file.strip(".py")
                self.mlist.append(importlib.import_module("module."+filename))