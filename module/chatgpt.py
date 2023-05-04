#模块使用方法：
#   安装依赖库:python -m pip install --upgrade revChatGPT
#   浏览器登陆openai网站后 访问https://chat.openai.com/api/auth/session 将内容复制下来保存为openai_token.json 存放到data文件夹中
#   注意 保存下来的token具有使用期限
from revChatGPT.V1 import Chatbot
from core import message
from core import bot
import json
import logging
import _thread,time

mahiroModuleInfo = {
    "name":"MahiroGPT",
    "version":0.3,
    "type":"trigger",
    "condition":"Command",
    "command":["chat"],
    "permission":True,
    "target":"target"
}

try:
    f = open("./data/openai_token.json","r",encoding="utf-8")
    tokeninfo = json.loads(f.read())
    f.close()
except:
    tokeninfo = {"accessToken":"null"}
chatbot = Chatbot(config={
  "access_token":tokeninfo["accessToken"]
})
cLock = _thread.allocate_lock()
logging.info("Module MahiroGPT INIT completed.")

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
        for data in chatbot.ask(prompt):response = data
        if(len(response["message"])>=650):raise Exception()
        inbound.add(message.Plain("[请谨慎使用 请求过多会被ban]\nReply to "+bot.fetchMemberInfo(bot.target,inbound.target["id"])["nickname"]+" :\n"))
        inbound.add(message.Plain(response["message"]))
        inbound.send(bot)
    except Exception as e:
        logging.error(e)
        inbound.chainClear()
        inbound.add(message.Plain("""机盖宁温馨提示: OpenAI API 返回错误喵
这可能是由于以下原因造成的喵：
-账号配置的token错误或有效期到期
-短时间请求次数过多
-ChatGPT返回的消息过长
-网络错误"""))
        inbound.send(bot)
    cLock.release()