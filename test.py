import time
import _thread
from core import bot
from core import message

b = bot.Bot("./config.toml")

def fetchD():
    while(1):
        time.sleep(0.5)
        msg = b.fetchMessage()
        if(msg!=None and msg.typename == "GroupMessage" and msg.target["group"] == b.target):print(msg.content)
_thread.start_new_thread(fetchD,())
while(1):
    i = input()
    j = message.Chain()
    j.setTarget(Group=b.target)
    j.add(message.Plain(i))
    j.add(message.Plain(" \n-From the New MahiroBot(beta) at "+time.asctime()))
    j.send(b)
