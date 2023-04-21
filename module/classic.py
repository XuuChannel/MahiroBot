#先测试下线程锁
from core import message
from core import bot
import json
import logging
import _thread

mahiroModuleInfo = {
    "name":"MahiroClassic",
    "version":1.0,
    "type":"trigger",
    "condition":"Command",
    "command":["入典","出典","语录入典","典"],
    "permission":True,
    "target":"target"
}

initFlag = False
classicList = []
cLock = _thread.allocate_lock()

def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    global classicList
    global initFlag
    if(initFlag == False):
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
        initFlag = True