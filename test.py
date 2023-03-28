
import time
from core import bot
from core import message



b = bot.Bot()
while(1):
    time.sleep(0.5)
    i = b.fetchMessage(True)
    if(i!=None and i.__class__.__name__=="Chain"):
        c = message.Chain()
        c.add(message.Plain(str(i.sender["perm"])))
        c.send(b)

        

        