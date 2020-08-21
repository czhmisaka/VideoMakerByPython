# -*- coding: utf-8 -*-
# @Date  : 2020/08/01 16:32
# @Author: CK

import requests
import json
import re

#爬取歌名
def song_list():
    url='http://music.163.com/discover/toplist?id=3778678'
    r=requests.get(url)
    reg1 = r'<ul class="f-hide"><li><a href="/song\?id=\d*?">.*</a></li></ul>'
    result_contain_songs_ul = re.compile(reg1).findall(r.text)
    result_contain_songs_ul = result_contain_songs_ul[0]
    reg2 = r'<li><a href="/song\?id=\d*?">(.*?)</a></li>'
    reg3 = r'<li><a href="/song\?id=(\d*?)">.*?</a></li>'
    hot_songs_name = re.compile(reg2).findall(result_contain_songs_ul)
    hot_songs_id = re.compile(reg3).findall(result_contain_songs_ul)
    print(hot_songs_name, hot_songs_id)
    # 返回歌曲名 歌曲id
    return hot_songs_name, hot_songs_id

# 爬取热评
def song_id(id,name):
    # 字符串拼接
    url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + str(id) + '?sortType=%203'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    }
    hotcomments = json.loads(requests.get(url,headers=headers).text)['hotComments']
    num = 0
    with open('./网抑云热评.txt', 'a', encoding='utf-8') as f:
        f.write('《' + name + '》：' + '\n')
        for i in hotcomments:
            num += 1
            print(i['content']+'\n')
            f.write('\n')
        f.write('\n====================================================\n\n')


def main():
    # 调用方法 获得歌曲名 歌曲id
    hot_songs_name, hot_songs_id =  song_list()
    print(hot_songs_name)
    print(hot_songs_id)
    # 循环遍历抓取所有热搜热评
    num = 0
    while num < len(hot_songs_name):
        print('正在抓取网易云音乐热搜榜第%d首歌曲热评...' % (num + 1))
        song_id(hot_songs_id[num],hot_songs_name[num])
        print('第%d首歌曲热评抓取成功' % (num + 1))
        num += 1

if __name__ == '__main__':
    main()