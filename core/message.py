#修改:把不应该是类共有变量的变量写在init内
class Chain:
    content = []
    target = {
        "id":None,
        "group":None,
        "groupPerm":None
    }
    typename = ""
    def __del__(self):
        self.allClear()
    def __init__(self,Type:str="BotMessage",sender:dict=None,chain:list=None):
        self.typename = Type
        if(Type!="BotMessage"):
            self.target["id"]=sender["id"]
        if("Group" in Type or "Temp" in Type):
            self.target["group"] = sender["group"]["id"]
            self.target["groupPerm"] = sender["permission"]
        if(chain!=None):self.__chainInit(chain)
    def setTarget(self,ID:int=None,Group:int=None):
        if(ID!=None):self.target["id"] = ID
        if(Group!=None):self.target["group"] = Group
    def __chainInit(self,chain):
        for msg in chain:
            if(msg["type"]=="Plain" or msg["type"]=="Quote" or msg["type"]=="At" or msg["type"]=="AtAll" or msg["type"]=="Image" or msg["type"]=="Voice"):
                self.content.append(msg)
        self.chainLocalize()
    def chainLocalize(self):#UNFINISHED
        if(self.typename=="BotMessage"):
            return False
        else:
            #UNFINISHED
            return True
    def chainClear(self):
        self.content.clear()
    def allClear(self):
        self.chainClear()
        self.target = {
        "id":None,
        "group":None,
        "groupPerm":None
        }
        self.typename = ""
    def add(self,contentClass):
        self.content.append(contentClass.content)
    def send(self,botClass):
        if(type(botClass).__name__ == "Bot"):
            if(self.target["group"]!=None):
                botClass.groupSend(self.content,self.target["group"])
                self.allClear()
                return True
            if(self.target["id"]!=None):
                botClass.friendSend(self.content,self.target["id"])
                self.allClear()
                return True
#UNFINISHED:关键词检测 关键元素匹配

class Event:
    content = {}
    typename = ""
    def __init__(self,eventsIn):
        self.content = eventsIn
        self.typename = self.content["type"]
#Future:群/bot事件信息分类解析

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
