
import time
from core import bot
from core import message



b = bot.Bot()
c = message.Chain()
d = open("./test.xml","r",encoding="utf-8")
c.chain = [{"type":"Xml","xml":d.read()}]
print(c.chain)
c.send(b)
print(b.target_admin_permission)
print(b.perm_banlist)
        