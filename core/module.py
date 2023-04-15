#插件加载 管理 触发 UNFINISHED
import os
import importlib
import sys


def moduleload()->list:
    files = os.listdir("./module/")
    d = []
    for file in files:
        if(".py" in file):
            filename = file.strip(".py")
            d.append(importlib.import_module("module."+filename))
    return d