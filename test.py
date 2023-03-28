
import time
from core import bot
from core import message



b = bot.Bot()
c = message.Chain()
c.add(message.Image(url="https://avatars.githubusercontent.com/u/67725421"))
print(c.chain)
c.send(b)

        