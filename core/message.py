class Chain:
    '''
    content = []
    target = {
        "id":None,
        "group":None,
        "groupPerm":None
    }
    typename = ""
    messageID = None
    '''
    def __init__(self,Type:str="BotMessage",sender:dict=None,chain:list=None):
        self.messageID = None
        self.content = []
        self.target = {
            "id":None,
            "group":None,
            "groupPerm":None
        }
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
            elif(msg["type"]=="Source"):
                self.messageID = msg["id"]
        self.chainLocalize()
    def chainLocalize(self):#UNFINISHED
        if(self.typename=="BotMessage"):
            return False
        else:
            #UNFINISHED
            return True
    def chainClear(self):
        self.content.clear()
    def add(self,contents):
        try:
            self.content.append(contents.content)
        except AttributeError:
            if(type(contents) is list):
                self.content.append(contents)    
    def send(self,botClass):
        if(type(botClass).__name__ == "Bot"):
            if(self.target["group"]!=None):
                botClass.groupSend(self.content,self.target["group"])
                return True
            if(self.target["id"]!=None):
                botClass.friendSend(self.content,self.target["id"])
                return True
        return False
    def commandCheck(self,comm:str,hasParam:bool=False):
        comm = "#"+comm
        for i in self.content:
            if(i["type"]=="Plain"):
                string = i["text"].strip()
                string = string.splitlines(False)
                strings = string[0].split(" ")
                if(len(strings)>=1):
                    if(strings[0]==comm):
                        if(len(strings)>=2 and hasParam == True and strings[1]!=""):
                            return strings[1]
                        elif(hasParam==False):
                            return True
        return False
    def chainCheck(self):
        ret = {
            "length":len(self.content),
            "containObjs":set()
        }
        for i in self.content:
            ret["containObjs"].add(i["type"])
        return ret
    def chainRead(self,num:int):
        if(num<0 or num>=len(self.content)):return False
        return(self.content[num])
    def plainRead(self):
        pass
#UNFINISHED:关键词检测 关键元素匹配 链读取

class Event:
    '''
    content = {}
    typename = ""
    '''
    def __init__(self,eventsIn):
        self.content = eventsIn
        self.typename = self.content["type"]
#Future:群/bot事件信息分类解析

class Plain:
    def __init__(self,text:str):
        self.content = {"type": "Plain"}
        self.content["text"] = text
class Quote:
    def __init__(self,id:int):
        self.content = {"type": "Quote"}
        self.content["id"] = id
class At:
    def __init__(self,target:int):
        self.content = {"type": "At"}
        self.content["target"] = target
class AtAll:
    content = {"type": "AtAll"}
class Image:
    def __init__(self,url:str=None,base64:str=None):
        self.content = {"type": "Image"}
        if(url!=None):
            self.content["url"]=url
        if(base64!=None):
            self.content["base64"]=base64 
class Voice:
    def __init__(self,url:str=None,base64:str=None):
        self.content = {"type": "Voice"}
        if(url!=None):
            self.content["url"]=url
        if(base64!=None):
            self.content["base64"]=base64  
#Future:把消息链的类型补全
