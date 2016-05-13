# RSSGen

## 说明
RSSGen 是一个使用 Python 语言编写并运行于 Leancloud 平台的简单应用。该应用允许用户通过编写规则来抓取网站的内容并生成一个 RSS ，推荐与 [KindleEar](https://github.com/cdhigh/KindleEar) 共同使用。

包含功能：

* 抓取网页生成 RSS
* 新建和删除一个书签列表，用于将 Kindle 中的 RSS 文章在电脑中打开（[与该的 Fork 版 KindleEar 的分享文章功能搭配使用](https://github.com/miaowm5/KindleEar/blob/master/books/m5_base.py)）

## 部署

注册 [Leancloud](https://leancloud.cn/) 账号，并创建一个应用

下载 RSSGen ，用记事本打开目录下的 auth.py ，填入刚刚创建的应用的 ID ，应用 ID 可以在 Leancloud 对应应用 后台 - 设置 中查看

将应用上传到 Leancloud ，具体的步骤可以参考 [Leancloud文档](https://leancloud.cn/docs/leanengine_guide-python.html#使用命令行工具部署) ，这里推荐使用 CSDN Code 部署应用

_实际上，如果不担心安全问题的话可以直接 Fork 本项目之后在 Github 上通过网页端修改 auth.py 的内容并直接部署_

在 Leancloud 应用 后台 - 存储 - 云引擎 - 定时任务 中，添加爬虫任务

| 函数名称           | Cron表达式       | 说明                |
| -------------- | ------------- | ----------------- |
| clear_old_feed | 0 0 0 * * ?   | 每天 0 点删除一天前的旧 RSS |
| spider_work    | 0 0 0/6 * * ? | 每隔六小时抓取一次网站的更新    |

在 Leancloud 应用 后台 - 存储 - 云引擎 - 设置 中，设置应用的域名

打开上一步设置的主机域名（假设为 rssgen.leanapp.cn），若显示 It works，则表示部署成功

## 功能

_假设主机域名为 rssgen.leanapp.cn_

### 设置 RSS 抓取规则

recipe 目录下的每个 py 文件对应一个 rss，以 base 结尾的类为公共库会自动忽略，必要时可以在提供相同接口的前提下重写全部代码，以下是必须实现的接口：

| 名称       | 类型       | 说明                                       |
| -------- | -------- | ---------------------------------------- |
| recipe   | 全局变量     | 该变量需要赋值为一个抓取规则的类，爬虫工作时会传递一个 info 参数对该类进行实例化 |
| info     | 规则类的类变量  | 纪录了服务器端所保存的抓取信息的对象，防止重复抓取同一内容            |
| name     | 规则类的类变量  | 用于区分不同规则的标识符，服务器端也将以该名字保存数据              |
| oldest   | 规则类的类变量  | 要保留的时间最早的文章，用于服务端自动清理过旧内容                |
| get_item | 规则类的实例方法 | yield 元祖，每个元祖内容为 (标题,时间,网址,内容)           |

默认的 base.py 中定义了以下方法和接口可以直接继承使用。sample_recipe 目录中放着一些基于 base.py 的范例 recipe 可供参考。

类变量

| 名称                | 类型    | 说明                                   |
| ----------------- | ----- | ------------------------------------ |
| capture           | 字典    | 储存了执行 process_article 清理文章时所需的数据     |
| capture["catch"]  | 字符串数组 | 每个字符串作为 CSS 选择器，提取文章中满足该选择器的内容       |
| capture["remove"] | 字符串数组 | 每个字符串作为 CSS 选择器，删除上一步提取的文章中满足该选择器的内容 |
| capture["nav"]    | 字符串   | 文章页码的 CSS 选择器，用于尝试自动拼接分页文章           |

方法

| 名称                     | 参数                | 说明                                       |
| ---------------------- | ----------------- | ---------------------------------------- |
| featch_content         | 网址字符串             | 打开网址，返回内容，失败时返回 None                     |
| spider_main            | 探测网址字符串,抓取网址 set  | 依次抓取 set 中的网页内容，返回由元祖(抓取网址,抓取内容)组成的 list |
| spider_refresh_capture | 探测网址字符串,探测网址内容    | spider_main 每次抓取结束后调用，用来抓取分页文章等，返回值将作为下一轮 spider_main 的参数使用 |
| spider_generate_html   | spider_main 的抓取结果 | 用于将 spider_main 抓取结果拼接成一个单独的 html 页面     |
| convert_time           | datetime          | 将所有 datetime 统一转换为不带时区的 datetime，时间不会自动转换 |
| get_last_check         | 无                 | 获取服务端数据最后的抓取时间（UTC8）                     |
| refresh_last_check     | datetime          | 时间作为最后抓取时间保存到服务端                         |
| process_article        | 网页内容              | 根据类变量 capture 的设置自动清理文章内容                |

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
