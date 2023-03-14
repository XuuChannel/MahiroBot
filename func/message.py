import requests
import json
from func import log

class MessageChain:
    chain = []
    def addPlain(self,text):
        self.chain.append({"type": "Plain","text": str(text)})
    def addQuote(self,id):
        self.chain.append({"type": "Quote","id": int(id)})
    def addAt(self,target):
        self.chain.append({"type": "At","target": int(target)})
    def addAtAll(self):
        self.chain.append({"type": "AtAll"})
    def addImage(self,url=None,base64=None):
        imageChain = {"type": "Image"}
        if(url!=None):
            imageChain["url"]=url
        if(base64!=None):
            imageChain["base64"]=base64  
    def addVoice(self,url=None,base64=None):
        voiceChain = {"type": "Voice"}
        if(url!=None):
            voiceChain["url"]=url
        if(base64!=None):
            voiceChain["base64"]=base64  
    #后续可以把消息链的类型补全

class SendAct:
    message = {"sessionKey":"","target":0,"messageChain":[]}
    url = ""
    errors = None   #如果读取到错误信息的话 说明你的消息链有问题
    def __init__(self,bot): #传入bot.Bot类
        self.message["sessionKey"]=bot.session
        self.message["target"]=bot.target
        self.url = bot.api
    #Group和Friend需传入message.MessageChain类
    def Group(self,messageChain,groupnum=None): #群号可选
        self.errors = None
        self.message["messageChain"]=messageChain.chain
        if(groupnum!=None):
            self.message["target"]=groupnum
        try:
            posts = requests.post(self.url+"sendGroupMessage",json.dumps(self.message,ensure_ascii=False).encode())
            if(json.loads(posts.text)["code"]!=0):
                self.errors = json.loads(posts.text)
                raise Exception(posts.text)
        except Exception as e:
            log.wprint(e)
    def Friend(self,messageChain,usernum):
        self.errors = None
        self.message["messageChain"]=messageChain.chain
        self.message["target"]=usernum
        try:
            posts = requests.post(self.url+"sendFriendMessage",json.dumps(self.message,ensure_ascii=False).encode())
            if(json.loads(posts.text)["code"]!=0):
                self.errors = json.loads(posts.text)
                raise Exception(posts.text)
        except Exception as e:
            log.wprint(e)
    #复制粘贴再加上陌生好友信息 这个可以有

#获取bot状态 操作次级api UNFINISHED

def fetchMessage(bot):
    url = bot.api+"fetchMessage?sessionKey="+bot.session
    messagelist = []
    try:
        i = json.loads(requests.get(url).text)
        if(i["code"]!=0):
            raise Exception({"code":i["code"],"msg":i["msg"]})
        messagelist = i["data"]
    except Exception as e:
        log.wprint(e)
    return messagelist
