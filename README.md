# 插画采集爬虫

从互联网上的插画网站抓取元数据，包括作品信息、作者信息、作品图片URL等。

## PixivSpider

`PixivSpider`能抓取Pixiv中某个标签名下的数据。

```bash
scrapy crawl pixiv -a tag_str=<抓取的标签> -a phpsessid=<登陆Cookie中PHPSESSID值> -s JOBDIR=working/pixiv_spider
```

**tag_str**：抓取的标签名

**phpsessid**：登陆后的Cookie中PHPSESSID值

**JOBDIR（可选）**：状态保存路径，用于一次任务断点续爬

## 更多蜘蛛 & 管理界面

待开发...

## 使用代理启动蜘蛛

Linux环境下设置环境变量配置HTTP代理。

```bash
export HTTP_PROXY='http://localhost:10809'
export HTTPS_PROXY='http://localhost:10809'
```

Windows环境下使用PowerShell设置环境变量配置HTTP代理。

```powershell
$env:HTTP_PROXY = 'http://localhost:10809'
$env:HTTPS_PROXY = 'http://localhost:10809'
```

## 免责声明 ⚠️

本项目**仅限于学习和研究用途**，请勿用于任何商业或非法用途。使用时请遵守目标网站的相关规定和法律法规。
