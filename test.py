import time
from core import bot
from core import message

b = bot.Bot("./config.toml")
m = [
    {
    "type":"Plain",
    "text":"这是一条测试信息喵"
    },
    {
    "type":"Image",
    "url":"https://jp.bvid.fun/directlink/sample.jpeg"
    },
    {
    "type":"Plain",
    "text":" \n-From the New MahiroBot(beta) at "+time.asctime()
    }
]
#b.groupSend(m)
i = message.Chain()
j = message.Chain()
print(i.content)
print(j.content)
i.add(message.Plain("I am \"i\""))
print(i.content)
print(j.content)
j.add(message.Plain("I am \"j\""))
print(i.content)
print(j.content)

'''
while(1):
    time.sleep(0.5)
    receive = b.fetchMessage()
    if(receive!=None and type(receive).__name__=="Chain"):
        print(receive.content)
        
'''