from core import bot
from core import message
import time
import threading
import toml
import importlib
import os
import logging
verInfo = toml.load("./version.toml")
logo = """\033[0;33;40m
                   __                       ____            __      
 /'\_/`\          /\ \      __             /\  _`\         /\ \__   
/\      \     __  \ \ \___ /\_\  _ __   ___\ \ \L\ \    ___\ \ ,_\  
\ \ \__\ \  /'__`\ \ \  _ `\/\ \/\`'__\/ __`\ \  _ <'  / __`\ \ \/  
 \ \ \_/\ \/\ \L\.\_\ \ \ \ \ \ \ \ \//\ \L\ \ \ \L\ \/\ \L\ \ \ \_ 
  \ \_\\\\ \_\ \__/.\_\\\\ \_\ \_\ \_\ \_\\\\ \____/\ \____/\ \____/\ \__\\
   \/_/ \/_/\/__/\/_/ \/_/\/_/\/_/\/_/ \/___/  \/___/  \/___/  \/__/
                                                                    
MahiroBot %s by Xuu [https://github.com/XuuChannel/MahiroBot]
\033[0m"""%(verInfo["version"])
print(logo)

b=bot.Bot("./config.toml")

while(1):
    time.sleep(1)
    b.fetchMessage()

