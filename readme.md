# RSSGen

## 说明
RSSGen 是一个使用 Python 语言编写并运行于 Leancloud 平台的简单应用。该应用允许用户通过编写规则来抓取网站的内容并生成一个 RSS ，推荐与 [KindleEar](https://github.com/cdhigh/KindleEar) 共同使用。

包含功能：

* 抓取网页生成 RSS
* 新建和删除一个书签列表，用于将 Kindle 中的 RSS 文章在电脑中打开

## 部署

[搭配 coding 平台进行部署的说明](./guide/deploy/readme.md)

## 功能

_假设主机域名为 rssgen.leanapp.cn_

### 设置 RSS 抓取规则

recipe 目录下的每个 py 文件对应一个 rss 的生成规则，文件名以 base 结尾的类和文件名以 hide 结尾文件会自动被忽略，生成规则的编写可以参考该目录下 readme 文件中的说明

### 查看正在抓取的 RSS

打开网址 rssgen.leanapp.cn/rss 即可查看所有规则成功导入并开始自动抓取的 RSS

### 保存网址到书签

访问网页 rssgen.leanapp.cn/list/save?url=12345&title=54321 可以将网址 12345 以标题 54231 保存

_一般来说，该网址是由 KindleEar 或其他第三方程序自动生成的，网址仅使用 urllib.quote 进行一层包装_

### 查看保存到书签的网址

访问网页 rssgen.leanapp.cn/list 可以查看或删除保存的网址

## 鸣谢

RSSGen 使用了以下库

+   Leancloud
+   Bottle
+   PyRSS2Gen
+   feedparser
+   BeautifulSoup
+   jQuery
+   requests
