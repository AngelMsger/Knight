import datetime
import json
import os
import random
import re

import jieba.analyse
import numpy as np
import requests
from PIL import Image
from itchat.content import PICTURE, VIDEO
from sqlalchemy.orm.exc import NoResultFound
from wordcloud import WordCloud

import settings
from models import session, ChatLog, KeyWordsCache


# 返回文本信息
def reply_text(msg, prefix=''):
    # 将log存入数据库
    log = ChatLog(MsgId=msg.msgId, FromUserName=msg.fromUserName,
                  Content=msg.content, CreateTime=datetime.datetime.now())
    session.add(log)
    session.commit()

    # 向图灵机器人API请求返回内容
    request_json = json.dumps({'key': settings.TULING123_API_KEY,
                               'info': msg.text,
                               'userid': msg.fromUserName})
    response_json = requests.post('http://www.tuling123.com/openapi/api', data=request_json)
    response = json.loads(response_json.text)

    # 如果是普通文本回复
    if response.get('code', None) == settings.TUlING123_RESPONSE_CODE['text']:
        msg.user.send('%s%s' % (prefix, response['text']))

    # 如果是带有URL的回复
    elif response.get('code', None) == settings.TUlING123_RESPONSE_CODE['link']:
        msg.user.send('%s%s' % (prefix, response['text']))
        msg.user.send(response['url'])

    # 如果是类新闻类回复
    elif response.get('code', None) == settings.TUlING123_RESPONSE_CODE['news']:
        msg.user.send('%s%s' % (prefix, response['text']))
        for item in msg['list']:
            msg.user.send('%s：%s，报道来自%s'
                          % (item['article'], item['detailurl'], item['source']))
    # 如果是类菜谱类回复
    elif response.get('code', None) == settings.TUlING123_RESPONSE_CODE['menu']:
        msg.user.send('%s%s' % (prefix, response['text']))
        for item in msg['list']:
            msg.user.send('%s：%s，更多详情请查看：%s'
                          % (item['name'], item['info'], item['detailurl']))


# 返回分享内容
def reply_sharing(msg):
    # 运行基于jieba分词的TF / IDF算法获取分词与权重结果
    seg_list = set(jieba.analyse.extract_tags(msg.text.lower(), topK=3))
    # 如果与定制问题列表存在匹配项，则随机返回配置的回答
    if len(seg_list & settings.CATEGORY_1) > 0:
        msg.user.send(random.choice(settings.CATEGORY_1_REPLY))
    elif len(seg_list & settings.CATEGORY_2) > 0:
        msg.user.send(random.choice(settings.CATEGORY_2_REPLY))
    elif len(seg_list & settings.CATEGORY_3) > 0:
        msg.user.send(random.choice(settings.CATEGORY_3_REPLY))
    # 否则有四分之一的概率返回图灵API的结果
    else:
        if random.randint(1, 4) == 1:
            request_json = json.dumps({'key': settings.TULING123_API_KEY,
                                       'info': msg.text,
                                       'userid': 'SHARING'})
            response_json = requests.post('http://www.tuling123.com/openapi/api', data=request_json)
            response = json.loads(response_json.text)
            msg.user.send(response['text'])


# 返回关键字或关键词
def reply_keywords(msg):
    # 缓存规则为24小时，此处优先读取缓存
    try:
        # 尝试读取缓存，无论过期与否，只要存在都可读入
        cache = session.query(KeyWordsCache).filter_by(FromUserName=msg.fromUserName).one()
    except NoResultFound:
        # 缓存读取失败，说明从未建立过缓存记录，新建缓存记录
        cache = KeyWordsCache(FromUserName=msg.fromUserName,
                              CreateTime=datetime.datetime.fromtimestamp(0))
        session.add(cache)
        session.commit()

    # 缓存命中，即缓存时间在24小时之内
    if cache.CreateTime >= datetime.datetime.now() - datetime.timedelta(days=1):
        seg_list = json.loads(cache.Content)
    # 缓存未命中，即缓存时间在24小时以上
    else:
        # 读取聊天记录，并合并为长文本
        logs = session.query(ChatLog).filter_by(FromUserName=msg.fromUserName).all()
        content = ' '.join((log.Content for log in logs))
        # 重新运行基于jieba分词的TF / IDF算法获取分词与权重结果
        seg_list = jieba.analyse.extract_tags(content, topK=32, withWeight=True)
        # 如果列表长度大于或等于8，则视为得到了合理的结果，向用户发送并刷新缓存记录
        if len(seg_list) >= 8:
            cache.Content = json.dumps(seg_list)
            cache.CreateTime = datetime.datetime.now()
            session.merge(cache)
            session.commit()
        # 如果列表长度小于8，说明用户聊天记录内容过少，得到的结果不是很有意义，置为None
        else:
            seg_list = None

    if seg_list:
        msg.user.send('\n'.join(("关键词：%s，权重：%s" % seg for seg in seg_list)))
    else:
        msg.user.send('还无法为你提取关键词哦，多说两句再试试看吧！')


