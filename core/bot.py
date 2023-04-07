import toml
import requests
import json
from core import message

class Bot:
    __api = ""
    account = 0
    target = 0
    __session  = ""
    __botmsg = []
    __perm = None#未定

    botevent = []#del?

    class __Perm:#未定
        t0 = []
        t1 = []
        banned = []
        target_admin_permission = False
        #权限判定 添加 删除 UNFINISHED
    
    def __init__(self,configPath:str):
    #读取配置文件并尝试连接api
        configs = toml.load(configPath)
        self.__api = configs["api_url"]+":"+str(configs["api_port"])+"/"
        self.account = configs["bot_account"]
        self.target = configs["target_group"]
        try:
            message = {"verifyKey": configs["api_key"]}
            post = requests.post(self.__api+"verify",json.dumps(message,ensure_ascii=False))
            result = json.loads(post.text)
            if(result["code"]!=0):
                raise Exception("[ERROR] MiraiAPI:SessionVerify Error.")
            message = {"sessionKey": result["session"],"qq": self.account}
            self.__session = result["session"]
            post = requests.post(self.__api+"bind",json.dumps(message,ensure_ascii=False))
            result = json.loads(post.text)
            if(result["code"]!=0):
                raise Exception("[ERROR] MiraiAPI:SessionBind Error.")
            print("[INFO] MiraiAPI:Verify&Bind Succeed.")
        except Exception as e:
            print(e)
            exit(1)
    #读取权限文件
        #未定
        self.__perm = self.__Perm()
        self.__perm.t0 = configs["t0_users"]
        self.__perm.target_admin_permission = configs["target_admin_permission"]
        '''↓重写
        try:
            f = open("./data/perm/t1.json","r", encoding="utf-8")
            self.perm_t1list = json.load(f)["list"]
            f.close()
        except FileNotFoundError:
            f = open("./data/perm/t1.json","w", encoding="utf-8")
            s = {"list":[]}
            json.dump(s, f, ensure_ascii=False)
            f.close()
        try:
            f = open("./data/perm/banlist.json","r", encoding="utf-8")
            self.perm_banlist = json.load(f)["list"]
            f.close()
        except FileNotFoundError:
            f = open("./data/perm/banlist.json","w", encoding="utf-8")
            s = {"list":[]}
            json.dump(s, f, ensure_ascii=False)
            f.close()
        '''

    def __del__(self):
        try:
            message = {"sessionKey": self.__session,"qq": self.account}
            post = json.loads(requests.post(self.__api+"release",json.dumps(message,ensure_ascii=False)).text)
            if(post["code"]!=0):
                raise Exception("[ERROR] MiraiAPI:SessionRelease Error.")
            print("[INFO] MiraiAPI:SessionRelease Succeed.")
        except Exception as e:
            print(e)
    def groupSend(self,messageChain:list,target:int=None): #群号可选
        message = {"sessionKey":self.__session,"target":self.target,"messageChain":messageChain}
        if(target!=None):
            message["target"]=target
        try:
            post = requests.post(self.__api+"sendGroupMessage",json.dumps(message,ensure_ascii=False).encode())
            if(json.loads(post.text)["code"]!=0):
                raise Exception("[ERROR] MiraiAPI:"+post.text)
        except Exception as e:
            print(e)
            return False
        print("[INFO] MiraiAPI:SendAction Succeed.")
        return True
    def friendSend(self,messageChain:list,target:int):
        message = {"sessionKey":self.__session,"target":target,"messageChain":[]}
        message["messageChain"]=messageChain
        try:
            post = requests.post(self.__api+"sendFriendMessage",json.dumps(message,ensure_ascii=False).encode())
            if(json.loads(post.text)["code"]!=0):
                raise Exception("[ERROR] MiraiAPI:"+post.text)
        except Exception as e:
            print(e)
            return False
        print("[INFO] MiraiAPI:SendAction Succeed.")
        return True
    #Future:临时会话发送 获取bot,群,用户信息 撤回 戳一戳 账号管理 群管理

