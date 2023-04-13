from core import bot
from core import message
import time
import threading
version = 3.0

logo = """
                   __                       ____            __      
 /'\_/`\          /\ \      __             /\  _`\         /\ \__   
/\      \     __  \ \ \___ /\_\  _ __   ___\ \ \L\ \    ___\ \ ,_\  
\ \ \__\ \  /'__`\ \ \  _ `\/\ \/\`'__\/ __`\ \  _ <'  / __`\ \ \/  
 \ \ \_/\ \/\ \L\.\_\ \ \ \ \ \ \ \ \//\ \L\ \ \ \L\ \/\ \L\ \ \ \_ 
  \ \_\\\\ \_\ \__/.\_\\\\ \_\ \_\ \_\ \_\\\\ \____/\ \____/\ \____/\ \__\\
   \/_/ \/_/\/__/\/_/ \/_/\/_/\/_/\/_/ \/___/  \/___/  \/___/  \/__/
                                                                    
MahiroBot v%s by Xuu [https://github.com/XuuChannel/MahiroBot]
BOOTING..."""%(str(version))

print(logo)

b=bot.Bot("./config.toml")
