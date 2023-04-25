#所以我放弃了花里胡哨
from core import bot
from core import module
import time
import toml
import os

verInfo = toml.load("./version.toml")
os.system(' ')
logo = """\033[0;33m
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
m=module.Module()

while(1):
    time.sleep(0.1)
    m.moduleProcess(b)