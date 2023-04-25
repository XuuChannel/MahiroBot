<div align="center">
<img src="https://i0.hdslb.com/bfs/article/90f468f90fd2715a42c0b017c53953c65fd4e8e4.png" width=200px>

# MahiroBot

**基于 [`Mirai-API-HTTP`](https://github.com/project-mirai/mirai-api-http)  的多功能 QQ 群聊机器人**

</div>

## 简介

`MahiroBot` 是一个使用 Python 编写的多功能 QQ 群聊机器人。

>### **ここに注意！**
>
>本项目可能与某些大佬的同类项目撞名 这绝对不是故意的喵
>
>投降喵！投降喵！

## 功能

`MahiroBot` 内置功能采用模块加载的形式，也可以接受第三方编写的模块以实现更多功能。

以下为项目默认模块目前可提供的功能，命令详情请参考bot内的帮助信息。

1. `MahiroBotManage`（内置）:
    - 其他模块的启用 禁用 管理 模块信息读取
    - 权限与黑名单系统
    - 关于与帮助信息
2. `MahiroTime`:
    - 报时
3. `MahiroNudge`:
    - 对戳一戳事件做出反应
4. `MahiroSetu`:
    - 基于 [`LoliconAPI`](https://api.lolicon.app/#/setu) 的随机涩图发送
5. `MahiroClassic`:
    - 记录群友逆天言论与弔图并随机/定向爆典
6. [开发中] `MahiroResponse`:
    - 读取消息链内容并触发特定回复
7. [计划中] `MahiroSocialCredit`:
    - 记录公民社会信用值。做的好！SC+10
8. [计划中] `MahiroMeme`:
    - 随机梗图
9. `MahiroGPT`:
    - 基于[`revChatGPT`](https://github.com/acheong08/ChatGPT)V1 的ai聊天模块（需要境外网络环境|模块安装说明详见代码文件注释）
10. `Performance`:
    - 输出性能信息（模块安装说明详见代码文件注释）

>### **ここに注意！**
>
>`MahiroBot` 不是(也不会是)完整的QQ机器人框架。_~~其实是因为作者太菜了 只管自己写的爽~~_
>
>如果您想为 `MahiroBot` 编写第三方模块 可以参考  [`MahiroBot`内部函数用法与插件规范](https://github.com/XuuChannel/MahiroBot) (施工中) 。

## Requirements

- Python 3.10+
- Mirai 2.14.0+
- Mirai-API-HTTP 2.7.0+

## 部署
### git pull

这部分不用多说了罢 不下载下来没法用喵

### 安装依赖

使用 PyPi 包管理器安装依赖。

```bash
pip install -r ./requirements.txt
```

### 配置文件

在根目录新建 `config.toml` , 按照 `config_sample.toml` 内提供的说明填写配置。

### 运行

```bash
python3 main.py
```

>### **ここに注意！**
>
>`Mirai-API-HTTP` 必须配置为 `http adapter` 开启 , `singleMode` 关闭。[详见此处](https://github.com/project-mirai/mirai-api-http#settingyml%E6%A8%A1%E6%9D%BF)
>
>部分模块会导入新的依赖库，建议检查模块文件的注释并提前安装新的依赖。
>
>`MahiroBot` 命令皆为#号开头。

## 开源许可

本项目依据 `Do What The F*ck You Want To Public License` 开源。

_~~拿去用的话 被人骂依托够使时不要说是我写的捏~~_

项目图片来源:《别当欧尼酱了》官方表情包  侵删