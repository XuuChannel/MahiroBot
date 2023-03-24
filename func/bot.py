import toml
import requests
import json
import sys
from func import message

class Bot:
    api = ""
    account = 0
    target = 0
    session  = ""
    normalmsg = []
    targetmsg = []
    syncmsg = []
    botevent = []
    undevent = []
    def __init__(self) -> None:
    #读取配置文件并尝试连接api
        configs = toml.load("./config.toml")
        self.api = configs["api_url"]+":"+str(configs["api_port"])+"/"
        self.account = configs["bot_account"]
        self.target = configs["target_group"]
        try:
            verifyMessage = {"verifyKey": configs["api_key"]}
            verifyPost = requests.post(self.api+"verify",json.dumps(verifyMessage,ensure_ascii=False))
            sessionMessage = json.loads(verifyPost.text)
            if(sessionMessage["code"]!=0):
                raise Exception("SessionVerify_Error")
            bindMessage = {"sessionKey": sessionMessage["session"],"qq": self.account}
            bindPost = requests.post(self.api+"bind",json.dumps(bindMessage,ensure_ascii=False))
            bindResult = json.loads(bindPost.text)
            if(bindResult["code"]!=0):
                raise Exception("SessionBind_Error")
            self.session = sessionMessage["session"]
            self.success = True
            print("[INFO] BotConnection: Verify & Bind success.")
        except Exception as e:
            print(e)
            sys.exit()
    def __del__(self):
        try:
            releaseMessage = {"sessionKey": self.session,"qq": self.account}
            releasePost = json.loads(requests.post(self.api+"release",json.dumps(releaseMessage,ensure_ascii=False)).text)
            if(releasePost["code"]!=0):
                raise Exception("SessionRelease_Error")
            print("[INFO] BotRelease success.")
        except Exception as e:
            print(e)
    def GroupSend(self,messageChain,target:int=None): #群号可选
        smessage = {"sessionKey":self.session,"target":self.target,"messageChain":[]}
        smessage["messageChain"]=messageChain
        if(target!=None):
            smessage["target"]=target
        try:
            posts = requests.post(self.api+"sendGroupMessage",json.dumps(smessage,ensure_ascii=False).encode())
            if(json.loads(posts.text)["code"]!=0):
                self.errors = json.loads(posts.text)
                raise Exception(posts.text)
        except Exception as e:
            print(e)
            return False
        return True
    def FriendSend(self,messageChain,target:int):
        smessage = {"sessionKey":self.session,"target":target,"messageChain":[]}
        smessage["messageChain"]=messageChain
        try:
            posts = requests.post(self.api+"sendFriendMessage",json.dumps(smessage,ensure_ascii=False).encode())
            if(json.loads(posts.text)["code"]!=0):
                self.errors = json.loads(posts.text)
                raise Exception(posts.text)
        except Exception as e:
            print(e)
            return False
        return True
    #Future:临时会话发送 获取bot,群,用户信息 撤回 戳一戳 账号管理 群管理
    def _fetch(self):
        url = self.api+"fetchMessage?sessionKey="+self.session
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
        temp = {}
        if(istarget==True):
            if(len(self.targetmsg)!=0):temp = self.targetmsg.pop()
        else:
            if(len(self.normalmsg)!=0):temp = self.normalmsg.pop()
        if(temp!={}):
            if(temp["type"]=="GroupMessage"):
                r = message.Chain(True,temp["sender"]["id"],temp["sender"]["group"]["id"])
                #UNFINISHED:权限判定 权限添加
                chain = self._filter(temp["messageChain"])
                if(len(chain)!=0):r.chain = chain
                else:r.chain = [{"type":"Plain","text":"###不支持的消息###"}]
                return r
#↓未完成功能 不要用↓
    def fetchSync(self):
        self._fetch()
        if(len(self.syncmsg)!=0):return self.syncmsg.pop()
        return {}
    def fetchUndefined(self):
        self._fetch()
        if(len(self.undevent)!=0):return self.undevent.pop()
        return {}
    def fetchEvent(self):
        self._fetch()
        if(len(self.botevent)!=0):return self.botevent.pop()
        return {}
#↑Future:Sync和Event输出改为新的Chain/Event类↑
    def fetchByID(self,messageid:int,targetid:int):
        
        #UNFINISHED
        pass


#UNFINISHED:权限类