import re
import webbrowser
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

import sites.btbtdy as btbtdy
import sites.dytt8 as dytt8

HTML_PATH = 'D:/Project/others/python/movieCrawl/result.html'

def getHtmlTam(movieName):
    html = '''<!DOCTYPE html>
        <html lang="en"><head><meta charset="UTF-8"><title>Document</title></head>
        <body>
        <main><h1>''' + movieName + ' <small>搜索结果</small></h1></main></body></html>'
    return BeautifulSoup(html, "html5lib")

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

def dytt8Format(list):
    if (len(list) == 0):
        return BeautifulSoup('<h2>电影天堂（dytt8）</h2><h4> 找不到该电影</h4>', "html5lib")
    htmlStr = '<h2>电影天堂（dytt8）</h2><ol>'
    for movie in list:
        htmlStr = htmlStr + '<li><a href=' + movie['link'] + '>' + movie['title'] + '</a></li>'
    htmlStr = htmlStr + '</ol>'
    return BeautifulSoup(htmlStr, "html5lib")

# 存储最终搜索结果
allLink = []

movieName = input("输入电影名称:")
print('正在检索电影天堂...')
dytt8Dict = dytt8.getMovieLink(movieName)
print('正在检索BT电影天堂...')
btbtdyDict = btbtdy.getMovieLink(movieName)
# print(btbtdyDict)
# print(dytt8Dict)
print('正在写入文件...')
with open(HTML_PATH,'w',encoding='utf-8') as file:
    htmlSoup = getHtmlTam(movieName)
    htmlSoup.main.append(dytt8Format(dytt8Dict))
    htmlSoup.main.append(btbtdyFormat(btbtdyDict))
    file.write(htmlSoup.prettify())
    print('正在打开文件')
    webbrowser.open(HTML_PATH)