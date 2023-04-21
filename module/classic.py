from core import message
from core import bot
import json
import logging
import _thread
import time
import os

mahiroModuleInfo = {
    "name":"MahiroClassic",
    "version":1.0,
    "type":"trigger",
    "condition":"Command",
    "command":["入典","出典","语录入典","典"],
    "permission":True,
    "target":"target"
}

classicList = []
cLock = _thread.allocate_lock()

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
    global classicList
    global cLock
    while(cLock.locked()):
        time.sleep(0.1)
    cLock.acquire()
    for i in range(20):
        time.sleep(1)
        print("lockTest:"+str(i))
    cLock.release()