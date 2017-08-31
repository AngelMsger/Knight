#!/usr/bin/env python3
# - *- coding utf- 8 - *-
import os
import random

import itchat
from itchat.content import TEXT, MAP, CARD, NOTE, SHARING, PICTURE, \
    RECORDING, ATTACHMENT, VIDEO, FRIENDS
import time
import datetime

import settings
from models import session
from tasks import reply_wordcloud, reply_keywords, reply_revoke, reply_file, \
    reply_text, reply_github_repos, reply_sharing

__author__ = 'AngelMsger'

"""
    NAME: Hawkin Robot
    VERSION: 1.0.0
    LICENSE: BSD
    DESCRIPTION: 这是一个简单的微信个人帐号机器人
"""


# 如果段时间内回复过消息，则随机退避一段时间后重试，直到成功
# TODO：这不是一个很好的处理方式，有可能造成饥饿，待改进
def retreat():
    while settings.LAST_REPLY > datetime.datetime.now() - datetime.timedelta(seconds=settings.RETREAT_CYCLE):
        time.sleep(random.randint(0, settings.RETREAT_CYCLE))
    settings.LAST_REPLY = datetime.datetime.now()


# 注册文本，地图位置，名片，特殊提示及分享的回复函数
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # 如果消息来自自己，则忽略，避免Bug
    if msg.fromUserName == itchat.originInstance.loginInfo['User']['UserName']:
        return
    retreat()
    # 如果为文本类型的消息
    if msg.type == TEXT:
        # 如果唤醒关键词
        if msg.text.lower() in settings.KEYWORDS_WAKEUP:
            reply_keywords(msg)
        # 如果唤醒词云
        elif msg.text.lower() in settings.WORDCLOUD_WAKEUP:
            reply_wordcloud(msg)
        # 如果唤醒GitHub仓库列表
        elif msg.text.lower() in settings.GITHUBREPOS_WAKEUP:
            reply_github_repos(msg)
        # 其他类型返回图灵机器人API调用结果
        else:
            reply_text(msg)
    # 如果为地理位置分享，随机返回一个预配置列表中的结果
    elif msg.type == MAP:
        msg.user.send(random.choice(settings.MSG_MAP))
    # 如果是联系人名片分享，则添加为好友
    elif msg.type == CARD:
        itchat.add_friend(msg.text['UserName'], verifyContent=settings.VERIFYCONTENT)
    # 如果是特殊提示，根据提示内容分类处理
    elif msg.type == NOTE:
        # 如果是红包，返回预配置结果
        if msg.msgType == settings.ITCHAT_MSGTYPE_CODE['common'] and msg.text == '收到红包，请在手机上查看':
            msg.user.send(settings.MSG_RED_PACKETS)
        # 如果是消息撤回，尝试发送，如图片不存在，则发送默认内容
        elif msg.msgType == settings.ITCHAT_MSGTYPE_CODE['revoke'] and msg.text.endswith('撤回了一条消息'):
            reply_msg = '@img@%s' % random.choice(settings.RESOURCES['revoke']) \
                if len(settings.RESOURCES.get('revoke', [])) > 0 else settings.MSG_REVOKE
            msg.user.send(reply_msg)
            # 调用函数返回撤回消息的内容
            reply_revoke(msg)
        elif msg.msgType == settings.ITCHAT_MSGTYPE_CODE['common'] and msg.text.startswith('你已添加了'):
            # 添加好友成功，发送打招呼内容
            msg.user.send(settings.MSG_GREET)
    # 是应用分享内容，调用函数任务分类处理
    else:
        reply_sharing(msg)


# 注册图音，附件，小视频的回复函数
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    # 调用函数任务分类处理
    reply_file(msg)


# 好友申请
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    # 接受好友申请并发送打招呼内容
    msg.user.verify()
    msg.user.send(settings.MSG_GREET)


# 群聊部分
@itchat.msg_register([TEXT, NOTE, SHARING], isGroupChat=True)
def text_reply(msg):
    # 如果为文本消息并@自己
    if msg.type == TEXT and msg.isAt:
        # 如果唤醒GitHub仓库列表
        msg.text = msg.text.replace('@%s\u2005' % itchat.originInstance.loginInfo['User']['NickName'], '')
        if msg.text.lower() in settings.GITHUBREPOS_WAKEUP:
            reply_github_repos(msg)
        # 如果是普通消息，则返回图灵机器人API调用结果并@发送人
        else:
            reply_text(msg, '@%s\u2005' % msg.actualNickName)
    # 如果是系统提示消息，则分类处理
    elif msg.type == NOTE:
        if msg.msgType == settings.ITCHAT_MSGTYPE_CODE['common'] and msg.text == '收到红包，请在手机上查看':
            msg.user.send(random.choice(settings.MSG_RED_PACKETS_GROUP))
        elif msg.msgType == settings.ITCHAT_MSGTYPE_CODE['revoke'] and msg.text.endswith('撤回了一条消息'):
            reply_msg = '@img@%s' % random.choice(settings.RESOURCES['revoke']) \
                if len(settings.RESOURCES.get('revoke', [])) > 0 else settings.MSG_REVOKE
            msg.user.send(reply_msg)
            # 由于并不记录群聊聊天内容，因此无法回复真实的聊天消息，同时也考虑到在群内撤回的消息不适合再发出来，此处随机回复恶搞内容
            msg.user.send('@%s\u2005说%s' % (msg.actualNickName, random.choice(settings.RANDOM_REVOKE_LIST)))
    # 是应用分享内容，调用函数分别处理
    elif msg.type == SHARING:
        reply_sharing(msg)
    else:
        # 群聊的普通消息有十六分之一的概率回复，回复内容在预配置列表中随机选择
        if random.randint(1, 16) == 1:
            msg.user.send(random.choice(settings.RANDOM_REPLY_LIST))


# 登录并运行
itchat.auto_login(True, enableCmdQR=settings.CONSOLE_QR, picDir=os.path.join(settings.CACHE_DIR, 'login_qr.jpg'),
                  statusStorageDir=os.path.join(settings.CACHE_DIR, 'login.status'))
itchat.run(True)

# 关闭数据库会话
session.close()
