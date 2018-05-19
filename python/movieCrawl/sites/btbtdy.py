import requests
import re
import webbrowser

from urllib.parse import quote
from bs4 import BeautifulSoup

def _getHtmlSoup (url):
    r = requests.get(url)
    try:
        soup = BeautifulSoup(r.text, "html5lib")
    except:
        raise Exception("解析html出错")
    return soup

# 获取一部电影的所有下载链接
def _getMagnet (url, title):
    moviePage = _getHtmlSoup(url)
    movieLink = []
    for ul in moviePage.select('.p_list_02'):
        movieLink.append({
            'title': ul.select('.ico_1')[0].get_text(),
            'link': ul.find_all("a")[1]['href']
        })
    return movieLink

def getMovieLink (movieName):
    # 存储最终搜索结果
    allLink = []
    searchSoup = _getHtmlSoup('http://www.btbtdy.com/search/' + quote(movieName) + '.html')
    dlEle = searchSoup.find_all("dl")
    if (len(dlEle) > 0):
        for dl in dlEle:
            mTitle = (dl.find('a')['title'])
            movieId = re.findall(r'\d+', dl.find('a')['href'])[0]
            downloadPagePath = 'http://www.btbtdy.com/vidlist/' + movieId + '.html'
            allLink.append({
                'title': mTitle,
                'content' : _getMagnet(downloadPagePath, dl.find('a')['title'])
            })
        return allLink
    else:
        print('找不到该电影!!!')
        return []

if __name__=='__main__':
    getMovieLink(input("输入电影名称:"))