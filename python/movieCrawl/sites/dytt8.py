import requests
import base64
import re
from bs4 import BeautifulSoup

def ThunderEncode (url):
    targetStr = 'AA' + url + 'ZZ'
    return 'thunder://' + re.sub(r'^b|[\"\']', '', str(base64.b64encode(targetStr.encode('utf-8'))))

def _getHtmlSoup (url):
    r = requests.get(url)
    r.encoding = 'gb2312'
    try:
        soup = BeautifulSoup(r.text, "html5lib")
    except:
        raise Exception("解析html出错")
    return soup

# 获取一部电影的所有下载链接
def _getMagnet (url):
    moviePage = _getHtmlSoup(url)
    content = moviePage.select('.bd3r')[0].select('.co_area2')[0]
    return {
            'title': content.select('.title_all')[0].find('font').get_text(),
            'link': ThunderEncode(content.select('#Zoom')[0].find('a')['href'])
        }

def getMovieLink (movieName):
    # 存储最终搜索结果
    allLink = []
    mName = str(movieName.encode('gb2312'))[2:].replace('\\x', '%')
    searchSoup = _getHtmlSoup('http://s.ygdy8.com/plus/so.php?kwtype=0&searchtype=title&keyword=' + mName)
    tables = searchSoup.select(".co_content8 table")
    if (len(tables) == 0):
        return []
    for table in tables:
        allLink.append(_getMagnet('http://www.ygdy8.com' + table.find('a')['href']))
    return allLink

if __name__=='__main__':
    print('测试,搜索电影：黑豹')
    getMovieLink('黑豹')