#傻逼函数传参 list dict内数据的类型也需要指定吗
#不定参数又是什么玩意 麻了
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
    def __init__(self,Type:str="BotMessage",sender:dict=None,chain:list=None)->None:
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
    def setTarget(self,ID:int=None,Group:int=None)->None:
        if(ID!=None):self.target["id"] = ID
        if(Group!=None):self.target["group"] = Group
    def __chainInit(self,chain:list)->None:
        for msg in chain:
            if(msg["type"]=="Plain" or msg["type"]=="Quote" or msg["type"]=="At" or msg["type"]=="AtAll" or msg["type"]=="Image" or msg["type"]=="Voice"):
                self.content.append(msg)
            elif(msg["type"]=="Source"):
                self.messageID = msg["id"]
        self.chainLocalize()
    def chainLocalize(self)->None:#UNFINISHED
        if(self.typename=="BotMessage"):
            return False
        else:
            #UNFINISHED
            return True
    def chainClear(self)->None:
        self.content.clear()
    def add(self,contents)->bool:
        try:
            self.content.append(contents.content)
            return True
        except AttributeError:
            if(type(contents) is list):
                self.content.append(contents)
                return True
            return False   
    def send(self,botClass)->bool:
        if(self.target["group"]!=None):
            botClass.groupSend(self.content,self.target["group"])
            return True
        if(self.target["id"]!=None):
            botClass.friendSend(self.content,self.target["id"])
            return True
        return False
    def commandCheck(self,comm:str,hasParam:bool=False):#傻逼类型检查 传入类不知道咋写 摆了
        comm = "#"+comm
        for i in self.content:
            if(i["type"]=="Plain"):
                string = i["text"].strip()
                string = string.split(" ")
                if(len(string)>=1):
                    if(string[0]==comm):
                        if(len(string)>=2 and hasParam == True and string[1]!=""):
                            return string[1]
                        elif(hasParam==False):
                            return True
        return False
    def chainCheck(self)->dict:
        ret = {
            "length":len(self.content),
            "containObjs":set()
        }
        for i in self.content:
            ret["containObjs"].add(i["type"])
        return ret
    def chainRead(self,num:int)->dict:
        if(num<0 or num>=len(self.content)):return None
        return(self.content[num])
    def plainRead(self)->str:
        ret = ""
        for i in self.content:
            if(i["type"]=="Plain"):
                ret=ret+i["text"]+"\n"
        if(ret == ""):return None
        return ret
    def imgUrlRead(self)->list:
        ret = []
        for i in self.content:
            if(i["type"]=="Image" and i["url"]!=None):
                ret.append(i["url"])
        if(len(ret)==0):return None
        return ret
    def voUrlRead(self)->list:
        ret = []
        for i in self.content:
            if(i["type"]=="Voice" and i["url"]!=None):
                ret.append(i["url"])
        if(len(ret)==0):return None
        return ret
    def quoteRead(self)->dict:
        for i in self.content:
            if(i["type"]=="Quote"):
                return {"messageID":i["id"],"target":i["targetId"]}
        return None
    def quoteDel(self)->None:
        for i in self.content:
            if(i["type"]=="Quote"):
                self.content.remove(i)
        return None
    def atRead(self)->list:
        ret = []
        for i in self.content:
            if(i["type"]=="At"):
                ret.append(i["target"])
        if(len(ret)==0):return None
        return ret
    def chainStrReturn(self)->str:
        ret = ""
        for i in self.content:
            match i["type"]:
                case "Plain":
                    ret+=i["text"]
                case "Image":
                    ret+="[IMAGE]"
                case "Voice":
                    ret+="[VOICE]"
                case "At":
                    ret = ret+"@"+str(i["target"])
                case "AtAll":
                    ret+="@所有成员"
                case "Quote":
                    ret = ret+"[QUOTE "+str(i["id"])+"]"
        return ret

class Event:
    '''
    content = {}
    typename = ""
    '''
    def __init__(self,eventsIn:dict)->None:
        self.content = eventsIn
        self.typename = self.content["type"]
#Future:群/bot事件信息分类解析

class Plain:
    def __init__(self,text:str)->None:
        self.content = {"type": "Plain"}
        self.content["text"] = text
class At:
    def __init__(self,target:int)->None:
        self.content = {"type": "At"}
        self.content["target"] = target
class AtAll:
    content = {"type": "AtAll"}
class Image:
    def __init__(self,url:str=None,base64:str=None)->None:
        self.content = {"type": "Image"}
        if(url!=None):
            self.content["url"]=url
        if(base64!=None):
            self.content["base64"]=base64 
class Voice:
    def __init__(self,url:str=None,base64:str=None)->None:
        self.content = {"type": "Voice"}
        if(url!=None):
            self.content["url"]=url
        if(base64!=None):
            self.content["base64"]=base64  
#Future:把消息链的类型补全
#↓作废 不要用
class Quote:
    def __init__(self,id:int,target:int,sender:int,group:int)->None:
        self.content = {"type": "Quote"}
        self.content["id"] = id
        self.content["targetId"] = target
        self.content["senderId"] = sender
        self.content["groupId"] = group
        self.content["origin"] = [{"type":"Plain","text":""}]
        print(self.content["origin"])