from core import message
from core import bot
import _thread,logging
import urllib,os,base64
from io import BytesIO
from PIL import Image as IMG
from PIL import ImageOps
from moviepy.editor import ImageSequenceClip as imageclip
import numpy

mahiroModuleInfo = {
    "name":"PetPet",
    "version":1.0,
    "type":"trigger",
    "condition":"Command",
    "command":["摸"],
    "permission":False,
    "target":"target"
}

if(os.path.exists("./data/PetPet")==False):
    os.makedirs("./data/PetPet")
    os.makedirs("./data/PetPet/temp")
    os.makedirs("./data/PetPet/PetPetFrames")
    for pnum in range(5):
        urllib.request.urlretrieve(f"https://raw.githubusercontent.com/SAGIRI-kawaii/saya_plugins_collection/master/modules/PetPet/PetPetFrames/frame{pnum}.png",f"./data/PetPet/PetPetFrames/frame{pnum}.png")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/SAGIRI-kawaii/saya_plugins_collection/master/modules/PetPet/PetPetFrames/template.gif","./data/PetPet/PetPetFrames/template.gif")
cLock = _thread.allocate_lock()
logging.info("Module "+mahiroModuleInfo["name"]+" INIT succeed.")

def mahiroModule(bot:bot.Bot,inbound:message.Chain=None,evinbound:message.Event=None)->None:
    global cLock
    if(cLock.locked()==False):
        cLock.acquire()
        try:
            targetuser = inbound.atRead()
            if(len(targetuser)!=1 or targetuser==None):raise Exception
            petpet(targetuser[0],fps=15)
            inbound.chainClear()
            inbound.add(message.Image(base64=base64.b64encode(open(f'./data/PetPet/temp/tempPetPet-{targetuser[0]}.gif','rb').read()).decode()))
            inbound.send(bot)
        except:
            inbound.chainClear()
            inbound.add(message.Plain("机盖宁温馨提示：参数错误喵 请参照以下格式喵\n'#摸 @你要at的人'"))
            inbound.send(bot)
        cLock.release()

#👇天下代码一大抄()

frame_spec = [
    (27, 31, 86, 90),
    (22, 36, 91, 90),
    (18, 41, 95, 90),
    (22, 41, 91, 91),
    (27, 28, 86, 91)
]

squish_factor = [
    (0, 0, 0, 0),
    (-7, 22, 8, 0),
    (-8, 30, 9, 6),
    (-3, 21, 5, 9),
    (0, 0, 0, 0)
]

squish_translation_factor = [0, 20, 34, 21, 0]

frames = tuple([f'./data/PetPet/PetPetFrames/frame{i}.png' for i in range(5)])


def save_gif(gif_frames, dest, fps=10):
    """生成 gif

    将输入的帧数据合并成视频并输出为 gif

    参数
    gif_frames: list<numpy.ndarray>
    为每一帧的数据
    dest: str
    为输出路径
    fps: int, float
    为输出 gif 每秒显示的帧数

    返回
    None
    但是会输出一个符合参数的 gif
    """
    clip = imageclip(gif_frames, fps=fps)
    clip.write_gif(dest)  # 使用 imageio
    clip.close()


# 生成函数（非数学意味）
def make_frame(avatar, i, squish=0, flip=False):
    """生成帧

    将输入的头像转变为参数指定的帧，以供 make_gif() 处理

    参数
    avatar: PIL.Image.Image
    为头像
    i: int
    为指定帧数
    squish: float
    为一个 [0, 1] 之间的数，为挤压量
    flip: bool
    为是否横向反转头像

    返回
    numpy.ndarray
    为处理完的帧的数据
    """
    # 读入位置
    spec = list(frame_spec[i])
    # 将位置添加偏移量
    for j, s in enumerate(spec):
        spec[j] = int(s + squish_factor[i][j] * squish)
    # 读取手
    hand = IMG.open(frames[i])
    # 反转
    if flip:
        avatar = ImageOps.mirror(avatar)
    # 将头像放缩成所需大小
    avatar = avatar.resize((int((spec[2] - spec[0]) * 1.2), int((spec[3] - spec[1]) * 1.2)), IMG.ANTIALIAS)
    # 并贴到空图像上
    gif_frame = IMG.new('RGB', (112, 112), (255, 255, 255))
    gif_frame.paste(avatar, (spec[0], spec[1]))
    # 将手覆盖（包括偏移量）
    gif_frame.paste(hand, (0, int(squish * squish_translation_factor[i])), hand)
    # 返回
    return numpy.array(gif_frame)


def petpet(member_id, flip=False, squish=0, fps=20) -> None:
    """生成PetPet

    将输入的头像生成为所需的 PetPet 并输出

    参数
    path: str
    为头像路径
    flip: bool
    为是否横向反转头像
    squish: float
    为一个 [0, 1] 之间的数，为挤压量
    fps: int
    为输出 gif 每秒显示的帧数

    返回
    bool
    但是会输出一个符合参数的 gif
    """

    url = f'http://q1.qlogo.cn/g?b=qq&nk={str(member_id)}&s=640'
    gif_frames = []
    # 打开头像
    # avatar = Image.open(path)
    img_content = urllib.request.urlopen(url)

    avatar = IMG.open(BytesIO(img_content.read()))

    # 生成每一帧
    for i in range(5):
        gif_frames.append(make_frame(avatar, i, squish=squish, flip=flip))
    # 输出
    save_gif(gif_frames, f'./data/PetPet/temp/tempPetPet-{member_id}.gif', fps=fps)

