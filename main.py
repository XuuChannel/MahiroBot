from core import bot
from core import message
from core import module
import time
import toml
import os
import logging

verInfo = toml.load("./version.toml")
os.system(' ')
print("\033c","\n"*os.get_terminal_size().lines*2)
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
def barDisplay():
    sp = " " * (os.get_terminal_size().columns-len(" MahiroBot %s"%(verInfo["version"]))-len(time.asctime())-2)
    print("\033[0;37;42m MahiroBot %s"%(verInfo["version"])+sp+time.asctime()+" \033[0m",end="\r",flush=True)

b=bot.Bot("./config.toml")
mnum=module.Module()

while(1):
    time.sleep(0.5)
    mnum.moduleProcess(b)
    barDisplay()

