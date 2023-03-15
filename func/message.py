
class Chain:
    chain = []
    def clear(self):
        self.chain = []
    def add(self,contentClass):
        self.chain.append(contentClass.content)
    def read():
        #消息链解析输出 UNFINISHED
        pass

class Person:
    id = 0
    #发送/被发送者信息 权限 UNFINISHED
class Event:
    id = 0
    #群/bot事件信息 UNFINISHED\

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
'''
UNFINISHED(修改)
class AtAll(self):
        self.chain.append({"type": "AtAll"})
class Image(self,url:str=None,base64:str=None):
        imageChain = {"type": "Image"}
        if(url!=None):
            imageChain["url"]=url
        if(base64!=None):
            imageChain["base64"]=base64  
class Voice(self,url:str=None,base64:str=None):
        voiceChain = {"type": "Voice"}
        if(url!=None):
            voiceChain["url"]=url
        if(base64!=None):
            voiceChain["base64"]=base64
'''
#UNFINISHED:各个消息链类型类的读取处理
#Future:把消息链的类型补全
