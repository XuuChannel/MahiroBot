from core import bot
from core import message
import requests
import base64
import json

mahiroModuleInfo = {
    "name":"MahiroSetu",
    "version":1.0,
    "type":"trigger",
    "condition":"Command",
    "command":["涩图"],
    "permission":False,
    "target":"group"
}

def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    msg = message.Chain()
    msg.setTarget(Group=inbound.target["group"])
    try:
        picinfo = json.loads(requests.get("https://api.lolicon.app/setu/v2?size=regular").text)
        picinfo = picinfo["data"][0]
        msg.add(message.Plain(picinfo["title"]+" by "+picinfo["author"]+" (pid"+str(picinfo["pid"])+")\n"+picinfo["urls"]["regular"]))
        msg.send(bot)
        msg.chainClear()
        pic = base64.b64encode(requests.get(picinfo["urls"]["regular"]).content).decode()
        msg.add(message.Image(base64=pic))
        msg.send(bot)
    except Exception:
        msg.chainClear()
        msg.add(message.Plain("机盖宁温馨提示:涩图获取失败喵"))
        msg.send(bot)
