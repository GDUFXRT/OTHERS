import re
import sys
import webbrowser
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

import sites.btbtdy as btbtdy
import sites.dytt8 as dytt8

HTML_PATH = sys.path[0] + '\\result.html'

# 获取展示html模板
def getHtmlTam(movieName):
    html = '''<!DOCTYPE html>
        <html lang="en"><head><meta charset="UTF-8"><title>Document</title></head>
        <body>
        <main><h1>''' + movieName + ' <small>搜索结果</small></h1></main></body></html>'
    return BeautifulSoup(html, "html5lib")

# 格式化btbtdy数据
def btbtdyFormat(list):
    if (len(list) == 0):
        return BeautifulSoup('<h2>BT电影天堂（www.btbtdy.com）</h2><h4> 找不到该电影</h4>', "html5lib")
    htmlStr = '<h2>BT电影天堂（www.btbtdy.com）</h2><ul>'
    for movie in list:
        htmlStr = htmlStr + '<li><h4>' + movie['title'] + '</h4><ol>'
        for movieLink in movie['content']:
            htmlStr = htmlStr + '<li><a href=\"' + movieLink['link'] + '\">' + movieLink['title'] + '</a></li>'
        htmlStr = htmlStr + '</ol></li>'
    htmlStr = htmlStr + '</ul>'
    return BeautifulSoup(htmlStr, "html5lib")

# 格式化dytt8数据
def dytt8Format(list):
    if (len(list) == 0):
        return BeautifulSoup('<h2>电影天堂（dytt8）</h2><h4> 找不到该电影</h4>', "html5lib")
    htmlStr = '<h2>电影天堂（dytt8）</h2><ol>'
    for movie in list:
        htmlStr = htmlStr + '<li><a href=' + movie['link'] + '>' + movie['title'] + '</a></li>'
    htmlStr = htmlStr + '</ol>'
    return BeautifulSoup(htmlStr, "html5lib")

if __name__=='__main__':
    # 存储最终搜索结果
    allLink = []
    movieName = input("输入电影名称:")
    print('正在检索电影天堂...')
    dytt8Dict = dytt8.getMovieLink(movieName)
    print('正在检索BT电影天堂...')
    btbtdyDict = btbtdy.getMovieLink(movieName)
    print('正在写入文件...')
    with open(HTML_PATH,'w',encoding='utf-8') as file:
        htmlSoup = getHtmlTam(movieName)
        htmlSoup.main.append(dytt8Format(dytt8Dict))
        htmlSoup.main.append(btbtdyFormat(btbtdyDict))
        file.write(htmlSoup.prettify())
        print('正在打开文件...')
        webbrowser.open(HTML_PATH)