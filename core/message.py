
class Chain:#重写
    chain = []
    sender = {
        "id":0,
        "group":0,
        "perm":2,#0=t0,1=t1,2=none,3=banned
    }
    ReceiveFlag = False
    MessageType = ""
    def __init__(self,isReceived:bool = False,pid:int=0,group:int=0,perm:int=2):
        if(isReceived == True):
            self.sender["id"] = pid
            self.sender["group"] = group
            self.sender["perm"] = perm
            self.ReceiveFlag = True
    def senderinit(self,pid:int,group:int):
        if(self.ReceiveFlag == True):
            self.sender["id"] = pid
            self.sender["group"] = group
    def perminit(self,perm:int):
        if(self.ReceiveFlag == True):
            self.sender["perm"]=perm
    def clear(self):
        self.chain.clear()
    def add(self,contentClass):
        self.chain.append(contentClass.content)
    def send(self,botClass,target:int = 0,isGroup:bool = True):
        if(target == 0):
            botClass.GroupSend(self.chain)
        elif(isGroup == False):
            botClass.FriendSend(self.chain,target)
        else:
            botClass.GroupSend(self.chain,target)
        self.clear()
    def read(self):
        if(len(self.chain)==0):
            return None
        else:
            return self.chain.pop(0)
#UNFINISHED:关键词检测 关键元素匹配

class Event:
    content = {}
    def __init__(self,eventsIn):
        self.content = eventsIn
    #Future:群/bot事件信息

class Plain:
    content = {"type": "Plain"}
    def __init__(self,text:str):
        self.content["text"] = text
class Quote:
    content = {"type": "Quote"}
    def __init__(self,id:int):
        self.content["id"] = id
class At:
    content = {"type": "At"}
    def __init__(self,target:int):
        self.content["target"] = target
class AtAll:
    content = {"type": "AtAll"}
class Image:
    content = {"type": "Image"}
    def __init__(self,url:str=None,base64:str=None):
        if(url!=None):
            self.content["url"]=url
        if(base64!=None):
            self.content["base64"]=base64 
class Voice:
    content = {"type": "Voice"}
    def __init__(self,url:str=None,base64:str=None):
        if(url!=None):
            self.content["url"]=url
        if(base64!=None):
            self.content["base64"]=base64  
#Future:把消息链的类型补全
