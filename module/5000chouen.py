from core import message
from core import bot
import _thread,logging
import urllib,importlib,os,base64
from io import BytesIO
#代码文件名中带有字符"p"好像无法正常识别
mahiroModuleInfo = {
    "name":"5000兆円",
    "version":1.0,
    "type":"trigger",
    "condition":"Command",
    "command":["5000"],
    "permission":False,
    "target":"all"
}

if(os.path.exists("./data/5000choen")==False):
    os.makedirs("./data/5000choen")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/pcrbot/5000choyen/main/generator.py","./data/5000choen/generator.py")
    urllib.request.urlretrieve("https://github.com/pcrbot/5000choyen/raw/main/NotoSansCJKSC-Black.ttf","./data/5000choen/NotoSansCJKSC-Black.ttf")
    urllib.request.urlretrieve("https://github.com/pcrbot/5000choyen/raw/main/NotoSerifCJKSC-Black.ttf","./data/5000choen/NotoSerifCJKSC-Black.ttf")
generator = importlib.import_module("data.5000choen.generator")
cLock = _thread.allocate_lock()
logging.info("Module "+mahiroModuleInfo["name"]+" INIT succeed.")

def pic64process(upper:str,downer:str):
    pic=generator.genImage(word_a=upper, word_b=downer)
    output_buffer = BytesIO()
    pic.save(output_buffer,format="png")
    return base64.b64encode(output_buffer.getvalue()).decode('utf-8')

def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    global cLock
    if(cLock.locked()==False):
        cLock.acquire()
        try:
            text = inbound.commandCheck("5000",hasParam=True)
            text = text.lstrip()
            text = text.rstrip()
            text = text.split("|")
            inbound.chainClear()
            inbound.add(message.Image(base64=pic64process(text[0],text[1])))
            inbound.send(bot)
        except:
            inbound.chainClear()
            inbound.add(message.Plain("机盖宁温馨提示：输入格式错误喵 请参照以下格式\n'#5000 红字|白字'"))
            inbound.send(bot)
        cLock.release()