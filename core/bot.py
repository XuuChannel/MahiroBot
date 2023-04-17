#和message.py一样的问题 被强动态类型语言气晕.jpg 
import toml
import requests
import json
import logging
from core import message
import time

class MiraiError(Exception):#懒得改类型指定了 感觉屁用没有
    def __init__(self,errorMessage:dict):
        self.code = errorMessage["code"]
        self.msg = errorMessage["msg"]
    def __str__(self):
        return f"CODE {str(self.code)} \"{self.msg}\""

class Bot:
    errorCount = 0
    """
    __api = ""
    __session  = ""
    account = 0
    target = 0
    perm = None
    __botmsg = []
    """
    class __Perm:
        """
        t0 = []
        t1 = []
        banned = []
        """
        def __init__(self,configs)->None:
            self.t0 = []
            self.t1 = []
            self.banned = []
            self.t0 = configs["t0_users"]
            try:
                f = open("./data/perm/t1.json","r", encoding="utf-8")
                self.t1 = json.load(f)["list"]
                f.close()
            except FileNotFoundError:
                f = open("./data/perm/t1.json","w", encoding="utf-8")
                s = {"list":[]}
                json.dump(s, f, ensure_ascii=False)
                f.close()
            try:
                f = open("./data/perm/banned.json","r", encoding="utf-8")
                self.banned = json.load(f)["list"]
                f.close()
            except FileNotFoundError:
                f = open("./data/perm/banned.json","w", encoding="utf-8")
                s = {"list":[]}
                json.dump(s, f, ensure_ascii=False)
                f.close()
            logging.info("Permission INIT succeed.")
        def Check(self,id:int)->int:#0=t0,1=t1,2=none,3=banned
            for i in self.t0:
                if(i ==id):return 0
            for i in self.t1:
                if(i ==id):return 1
            for i in self.banned:
                if(i ==id):return 3
            return 2
        def Add(self,id:int,tier:int)->bool:
            idcheck = self.Check(id)
            if(tier!=1 or tier!=3 or idcheck!=2):
                return False
            elif(tier==1):
                self.t1.append(id)
                return True
            elif(tier==3):
                self.banned.append(id)
                return True
            return False
        def Del(self,id:int)->bool:
            idcheck = self.Check(id)
            match idcheck:
                case 1:
                    self.t1.remove(id)
                    return True
                case 3:
                    self.banned.remove(id)
                    return True
            return False
        def Save(self)->None:
            f = open("./data/perm/t1.json","w", encoding="utf-8")
            s = {"list":self.t1}
            json.dump(s, f, ensure_ascii=False)
            f.close()
            f = open("./data/perm/banned.json","w", encoding="utf-8")
            s = {"list":self.banned}
            json.dump(s, f, ensure_ascii=False)
            f.close()
            logging.info("Permission SAVE succeed.")
    
    def __init__(self,configPath:str)->None:
        self.__botmsg = []
    #读取配置文件并尝试连接api
        configs = toml.load(configPath)
        if(configs["event_log"] == True):logging.basicConfig(filename="./data/logs/MahiroLog_"+str(int(time.time()))+".log",format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO)
        else:logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO)
        self.__api = configs["api_url"]+":"+str(configs["api_port"])+"/"
        self.account = configs["bot_account"]
        self.target = configs["target_group"]
        message = {"verifyKey": configs["api_key"]}
        post = requests.post(self.__api+"verify",json.dumps(message,ensure_ascii=False))
        result = json.loads(post.text)
        if(result["code"]!=0):
            raise MiraiError(result)
        message = {"sessionKey": result["session"],"qq": self.account}
        self.__session = result["session"]
        post = requests.post(self.__api+"bind",json.dumps(message,ensure_ascii=False))
        result = json.loads(post.text)
        if(result["code"]!=0):
            raise MiraiError(result)
        logging.info("Bot Verify&Bind succeed.")
    #读取权限文件
        self.perm = self.__Perm(configs)

    def __del__(self)->None:
        message = {"sessionKey": self.__session,"qq": self.account}
        post = json.loads(requests.post(self.__api+"release",json.dumps(message,ensure_ascii=False)).text)
        if(post["code"]!=0):
            raise MiraiError(post)
        logging.info("Bot SessionRelease succeed.")
        #self.perm.Save()
        #为什么open会报错 气人
        
    def groupSend(self,messageChain:list,target:int=None)->bool: #群号可选
        message = {"sessionKey":self.__session,"target":self.target,"messageChain":messageChain}
        if(target!=None):
            message["target"]=target
        try:
            post = requests.post(self.__api+"sendGroupMessage",json.dumps(message,ensure_ascii=False).encode())
            if(json.loads(post.text)["code"]!=0):
                raise MiraiError(json.loads(post.text))
        except Exception as e:
            self.errorCount+=1
            if(self.errorCount>10):
                exit()
            logging.error(e)
            return False
        logging.info("Bot SendAction succeed.")
        return True
    def friendSend(self,messageChain:list,target:int)->bool:
        message = {"sessionKey":self.__session,"target":target,"messageChain":[]}
        message["messageChain"]=messageChain
        try:
            post = requests.post(self.__api+"sendFriendMessage",json.dumps(message,ensure_ascii=False).encode())
            if(json.loads(post.text)["code"]!=0):
                raise MiraiError(json.loads(post.text))
        except Exception as e:
            self.errorCount+=1
            if(self.errorCount>10):
                exit()
            logging.error(e)
            return False
        logging.info("Bot SendAction succeed.")
        return True

