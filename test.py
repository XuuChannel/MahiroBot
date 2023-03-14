
import time
from func import bot
from func import message

from threading import Thread
import random

bot = bot.Bot()
send = message.SendAct(bot)
while(1):
    messages = message.fetchMessage(bot)
    if(len(messages)!=0):
        for m in messages:
            print(m)
    time.sleep(0.1)






