#插件安装说明
#   安装依赖: pip install psutil
from core import message
from core import bot
import psutil,os
import _thread,time
#代码文件名中带有字符"p"好像无法正常识别
mahiroModuleInfo = {
    "name":"Performance",
    "version":2.0,
    "type":"trigger",
    "condition":"Command",
    "command":["P"],
    "permission":True,
    "target":"all"
}

cLock = _thread.allocate_lock()

def cpuInfo():
    cpuTimes = psutil.cpu_times()
    # 获取CPU信息中的内存信息
    def memoryInfo(memory):
        return '\n    总内存(total): '+ str(round((float(memory.total) / 1024 / 1024 / 1024), 2)) + "G"+'\n    已使用(used): '+ str(round((float(memory.used) / 1024 / 1024 / 1024), 2)) + "G"+'\n    空闲(free): '+ str(round((float(memory.free) / 1024 / 1024 / 1024), 2)) + "G"+'\n    使用率(percent): '+ str(memory.percent) + '%'
    return '物理CPU(core): '+str(psutil.cpu_count(logical=False))+'\n逻辑CPU(thread): '+str(psutil.cpu_count())+'\n虚拟内存(virtual_memory)'+memoryInfo(psutil.virtual_memory())+'\n交换内存(swap_memory)'+memoryInfo(psutil.swap_memory())

def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    global cLock
    while(cLock.locked()):
        time.sleep(0.1)
    cLock.acquire()
    pinfo = psutil.Process(os.getpid())
    perfmessage = "以下为机盖宁的进程信息喵\n\n内存占用: "+str(round(pinfo.memory_info().rss/1024/1024,2))+"MB ("+str(round(pinfo.memory_percent(),1))+"%)\nCPU占用: "+str(pinfo.cpu_percent(interval=3))+"%"
    inbound.chainClear()
    inbound.add(message.Plain(perfmessage))
    inbound.send(bot)
    perfmessage = "以下为宿主机的信息喵\n\n"+cpuInfo()
    inbound.chainClear()
    inbound.add(message.Plain(perfmessage))
    inbound.send(bot)
    cLock.release()
