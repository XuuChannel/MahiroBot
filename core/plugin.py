#插件加载 管理 UNFINISHED
import os
import importlib
import sys
from func import log

#初始化插件部分 UNFINISHED

def pluginload():
    files = os.listdir("./plugins/")
    d = []
    for file in files:
        if(".py" in file):
            filename = file.strip(".py")
            d.append(importlib.import_module("plugins."+filename))
    log.Print("Detected "+str(len(d))+" plugin(s).",1)
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
        

