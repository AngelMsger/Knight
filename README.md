# Knight
[![Build Status](https://travis-ci.org/AngelMsger/Knight.svg?branch=master)](https://travis-ci.org/AngelMsger/Knight)

## Overview
Knight is a Simple Wechat Bot Demo. I Code This **Just for Fun** :).

## Features
1. Support Most of Types of Wechat.
2. Sharing Content Analyze.
3. Random Retreat to Decrease the Risk of Being Banned.
4. Dockerized.
5. **Funny**

## Usage
**There is High Risks of Being Banned If You Change Login Location Frequently!**
1. `docker run -itd --name=knight --restart=always -v /tmp:/app/cache -e "TULING123_API_KEY=你的API KEY" [-e "ROBOT_NAME=机器人名字"] [-e "GITHUB_ACCOUNT=你的GITHUB用户名"] [-e "DB_URI='数据库连接URI'"] angelmsger/knight`
2. `docker logs knight`
3. Scan The QR Code And Start.

## Update
* 2018/2/27 Update Dependencies.

## Principle
1. [tuling123](http://www.tuling123.com/): NLP API
2. [jieba](https://github.com/fxsjy/jieba): Tokenizer
3. [itchat](https://github.com/littlecodersh/ItChat): Wechat Web API
4. [wordcloud](https://github.com/amueller/word_cloud): WordCloud Generator

