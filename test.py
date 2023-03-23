
import time
from func import bot
from func import message



b = bot.Bot()
m = message.Chain()
t = message.Plain("1")
m.add(t)
b.GroupSend(m)
while(1):
    msg = b.fetchMessage(True)
    msgo = b.fetchMessage()
    if(msg!={} or msgo!={}):print(str(msg)+str(msgo)+"\n")
    time.sleep(0.1)