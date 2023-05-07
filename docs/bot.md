# bot.py
注：带*号的部分仅供MahiroBot内数据交换，不应该被用户模块手动调用。
## `class Bot(configPath:str)`
MahiroBot机器人对象。  
*初始化需传入 `configPath` 参数 (.toml配置文件的相对路径)
### 方法

*`Bot.groupSend(messageChain:list,target:int)->bool`
- 将消息链列表(messageChain)发送至指定群聊(target)  
返回值为发送结果 (True:成功 False:失败)  
用户模块请使用 message.Chain 的 [Chain.send(bot)]() 方法

*`Bot.friendSend(messageChain:list,target:int)->bool`
- 将消息链列表(messageChain)发送至指定好友(target)  
返回值为发送结果 (True:成功 False:失败)  
用户模块请使用 message.Chain 的 [Chain.send(bot)]() 方法

*`Bot.fetchMessage()->message.Chain/message.Event`
- 从api获取最新消息列表 并返回一条包装成 [message.Chain]()/[message.Event]() 的最新信息/事件。

`Bot.fetchByID(messageID:int,targetID:int)->message.Chain`
- 根据消息的messageID和好友ID/群ID (targetID) 返回一条包装成 [message.Chain]() 的信息。

`Bot.fetchMemberInfo(group:int,id:int)->dict`
- 根据群ID(group)与用户ID(id)返回群成员的个人信息。  
关于返回值的格式 请参考[这里](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/API.md#%E5%93%8D%E5%BA%94-9)

`Bot.perm.Check(id:int)->int`
- 查询用户ID(id)在MahiroBot权限系统中的信息。  
返回值：  
    - 0: 管理员(tier0)
    - 1: 高级用户(tier1)
    - 2: 普通用户(tier2)
    - 3: 黑名单用户(tier3)

*`Bot.perm.Add(id:int,tier:int)->bool`
- 将用户(id)添加为tier=1或tier=3(含义同上)  
返回值: True(成功) False(失败)

*`Bot.perm.Del(id:int)->bool`
- 将用户(id)从tier1或tier3中移除(含义同上)  
返回值: True(成功) False(失败)

*`Bot.perm.Save()`
- 将内存中的用户权限系统信息保存至/data/perm

### 数据

`Bot.account:int`  
机器人的账号ID。

`Bot.target:int`
配置文件中设定的主要群聊ID。
