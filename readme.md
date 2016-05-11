# RSSGen1.0

## 说明
RSSGen1.0 是一个使用 Python 语言编写并运行于 Leancloud 平台的简单应用。该应用允许用户通过编写规则来抓取网站的内容并生成一个 RSS 。该应用主要用于个人搭配 [KindleEar](https://github.com/cdhigh/KindleEar) 共同使用。

包含功能：

* 抓取网页生成 RSS
* 新建和删除一个书签列表，用于将 Kindle 中的 RSS 文章在电脑中打开（[与该 Fork 版 KindleEar 的分享文章功能可以简单的搭配使用](https://github.com/miaowm5/KindleEar/blob/master/books/m5_base.py)）

## 部署
+   注册 [Leancloud](https://leancloud.cn/) 账号，并创建一个应用
+   下载 RSSGen ，用记事本打开目录下的 auth.py ，填入刚刚创建的应用的 ID ，应用 ID 可以在 Leancloud 对应应用 后台 - 设置 中查看
+   将应用上传到 Leancloud ，具体的步骤可以参考 [Leancloud文档](https://leancloud.cn/docs/leanengine_guide-python.html#使用命令行工具部署) ，这里推荐使用 CSDN Code 部署应用

_实际上，如果不担心安全问题的话可以直接 Fork 本项目之后在 Github 上通过网页端修改 auth.py 的内容并直接部署_

+   在 Leancloud 应用 后台 - 存储 - 云引擎 - 定时任务 中，添加爬虫任务

| 函数名称           | Cron表达式       | 说明                |
| -------------- | ------------- | ----------------- |
| clear_old_feed | 0 0 0 * * ?   | 每天 0 点删除一天前的旧 RSS |
| spider_work    | 0 0 0/6 * * ? | 每隔六小时抓取一次网站的更新    |

+   在 Leancloud 应用 后台 - 存储 - 云引擎 - 设置 中，设置应用的域名


+   打开上一步设置的主机域名（假设为 rssgen.leanapp.cn），若显示 It works，则表示部署成功

## 功能

_假设主机域名为 rssgen.leanapp.cn_

### 设置 RSS 抓取规则

recipe 目录下的每个 py 文件对应一个 rss，该文件拥有一个全局变量 recipe ，要求设置为一个抓取 RSS 规则的类，该类需要实现以下接口：

| 名称         | 类型   | 说明                                  |
| ---------- | ---- | ----------------------------------- |
| url        | 类变量  | 该 RSS 的名称                           |
| get_item() | 实例方法 | yield 一个元祖 (文章标题, 文章时间, 文章网址, 文章内容) |

### 查看正在抓取的 RSS

打开网址 rssgen.leanapp.cn/rss 即可查看所有规则成功导入并开始自动抓取的 RSS

### 在 Kindle 上保存网页网址到电脑端

访问网页 rssgen.leanapp.cn/list/save?url=12345&title=54321 可以将网址 12345 以标题 54231 保存

_一般来说，该网址是由 KindleEar 或其他第三方程序自动生成的_

### 查看保存的网址

访问网页 rssgen.leanapp.cn/list 可以查看或删除保存的网址

## 鸣谢

RSSGen 使用了以下库

+   Leancloud
+   Bottle
+   PyRSS2Gen
+   feedparser
+   BeautifulSoup
+   jQuery
