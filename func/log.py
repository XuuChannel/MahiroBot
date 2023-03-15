#用来输出日志的一坨屎 仅限于能用
#不要问为什么没有详细说明了 我都不知道当时是怎么写出来的 脑子抽了吧大概
import toml
from threading import Lock,Thread
import time
import sys

loglevel = toml.load("./config.toml")["log_level"]
logpath = "./data/logs/"
logcount = 0
errorCount = 0
logname = ""
flock = Lock()

def tAddHead(t,l):
    if(l == 0):
        return "[ERROR] "+t
    else:
        return "[INFO] "+t

def fWrite(text):
    global logcount
    global logpath
    global logname
    flock.acquire()
    if(logcount == 0):
        logname = str(int(time.time()))
    elif(logcount >=2000):
        logcount = 0
    logcount+=1
    logfile = open(logpath+logname+".log","a+",encoding="utf-8")
    logfile.write(text+"\n")
    logfile.close()
    flock.release()
    
def Print(text,ltype=0):
    global loglevel
    global errorCount
    text = str(text)
    if(errorCount>=10):
        sys.exit()
    if(ltype == 0):
        errorCount+=1
    if(loglevel == 0):
        print(tAddHead(text,ltype))
        Thread(target=fWrite,args=(tAddHead(text,ltype),)).start()
    elif(loglevel == 1):
        if(ltype==0):
            print(tAddHead(text,ltype))
            Thread(target=fWrite,args=(tAddHead(text,ltype),)).start()
        else:
            print(tAddHead(text,ltype))
    else:
        print(tAddHead(text,ltype))