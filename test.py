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
b.groupSend(m)
