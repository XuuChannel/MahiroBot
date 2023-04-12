import toml
import requests
import json
from core import message

class MiraiError(Exception):
    def __init__(self,errorMessage):
        self.code = errorMessage["code"]
        self.msg = errorMessage["msg"]
    def __str__(self):
        return f"CODE {str(self.code)} \"{self.msg}\""

class Bot:
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
        def __init__(self,configs):
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
        def Check(self,id:int):#0=t0,1=t1,2=none,3=banned
            for i in self.t0:
                if(i ==id):return 0
            for i in self.t1:
                if(i ==id):return 1
            for i in self.banned:
                if(i ==id):return 3
            return 2
        def Add(self,id:int,tier:int):
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
        def Del(self,id:int):
            idcheck = self.Check(id)
            match idcheck:
                case 1:
                    self.t1.remove(id)
                    return True
                case 3:
                    self.banned.remove(id)
                    return True
            return False
        def Save(self):
            f = open("./data/perm/t1.json","w", encoding="utf-8")
            s = {"list":self.t1}
            json.dump(s, f, ensure_ascii=False)
            f.close()
            f = open("./data/perm/banned.json","w", encoding="utf-8")
            s = {"list":self.banned}
            json.dump(s, f, ensure_ascii=False)
            f.close()
    
    def __init__(self,configPath:str):
        self.__botmsg = []
    #读取配置文件并尝试连接api
        configs = toml.load(configPath)
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
        print("[INFO] Verify&Bind Succeed.")
    #读取权限文件
        self.perm = self.__Perm(configs)

    def __del__(self):
        message = {"sessionKey": self.__session,"qq": self.account}
        post = json.loads(requests.post(self.__api+"release",json.dumps(message,ensure_ascii=False)).text)
        if(post["code"]!=0):
            raise MiraiError(post)
        print("[INFO] SessionRelease Succeed.")
        self.perm.Save()
        
    def groupSend(self,messageChain:list,target:int=None): #群号可选
        message = {"sessionKey":self.__session,"target":self.target,"messageChain":messageChain}
        if(target!=None):
            message["target"]=target
        try:
            post = requests.post(self.__api+"sendGroupMessage",json.dumps(message,ensure_ascii=False).encode())
            if(json.loads(post.text)["code"]!=0):
                raise MiraiError(json.loads(post.text))
        except Exception as e:
            print(e)
            return False
        print("[INFO] SendAction Succeed.")
        return True
    def friendSend(self,messageChain:list,target:int):
        message = {"sessionKey":self.__session,"target":target,"messageChain":[]}
        message["messageChain"]=messageChain
        try:
            post = requests.post(self.__api+"sendFriendMessage",json.dumps(message,ensure_ascii=False).encode())
            if(json.loads(post.text)["code"]!=0):
                raise MiraiError(json.loads(post.text))
        except Exception as e:
            print(e)
            return False
        print("[INFO] SendAction Succeed.")
        return True

#Future:临时会话发送 获取bot,群,用户信息 撤回 戳一戳 账号管理 群管理

    def __fetch(self):
        url = self.__api+"fetchMessage?sessionKey="+self.__session
        try:
            i = json.loads(requests.get(url).text)
            if(i["code"]!=0):
                raise MiraiError(i)
            if(len(i["data"])!=0):self.__botmsg=self.__botmsg+i["data"]
        except Exception as e:
            print(e)
    def fetchMessage(self):
        self.__fetch()
        msg = {}
        try:msg = self.__botmsg.pop()
        except IndexError:return None
        if("Event" in msg["type"]):
            ret = message.Event(msg)
            return ret
        elif("Message" in msg["type"] and "Sync" not in msg["type"]):
            if(self.perm.Check(msg["sender"]["id"])==3):return None
            ret = message.Chain(msg["type"],msg["sender"],msg["messageChain"])
            return ret
        return None
    def fetchByID(self,messageID:int,targetID:int):
        url = self.__api+"messageFromId?sessionKey="+self.__session+"&messageId="+str(messageID)+"&target="+str(targetID)
        msg = {}
        try:
            i = json.loads(requests.get(url).text)
            if(i["code"]!=0):
                raise MiraiError(i)
            if(len(i["data"])!=0):msg = i["data"]
        except Exception as e:
            print(e)
            return None
        if(self.perm.Check(msg["sender"]["id"])==3):return None
        ret = message.Chain(msg["type"],msg["sender"],msg["messageChain"])
        return ret