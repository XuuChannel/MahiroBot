#模块使用方法：
#参考https://github.com/ading2210/poe-api
#token保存为TXT文件 置于./data/

import poe
from core import message
from core import bot
import logging
import _thread,time

mahiroModuleInfo = {
    "name":"MahiroAIchat",
    "version":2.0,
    "type":"trigger",
    "condition":"Command",
    "command":["chat"],
    "permission":True,
    "target":"target"
}


f = open("./data/PoeToken.txt","r",encoding="utf-8")
tokeninfo = f.read()
f.close()

chatbot = poe.Client(tokeninfo)
cLock = _thread.allocate_lock()
logging.info("Module MahiroAIchat INIT completed.")

def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    global chatbot
    global cLock
    while(cLock.locked()):
        time.sleep(0.1)
    cLock.acquire()
    prompt = inbound.chainStrReturn()
    prompt=prompt.replace("#chat","")
    prompt=prompt.lstrip()
    inbound.chainClear()
    try:
        pd = prompt.replace("\n","")
        if(pd.isspace()==True or pd==""):raise Exception()
        response = None
        for chunk in chatbot.send_message("capybara",pd):pass
        response=chunk["text"]
        if(len(response)>=650):raise Exception()
        inbound.add(message.Plain("[请谨慎使用 请求过多会被ban]\nReply to "+bot.fetchMemberInfo(bot.target,inbound.target["id"])["nickname"]+" :\n"))
        inbound.add(message.Plain(response))
        inbound.send(bot)
    except Exception as e:
        logging.error(e)
        inbound.chainClear()
        inbound.add(message.Plain("""机盖宁温馨提示: Poe API 返回错误喵
这可能是由于以下原因造成的喵：
-账号配置的token错误或有效期到期
-短时间请求次数过多
-返回的消息过长
-网络错误"""))
        inbound.send(bot)
    cLock.release()