import os
import re

# 机器人名称，建议与图灵机器人API设置保持一致
_ROBOT_NAME = os.environ.get('ROBOT_NAME', '蠢愚的骑士')

# 资源目录
ASSETS_DIR = 'assets'
# 缓存目录
CACHE_DIR = 'cache'
# 字体文件名
FONT_PATH = os.path.join(ASSETS_DIR, 'wqy-microhei.ttc')

# 聊天记录图片缓存目录
LOGS_DIR = os.path.join(CACHE_DIR, 'logs')
# 词云图片混存目录
WORDCLOUD_DIR = os.path.join(CACHE_DIR, 'wordcloud')
# 如果指定目录不存在则创建
if not os.path.isdir(CACHE_DIR):
    os.mkdir(CACHE_DIR)
if not os.path.isdir(LOGS_DIR):
    os.mkdir(LOGS_DIR)
if not os.path.isdir(WORDCLOUD_DIR):
    os.mkdir(WORDCLOUD_DIR)

# 数据库URI
DB_URI = os.environ.get('DB_URI', 'sqlite:///cache/robot.db')

# 图灵机器人API配置
# TODO：你需要更新此处的 TULING123_API_KEY 为你的 API KEY。
TULING123_API_KEY = os.environ.get('TULING123_API_KEY', '你的API Key')

# 群聊普通消息随机返回内容
RANDOM_REPLY_LIST = ['😳', '😄', '😂', '😝',
                     '[微笑]', '[机智]', '[嘿哈]', '[捂脸]', '[皱眉]', '[耶]', '[奸笑]']
# 群聊撤回随机返回内容
RANDOM_REVOKE_LIST = ['今晚穿女装给大家看！', '明天请大家吃饭[鸡]！',
                      '钱多到只想发红包[红包][红包][红包]！']

# 关键词唤醒词
KEYWORDS_WAKEUP = ['关键字', '关键词']
# 词云唤醒词
WORDCLOUD_WAKEUP = ['生成词云', '词云']
# GitHub仓库列表唤醒词
GITHUBREPOS_WAKEUP = ['github项目', 'github仓库']

# 添加好友备注信息
VERIFYCONTENT = '你好啊，我叫%s，是一个机器人。你的好友向我推荐了你哦！' % _ROBOT_NAME

# 好友请求接受后的打招呼信息
MSG_GREET = '你好呀，我叫%s，一个机器人！[奸笑]' % _ROBOT_NAME
# 红包回复消息
MSG_RED_PACKETS = '我不花钱的，明天退给你~[机智]'
# 群聊红包随机回复列表
MSG_RED_PACKETS_GROUP = ['那我就不客气了哈！', '手快有，手慢无！[奸笑]', '谢谢老板！']
# 地理位置分享随机回复列表
MSG_MAP = ['正在呼叫空中支援！[机智]', '我记得我宝藏就埋在那！😳']
# 撤回默认回复内容
MSG_REVOKE = '撤回也没用，我看到了！'

# 自定义分享类型1关键词列表
CATEGORY_1 = {'猫', '猫咪', '咪', '喵', '铲屎', '可爱'}
# 自定义分享类型1随机回复列表
CATEGORY_1_REPLY = ['哇，好萌！', '暗中观察...', '有人组织一波偷猫吗？[皱眉]']

# 自定义分享类型2关键词列表
CATEGORY_2 = {'c++', 'python', 'java', 'android', 'linux', '编程', '代码', '文档'
              '前端', '爬虫', '机器学习', '深度学习', '程序员', '机器人', '论文'}
# 自定义分享类型2随机回复列表
CATEGORY_2_REPLY = ['生命不息，加班不止！', '程序员没有女朋友！', '优秀的同学，绝对是优秀的同学！[奸笑]',
                    '为什么你们会如此优秀啊！[捂脸][捂脸][捂脸]']

# 自定义分享类型3关键词列表
CATEGORY_3 = {'妹子', '小姐姐', '女神', '种子', '宅男', '魔法', '番剧'}
# 自定义分享类型3随机回复列表
CATEGORY_3_REPLY = ['四宅蒸鹅心！[机智][机智][机智]', '老哥，稳！[机智]', '发车了发车了！[奸笑]']

# 资源文件名词典
RESOURCES = {}
# 资源匹配正则表达式
_RESOURCES_PATTERN = re.compile(r'^([0-9a-zA-Z]+)_\d+\.jpg$')

# 根据资源匹配正则表达式加载合法资源
for resource in (_RESOURCES_PATTERN.match(img) for img in os.listdir(ASSETS_DIR)):
    if resource:
        resource_path = os.path.join(ASSETS_DIR, resource.group(0))
        RESOURCES.setdefault(resource.group(1), []).append(resource_path)

print(RESOURCES)

# 根据需要开启命令行二维码
try:
    CONSOLE_QR = int(os.environ.get('CONSOLE_QR', None))
except TypeError:
    CONSOLE_QR = False

# GitHub 帐号名
GITHUB_ACCOUNT = os.environ.get('GITHUB_ACCOUNT', 'AngelMsger')
GITHUB_DEFAULT_DESC = 'Another awesome %s project.'

# 图灵机器人API返回码
TUlING123_RESPONSE_CODE = {
    'text': 100000,
    'link': 200000,
    'news': 302000,
    'menu': 308000
}

# itchat库微信消息返回码
ITCHAT_MSGTYPE_CODE = {
    'common': 10000,
    'revoke': 10002
}