#↓重写 删除/移动不必要的
    def _fetch(self):
        url = self.__api+"fetchMessage?sessionKey="+self.__session
        messagelist = []
        try:
            i = json.loads(requests.get(url).text)
            if(i["code"]!=0):
                raise Exception({"code":i["code"],"msg":i["msg"]})
            messagelist = i["data"]
        except Exception as e:
            print(e)
        if(len(messagelist)==0):
            return None
        for message in messagelist:
            match message["type"]:
                case "GroupMessage":
                    if(message["sender"]["group"]["id"] == self.target):self.targetmsg.append(message)
                    else:self.normalmsg.append(message)
                case "FriendRecallEvent":
                    self.normalmsg.append(message)
                case "NudgeEvent":
                    self.targetmsg.append(message)
                case "GroupRecallEvent":
                    if(message["group"]["id"] == self.target):self.targetmsg.append(message)
                    else:self.normalmsg.append(message)
                case "MemberJoinEvent":
                    if(message["member"]["group"]["id"] == self.target):self.targetmsg.append(message)
                    else:self.normalmsg.append(message)
                case "MemberLeaveEventKick":
                    if(message["member"]["group"]["id"] == self.target):self.targetmsg.append(message)
                    else:self.normalmsg.append(message)
                case "MemberLeaveEventQuit":
                    if(message["member"]["group"]["id"] == self.target):self.targetmsg.append(message)
                    else:self.normalmsg.append(message)
                case "MemberPermissionChangeEvent":
                    if(message["member"]["group"]["id"] == self.target):self.targetmsg.append(message)
                    else:self.normalmsg.append(message)
                case "MemberMuteEvent":
                    if(message["member"]["group"]["id"] == self.target):self.targetmsg.append(message)
                    else:self.normalmsg.append(message)
                case "FriendMessage":
                    self.normalmsg.append(message)
                case "TempMessage":
                    self.normalmsg.append(message)
                case "StrangerMessage":
                    self.normalmsg.append(message)
                case "OtherClientMessage":
                    self.normalmsg.append(message)
                case "FriendSyncMessage":
                    self.syncmsg.append(message)
                case "GroupSyncMessage":
                    self.syncmsg.append(message)
                case "TempSyncMessage":
                    self.syncmsg.append(message)
                case "StrangerSyncMessage":
                    self.syncmsg.append(message)
                case "BotOnlineEvent":
                    self.botevent.append(message)
                case "BotOfflineEventActive":
                    self.botevent.append(message)
                case "BotOfflineEventForce":
                    self.botevent.append(message)
                case "BotOfflineEventDropped":
                    self.botevent.append(message)
                case "BotReloginEvent":
                    self.botevent.append(message)
                case "BotGroupPermissionChangeEvent":
                    self.botevent.append(message)
                case "BotMuteEvent":
                    self.botevent.append(message)
                case "BotUnmuteEvent":
                    self.botevent.append(message)
                case "BotJoinGroupEvent":
                    self.botevent.append(message)
                case "BotLeaveEventActive":
                    self.botevent.append(message)
                case "BotLeaveEventKick":
                    self.botevent.append(message)
                case "BotLeaveEventDisband":
                    self.botevent.append(message)
                case "GroupMuteAllEvent":
                    self.botevent.append(message)
                case "NewFriendRequestEvent":
                    self.botevent.append(message)
                case "MemberJoinRequestEvent":
                    self.botevent.append(message)
                case "BotInvitedJoinGroupRequestEvent":
                    self.botevent.append(message)
                case "OtherClientOnlineEvent":
                    self.botevent.append(message)
                case "OtherClientOfflineEvent":
                    self.botevent.append(message)
                case _:
                    self.undevent.append(message)
    def _filter(self,mlist):
        out = []
        for i in mlist:
            if(i["type"]=="Plain" or i["type"]=="Image" or i["type"]=="Voice" or i["type"]=="At" or i["type"]=="AtAll" or i["type"]=="Quote"):
                out.append(i)
        return out
    def fetchMessage(self,istarget:bool=False):
        self._fetch()
        msg = {}
        if(istarget==True):
            if(len(self.targetmsg)!=0):msg = self.targetmsg.pop()
        else:
            if(len(self.normalmsg)!=0):msg = self.normalmsg.pop()
        if(msg!={}):
            if(msg["type"]=="GroupMessage" or msg["type"] == "TempMessage"):
                r = message.Chain(True,msg["sender"]["id"],msg["sender"]["group"]["id"])
                r.MessageType = msg["type"]
                for id in self.perm_t0list:
                    if(id==msg["sender"]["id"]):r.perminit(0)
                for id in self.perm_t1list:
                    if(id==msg["sender"]["id"]):r.perminit(1)
                if(istarget==True and self.target_admin_permission==True):
                    if(msg["sender"]["permission"]=="ADMINISTRATOR" or msg["sender"]["permission"]=="OWNER"):
                        r.perminit(0)
                for id in self.perm_banlist:
                    if(id==msg["sender"]["id"]):r.perminit(3)
                chain = self._filter(msg["messageChain"])
                if(len(chain)!=0):r.chain = chain
                else:r.chain = [{"type":"Other","text":"不支持的消息"}]
                if(r.sender["perm"]==3):r.chain = [{"type":"Other","text":"BANNED USER"}]
                return r
            elif(msg["type"]=="FriendMessage" or msg["type"] == "StrangerMessage" or msg["type"] == "OtherClientMessage"):
                r = message.Chain(True,msg["sender"]["id"])
                r.MessageType = msg["type"]
                for id in self.perm_banlist:
                    if(id==msg["sender"]["id"]):r.perminit(3)
                chain = self._filter(msg["messageChain"])
                if(len(chain)!=0):r.chain = chain
                else:r.chain = [{"type":"Other","text":"不支持的消息"}]
                if(r.sender["perm"]==3):r.chain = [{"type":"Other","text":"BANNED USER"}]
                return r
            else:
                #Future:补全Event类
                r = message.Event(msg)
                return r         
    def fetchByID(self,messageid:int,targetid:int):
        url = self.__api+"messageFromId?sessionKey="+self.__session+"&messageId="+str(messageid)+"&target="+str(targetid)
        msg = {}
        try:
            i = json.loads(requests.get(url).text)
            if(i["code"]!=0):
                raise Exception({"code":i["code"],"msg":i["msg"]})
            elif(i["code"]==5):
                return None
            msg = i["data"]
        except Exception as e:
            print(e)
        if(msg["type"]=="GroupMessage" or msg["type"] == "TempMessage"):
            r = message.Chain(True,msg["sender"]["id"],msg["sender"]["group"]["id"])
            r.MessageType = msg["type"]
            for id in self.perm_banlist:
                if(id==msg["sender"]["id"]):r.perminit(3)
            chain = self._filter(msg["messageChain"])
            if(len(chain)!=0):r.chain = chain
            else:r.chain = [{"type":"Other","text":"不支持的消息"}]
            if(r.sender["perm"]==3):r.chain = [{"type":"Other","text":"BANNED USER"}]
            return r
        elif(msg["type"]=="FriendMessage" or msg["type"] == "StrangerMessage" or msg["type"] == "OtherClientMessage"):
            r = message.Chain(True,msg["sender"]["id"])
            r.MessageType = msg["type"]
            for id in self.perm_banlist:
                if(id==msg["sender"]["id"]):r.perminit(3)
            chain = self._filter(msg["messageChain"])
            if(len(chain)!=0):r.chain = chain
            else:r.chain = [{"type":"Other","text":"不支持的消息"}]
            if(r.sender["perm"]==3):r.chain = [{"type":"Other","text":"BANNED USER"}]
            return r
        else:
            #Future:补全Event类
            r = message.Event(msg)
            return r  
    def permAdd(self,perm:int,id:int):
        if(perm==1):
            self.perm_t1list.append(id)
            f = open("./data/perm/t1.json","w", encoding="utf-8")
            s = {"list":self.perm_t1list}
            json.dump(s, f, ensure_ascii=False)
            f.close()
        elif(perm==3):
            self.perm_banlist.append(id)
            f = open("./data/perm/banlist.json","w", encoding="utf-8")
            s = {"list":self.perm_banlist}
            json.dump(s, f, ensure_ascii=False)
            f.close()
        else:
            return None
    #UNFINISHED:权限删除 权限去重


    