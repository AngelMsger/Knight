# Knight
***
## Overview
Knight is a Simple Wechat Bot Demo. I Code This **Just for Fun** :).

## Features
1. Support Most of Types of Wechat.
2. Sharing Content Analyze.
3. Random Retreat to Decrease the Risk of Being Banned.
4. Dockerized.
5. **Funny**

## Usage
1. `docker run -itd --name=knight --restart=always -v /tmp:/app/cache -e "TULING123_API_KEY=你的API KEY" [-e "ROBOT_NAME=机器人名字"] [-e "GITHUB_ACCOUNT=你的GITHUB用户名"] [-e "DB_URI='数据库连接URI'"] angelmsger/knight`

2. `docker logs knight`

3. Scan The QR Code And Start.

## Principle
1. [tuling123](http://www.tuling123.com/): NLP API
2. [jieba](https://github.com/fxsjy/jieba): Tokenizer
3. [itchat](https://github.com/littlecodersh/ItChat): Wechat Web API
4. [wordcloud](https://github.com/amueller/word_cloud): WordCloud Generator
***
**血泪教训：利用VPS频繁切换登录地点有封号风险，请创建小号玩耍...**
