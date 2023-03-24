
import time
from func import bot
from func import message



b = bot.Bot()
c = message.Chain()
c.add(message.Plain("BotStartup"))
c.send(b)
while 1:
    time.sleep(0.1)
    i = b.fetchMessage()
    if(i!=None):
        k = i.chain
        i.send(b)
        i.chain = k
        print(i.sender)
        j = i.read()
        while(j!=None):
            print(j)
            j = i.read()
        print("\n")
        