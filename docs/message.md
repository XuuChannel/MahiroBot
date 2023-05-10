# message.py
注：带*号的部分仅供MahiroBot内数据交换，不应该被用户模块手动调用。
## `class Chain(Type:str,sender:dict,chain:list)`
MahiroBot的消息链类。  
*参数:
- `Type` (可选)：消息链的类型 详情请参考[这里](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/MessageType.md#%E6%B6%88%E6%81%AF%E9%93%BE%E7%B1%BB%E5%9E%8B)(type值)  
由用户模块生成的消息链为默认值 (BotMessage) ，留空即可。
- `sender` (可选)：消息链的发送者信息/回信目标。  
用户模块请使用 [`Chain.setTarget`](https://github.com/XuuChannel/MahiroBot/blob/main/docs/message.md#chainsettargetidintgroupint-none) 。
- `chain` (可选)：bot接收到的消息链。  
用户模块请留空。
### 方法
#### `Chain.setTarget(ID:int,Group:int)->None`  
设置消息链的发送者信息/回信目标。  
参数：
- `ID` (可选):目标的qq号
- `Group` (可选)：目标的qq群

#### `Chain.chainClear()->None`  
清空消息链列表。

#### `Chain.add(content)->bool`  
往消息链列表内添加消息。  
参数：
- `content` ：类型为 [MahiroBot消息类](https://github.com/XuuChannel/MahiroBot/blob/main/docs/message.md#%E4%BB%A5%E4%B8%8B%E4%B8%BAmahirobot%E6%B6%88%E6%81%AF%E7%B1%BB) 或 标准`dict`格式消息 (格式请参考[这里](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/MessageType.md#%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B))

返回值：
- `True`(成功)/`False`(失败)

#### `Chain.send(bot:bot.Bot)->None`  
向设定的目标发送此消息链。  
参数：
- `bot` ：[bot.Bot](https://github.com/XuuChannel/MahiroBot/blob/main/docs/bot.md#class-botconfigpathstr) 类

返回值：
- `True`(成功)/`False`(失败)

#### `Chain.commandCheck(comm:str,hasParam:bool)->bool/str`  
检查消息链中是否存在MahiroBot命令。  
参数：
- `comm` ：需要检查的命令（不带前缀#号）
- `hasParam` (可选)：是否包含参数 默认为False

返回值；
- `True`(是)/`False`(否)  
当`hasParam`为`True`时返回读取到的参数（字符串）

#### `Chain.chainCheck()->dict`  
返回一个包含该消息链中所有消息类型名称的列表。详见[这里](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/MessageType.md#%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B)(type值)

#### `Chain.plainRead()->str`  
返回消息链中的文字消息(字符串)。如果消息链中没有文字信息则返回`None`。

#### `Chain.imgUrlRead()->list`  
返回一个列表 包含消息链中所有图片的链接。如果消息链中没有图片消息则返回`None`。

#### `Chain.voUrlRead()->list`  
返回一个列表 包含消息链中所有语音的链接。如果消息链中没有语音消息则返回`None`。

#### `Chain.quoteRead()->dict`  
返回一个包含引用信息(Quote)的字典。如果消息链中没有此类消息则返回`None`。  
关于Quote消息 请看[这里](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/MessageType.md#quote)  
返回值：
- ```python
    dict{
        "messageID":int,#被回复消息的messageID
        "target":int    #被回复消息的好友/所在群聊
    }
    ```

#### `Chain.quoteDel()->None`  
删除消息链中所有Quote消息。

#### `Chain.atRead()->list:`  
返回一个列表 包含消息链中所有被at的用户的qq号。如果消息链中没有此类消息则返回`None`。

### 数据
#部分信息可能为None 读取时建议`try`一下。

#### `Chain.content:list`  
消息链列表。

#### `Chain.target:dict`  
消息链发送者/目标信息。  
格式:
- ```python
    dict{
        "id":int,       #用户qq号
        "group":int,    #群号
        "groupPerm":str #用户在群内的权限
    }
    ```

#### `Chain.typename:str`  
消息链的类型。

#### `Chain.messageID:int`  
消息链的messageID。

## `class Event(eventsIn:dict)`
MahiroBot的事件类。  
*参数：
- `eventsIn` ：字典格式的标准事件信息
### 数据
#### `Event.content:dict`
事件信息 格式请参考[这里](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/EventType.md)
#### `Event.typename:str`
事件名称 定义请参考[这里](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/EventType.md)(type)

>##### ↓以下为MahiroBot消息类↓

## `class Plain(text:str)`
MahiroBot文字消息类。  
参数：
- `text` ：文字信息。
### 数据
#### `Plain.content:dict`
请参考[这里](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/MessageType.md#plain)

## `class At(target:int)`
MahiroBot @消息类。  
仅群聊可使用。  
参数：
- `target` ：要at的用户qq号。
### 数据
#### `At.content:dict`
请参考[这里](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/MessageType.md#at)

## `class AtAll()`
MahiroBot @全体成员消息类。无参数。
仅群聊可使用。

## `class Image(url:str,base64:str)`
MahiroBot图片消息类。
参数：
- `url` ：图片的链接
- `base64` ：图片的base64数据
### 数据
#### `Image.content:dict`
请参考[这里](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/MessageType.md#image)

## `class Voice(url:str,base64:str)`
MahiroBot语音消息类。  
请注意 一个消息链列表中只能存在一条语音消息 同时该消息链中必须只有此条消息。  
参数：
- `url` ：语音的链接
- `base64` ：语音的base64数据
### 数据
#### `Voice.content:dict`
请参考[这里](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/MessageType.md#voice)