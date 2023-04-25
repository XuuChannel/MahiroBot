#插件安装说明
#   安装依赖: pip install psutil
from core import message
from core import bot
import psutil
import _thread,time

mahiroModuleInfo = {
    "name":"Performance",
    "version":1.0,
    "type":"trigger",
    "condition":"Command",
    "command":["P"],
    "permission":True,
    "target":"all"
}

cLock = _thread.allocate_lock()

def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    global cLock
    while(cLock.locked()):
        time.sleep(0.1)
    cLock.acquire()
    perfmessage = "以下是bot宿主机的状态信息喵\n\nCPU("+str(psutil.cpu_count(logical=False))+"C"+str(psutil.cpu_count())+"T):\n"+str(psutil.cpu_times())+"\ncpu_percent"+str(psutil.cpu_percent(interval=3,percpu=True))+"\n\nMemory:\n"+str(psutil.virtual_memory())
    inbound.chainClear()
    inbound.add(message.Plain(perfmessage))
    inbound.send(bot)
    cLock.release()