# 返回词云
def reply_wordcloud(msg):
    # 缓存规则为24小时，此处优先读取缓存。根据用户名设置缓存路径
    cache_path = os.path.join(settings.WORDCLOUD_DIR, msg.fromUserName[1:]) + '.jpg'

    try:
        # 如果缓存文件不存在或修改时间在大于24小时，则视为缓存已失效
        if not os.path.isfile(cache_path) or datetime.datetime. \
                fromtimestamp(os.path.getmtime(cache_path)) < datetime.datetime.now() \
                - datetime.timedelta(days=1):
            # 读取聊天记录，拼接为长文本
            logs = session.query(ChatLog).filter_by(FromUserName=msg.fromUserName).all()
            content = ' '.join((log.Content for log in logs))
            # 对长文本调用jieba分词进行分词
            seg_list = [seg for seg in jieba.cut(content)]
            # 生成词云需要较多词汇，此处判断分词结果列表长度
            if len(seg_list) > 32:
                # 尝试获取背景图资源
                mask_bgs = settings.RESOURCES.get('wordcloud', [])
                # 若背景图存在，则随机选取一张作为背景图
                if len(mask_bgs) > 0:
                    wordcloud = WordCloud(font_path=settings.FONT_PATH,
                                          mask=np.array(Image.open(random.choice(mask_bgs))))
                # 若背景图不存在，则设置默认白色背景
                else:
                    wordcloud = WordCloud(font_path=settings.FONT_PATH, background_color="white",
                                          width=768, height=768, margin=4)
                # 根据长文本生成词云
                wordcloud.generate(' '.join(seg_list))
                # 将词云存储进缓存目录
                wordcloud.to_file(cache_path)
            # 如果词汇量较少，则不适合生成词云，向用户发送错误信息
            else:
                raise RuntimeError('还无法为你提取关键词哦，多说两句再试试看吧')

        msg.user.send('@img@%s' % cache_path)
    except RuntimeError as e:
        msg.user.send(str(e))


# GitHub仓库信息缓存于内存中，期限为2分钟
repos_cache = {}


# 返回GitHub仓库信息
def reply_github_repos(msg):
    global repos_cache
    # 若缓存不存在或已过期，则刷新缓存
    if not repos_cache.get('time', None) or repos_cache['time'] \
            > datetime.datetime.now() - datetime.timedelta(minutes=2):
        repos_cache['cache'] = []
        repos = json.loads(requests.get('https://api.github.com/users/%s/repos' % settings.GITHUB_ACCOUNT).text)
        for repo in repos:
            repo_desc = repo.get('description', None) or settings.GITHUB_DEFAULT_DESC % repo.get('language', '')
            reply_msg = '%s：%s，详情点击%s' % (repo['name'], repo_desc, repo['clone_url'])
            repos_cache['cache'].append(reply_msg)
        repos_cache['time'] = datetime.datetime.now()
    for reply_msg in repos_cache['cache']:
        msg.user.send(reply_msg)


# 撤回消息匹配规则
revoke_msgid_pattern = re.compile(r'.+?<msgid>(\d+)</msgid>.+')


# 返回撤回消息
def reply_revoke(msg):
    # 查找撤回命令中的消息ID
    msgid = revoke_msgid_pattern.match(msg.content)
    if msgid:
        # 如果消息ID存在，则查找数据库找到这条消息并向用户发送消息内容
        try:
            log = session.query(ChatLog).filter_by(MsgId=msgid.group(1)).one()
            msg.user.send('你刚刚说%s[机智]' % log.Content)
        except NoResultFound:
            pass


# 返回文件
# TODO：此处逻辑比较简单，仍有发挥空间 ^_^
def reply_file(msg):
    # 根据用户名和时间设置缓存位置
    cache_path = os.path.join(settings.LOGS_DIR, '%s_%s.jpg' %
                              (msg.fromUserName[1:], str(datetime.datetime.now().timestamp())[1:11:2]))

    # 下载用户传输内容
    msg.download(cache_path)
    # 标识文件类型
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')

    # 回传用户传输的内容
    msg.user.send('@%s@%s' % (typeSymbol, cache_path))
