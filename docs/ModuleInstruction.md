# MahiroBot模块构建指南
本文档将简要说明如何构建一个标准的MahiroBot模块。  
请注意：由于版本迭代，本文档提供的内容有可能是**过时、不全面且错误的**。  
如有任何问题请发issue，谢谢茄子。
## 第一步
在module文件夹新建一个.py文件并打开。
>### **ここに注意！**
>module根目录下的任何.py文件都会作为MahiroBot模块被读取加载。  
>由于某些神必的原因，请不要在文件名中加入字符 "p"。会报错。
>
>导入其他人编写的模块时 只需将文件放入module文件夹后重启bot即可。
## 第二步
编写MahiroModule信息。  
```python
from core import message
from core import bot

mahiroModuleInfo = {
    "name":"MahiroTime",    #模块名称
    "version":1.1,    #模块版本 瞎几把填也行
    "type":"trigger",    #模块类型 分为条件触发和后台常驻两种 (trigger/background 目前只有trigger可用) (值为background时其余条件无效)
    "condition":"Command",    #trigger类型的触发条件:Command(命令)/Event(事件)/Plain(收到文字消息)/At(机器人被at) (值为Event时permission/target无效)
    "command":["模块的命令1","模块的命令2"],    #当condition值为Command时 在此指定(多个)触发模块的命令文字
    "event":["NudgeEvent"],    #当condition值为Event时 在此指定(多个)触发模块的事件
    "permission":False,    #指定bot是否限制低级权限用户无法触发模块
    "target":"group"    #指定模块触发范围:group/friend/target/all(群/好友/bot配置文件内指定的群聊/所有)
}
```
>### **ここに注意！**
>请务必仔细编写。否则会报错。  
>
>`command` 内填入的命令值不需要前面带#号。（实际触发时还是需要#的）  
>
>`event` 内填入的事件名称与 `Mirai-API-HTTP` 的事件名 (type) 相同。详见[此处](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/EventType.md)
## 第三步
定义模块主函数。
```python
def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    #在此编写你的模块逻辑
```
>### **ここに注意！**
>主函数会传入三个参数:  
>+ `bot` ([bot.Bot](https://github.com/XuuChannel/MahiroBot/blob/main/docs/bot.md#class-botconfigpathstr)类 机器人对象)  
>+ `inbound` ([message.Chain]()类 触发模块的消息对象 仅在触发条件为 Command/Plain/At 时传入)
>+ `evinbound` ([message.Event]()类 触发模块的事件对象 仅在触发条件为 Event 时传入)
>
>关于以上类的用法 以及 如何在主函数内调用bot内置功能和构建/发送消息链 请查阅 [MahiroBot类 与 内置函数](https://github.com/XuuChannel/MahiroBot/blob/master/docs/Class.md) (施工中) 。
>
>MahiroBot模块管理采用多线程技术，每个模块触发时都会产生一个新的线程。因此我们强烈建议在主函数外加入线程锁：  
>```python
>import _thread,time
>#在模块主函数前定义线程锁
>mLock = _thread.allocate_lock()
>#主函数内:
>   global mLock
>   while(mLock.locked()):
>       time.sleep(0.1)
>   mLock.acquire()    #上锁
>   #您的代码
>   mLock.release()    #解锁
>```
>同理 你也可以在主函数外定义模块的全局变量和函数。

以上です。