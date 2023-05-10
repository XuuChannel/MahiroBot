# bot.py
注：带*号的部分仅供MahiroBot内数据交换，不应该被用户模块手动调用。
## `class Bot(configPath:str)`
MahiroBot机器人对象。  
*参数：
- `configPath` ：.toml配置文件的相对路径
### 方法

#### *`Bot.groupSend(messageChain:list,target:int)->bool`  
将消息链列表发送至指定群聊。  
参数：
- `messageChain` ：消息链列表。
- `target` ：目标qq群群号

返回值：
- `True`(成功)/`False`:(失败) 

用户模块请使用 message.Chain 的 [Chain.send(bot)](https://github.com/XuuChannel/MahiroBot/blob/main/docs/message.md#%E6%96%B9%E6%B3%95) 方法

#### *`Bot.friendSend(messageChain:list,target:int)->bool`
将消息链列表发送至指定好友。  
参数：
- `messageChain` ：消息链列表。
- `target` ：目标qq号

返回值：
- `True`(成功)/`False`:(失败) 
 
用户模块请使用 message.Chain 的 [Chain.send(bot)](https://github.com/XuuChannel/MahiroBot/blob/main/docs/message.md#%E6%96%B9%E6%B3%95) 方法

#### *`Bot.fetchMessage()->message.Chain/message.Event`  
从api获取最新消息列表 并返回一条包装成 [message.Chain](https://github.com/XuuChannel/MahiroBot/blob/main/docs/message.md#class-chaintypestrsenderdictchainlist)/[message.Event](https://github.com/XuuChannel/MahiroBot/blob/main/docs/message.md#class-eventeventsindict) 的最新消息链/事件。

#### `Bot.fetchByID(messageID:int,targetID:int)->message.Chain`  
返回一条指定的 包装成 [message.Chain](https://github.com/XuuChannel/MahiroBot/blob/main/docs/message.md#class-chaintypestrsenderdictchainlist) 的消息链。  
参数：
- `messageID` ：消息链的messageID
- `targetID` ：好友/群聊的qq号/群号

返回值：
- [`message.Chain`](https://github.com/XuuChannel/MahiroBot/blob/main/docs/message.md#class-chaintypestrsenderdictchainlist)

#### `Bot.fetchMemberInfo(group:int,id:int)->dict`  
返回指定群成员的个人信息  
参数:
- `group` ：群号
- `id` ：qq号

返回值：
- 请参考[这里](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/API.md#%E5%93%8D%E5%BA%94-9)

#### `Bot.perm.Check(id:int)->int`  
查询用户在MahiroBot权限系统中的信息。  
参数:
- `id` ：用户qq号

返回值：  
- `0`: 管理员(tier0)
- `1`: 高级用户(tier1)
- `2`: 普通用户(tier2)
- `3`: 黑名单用户(tier3)

#### *`Bot.perm.Add(id:int,tier:int)->bool`  
将用户添加为tier1或tier3(含义同上)  
参数：
- `id` ：用户qq号
- `tier` ：指定tier(1 or 3)

返回值: 
- `True`(成功)/`False`(失败)

#### *`Bot.perm.Del(id:int)->bool`
将用户从tier1或tier3中移除(含义同上)  
参数：
- `id` ：用户qq号

返回值: 
- `True`(成功)/`False`(失败)

#### *`Bot.perm.Save()`  
将内存中的用户权限系统信息保存至`/data/perm`

### 数据

#### `Bot.account:int`  
机器人的账号ID。

#### `Bot.target:int`  
配置文件中设定的主要群聊ID。