#Future:临时会话发送 获取bot,群,用户信息 撤回 戳一戳 账号管理 群管理

    def __fetch(self)->None:
        url = self.__api+"fetchMessage?sessionKey="+self.__session
        try:
            i = json.loads(requests.get(url).text)
            if(i["code"]!=0):
                raise MiraiError(i)
            if(len(i["data"])!=0):self.__botmsg=self.__botmsg+i["data"]
        except Exception as e:
            self.errorCount+=1
            if(self.errorCount>10):
                exit()
            logging.error(e)
    def fetchMessage(self):#输出有多种类型的该怎么指定
        self.__fetch()
        msg = {}
        try:msg = self.__botmsg.pop()
        except IndexError:return None
        if("Event" in msg["type"]):
            ret = message.Event(msg)
            logging.info("Bot FetchEvent succeed. "+ret.typename)
            return ret
        elif("Message" in msg["type"] and "Sync" not in msg["type"]):
            if(self.perm.Check(msg["sender"]["id"])==3):return None
            ret = message.Chain(msg["type"],msg["sender"],msg["messageChain"])
            logging.info("Bot FetchMessage succeed. Type="+ret.typename+" Sender="+str(ret.target["id"])+" Group="+str(ret.target["group"])+"\nMessage="+ret.chainStrReturn())
            return ret
        return None
    def fetchByID(self,messageID:int,targetID:int)->message.Chain:
        url = self.__api+"messageFromId?sessionKey="+self.__session+"&messageId="+str(messageID)+"&target="+str(targetID)
        msg = {}
        try:
            i = json.loads(requests.get(url).text)
            if(i["code"]!=0):
                raise MiraiError(i)
            if(len(i["data"])!=0):msg = i["data"]
        except Exception as e:
            self.errorCount+=1
            if(self.errorCount>10):
                exit()
            logging.error(e)
            return None
        if(self.perm.Check(msg["sender"]["id"])==3):return None
        ret = message.Chain(msg["type"],msg["sender"],msg["messageChain"])
        logging.info("Bot FetchMessage succeed. Type="+ret.typename+" Sender="+str(ret.target["id"])+" Group="+str(ret.target["group"])+"\nMessage="+ret.chainStrReturn())
        return ret