# Scraping comments from Bilibili
# How to use:Change the share_info variable to the video sharing link you want to crawl, and run the program.
# P.S. The cookie in the headers variable needs to be updated regularly, otherwise the location cannot be crawled.

import requests  # 发送请求
import pandas as pd  # 保存csv文件
import os  # 判断文件是否存在
import time
from time import sleep  # 设置等待，防止反爬
import random  # 生成随机数
import re
import matplotlib.pyplot as plt
from snownlp import SnowNLP  # 中文情感分析库
from wordcloud import WordCloud  # 绘制词云图
import numpy as np
from PIL import Image  # 读取图片
import jieba.analyse  # jieba分词
import matplotlib.dates as mdates

# 请求头
headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 需定期更换cookie，否则location爬不到
    'cookie':"buvid3=DCA032FE-1058-4F35-B5F7-1FBAE08AED8908252infoc; b_nut=1709786308; i-wanna-go-back=-1; b_ut=7; _uuid=2F10F101B2-BFE2-10265-2DDD-6ABCD8FD7D5930249infoc; enable_web_push=DISABLE; FEED_LIVE_VERSION=V8; header_theme_version=undefined; browser_resolution=1100-0; home_feed_column=4; DedeUserID=12667712; DedeUserID__ckMd5=3ac2e58fee5dccb4; CURRENT_FNVAL=4048; rpdid=|(~k|)J|lJ|0J'u~|mm|YR|); buvid_fp_plain=undefined; buvid4=A6E27371-6AD7-3347-B265-17F84B0E4A9109160-024030704-5HSWhG7T%2FmEmAmagt9Fe0Q%3D%3D; fingerprint=b0d35f0b6d8853202042ec0546e57f61; hit-dyn-v2=1; CURRENT_QUALITY=80; buvid_fp=b0d35f0b6d8853202042ec0546e57f61; SESSDATA=dd299e51%2C1728187572%2Cf873d%2A41CjCwsU26ILSlvtUpTPM1Tem8Ps0yQdGCGiRQi9-rCYaqofz3t2h6YSRdFWAzbv_HhjcSVkhxaVNSelZuSTNMWlowd0xqRGhsUVhBZmxOdTZyR3JlSEZJQTVzS0E5RkE2cWZQMzl5NVJHek1abFhrSDVERHJ3TVlsdU9aS2kxclRmNHpUTHFDdHhBIIEC; bili_jct=36c347286836aae101d3fe05bd1790e7; sid=83it82ml; bp_video_offset_12667712=918314941909303302; LIVE_BUVID=AUTO7417126504324879; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTI5MDk2MzQsImlhdCI6MTcxMjY1MDM3NCwicGx0IjotMX0.hmjrhOfxAd7dwsbhG6oDKSxq8QuniqaHFTl6JAEhg74; bili_ticket_expires=1712909574; PVID=3; b_lsid=82DB1FC3_18EC3292719",
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/video/BV1FG4y1Z7po/?spm_id_from=333.337.search-card.all.click&vd_source=69a50ad969074af9e79ad13b34b1a548',
    'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
}


def trans_date(v_timestamp):
    """10位时间戳转换为时间字符串"""
    timeArray = time.localtime(v_timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def bv2av(bid):
    """把哔哩哔哩视频的bv号转成av号"""
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    r = 0
    for i in range(6):
        r += tr[bid[s[i]]] * 58 ** i
    aid = (r - 8728348608) ^ 177451812
    return aid


def get_comment(v_aid, v_bid):
    """
    爬取B站评论数据
    :param v_aid: B站视频的aid号
    :param v_bid: B站视频的bid号
    :return: None
    """
    # 循环页码爬取评论
    for i in range(max_page):
        try:
            sleep(random.uniform(0, 1))  # 随机等待，防止反爬
            url = "https://api.bilibili.com/x/v2/reply/main?csrf=bf9a78c05400af2f7bdac7947b836cc8&mode=3&next={}&oid={}&plat=1&type=1".format(
                i, v_aid)  # 请求地址
            response = requests.get(url, headers=headers, )  # 发送请求
            data_list = response.json()['data']['replies']  # 解析评论数据
            print('正在爬取B站评论[{}]: 第{}页,共{}条评论'.format(v_bid, i + 1, len(data_list)))
            if len(data_list) == 0:
                print('评论爬取完毕！')
                break
            comment_list = []  # 评论内容
            location_list = []  # IP属地
            time_list = []  # 评论时间
            user_list = []  # 评论作者
            like_list = []  # 点赞数
            # 循环爬取每一条评论数据
            for a in data_list:
                # 评论内容
                comment = a['content']['message']
                # XML 1.0 legal characters (https://www.w3.org/TR/xml/#charsets)
                re_xml_illegal = u'[\x00-\x08\x0b-\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]'
                if re.search(re_xml_illegal, comment):
                    comment = re.sub(re_xml_illegal, "", comment)
                comment_list.append(comment)
                # IP属地
                try:
                    location = a['reply_control']['location']
                except:
                    location = ""
                location_list.append(location.replace("IP属地：", ""))
                # 评论时间
                time = trans_date(a['ctime'])
                time_list.append(time)
                # 评论作者
                user = a['member']['uname']
                user_list.append(user)
                # 点赞数
                like = a['like']
                like_list.append(like)
            # 把列表拼装为DataFrame数据
            df = pd.DataFrame({
                '视频链接': 'https://www.bilibili.com/video/' + v_bid,
                '评论页码': (i + 1),
                '评论作者': user_list,
                '评论时间': time_list,
                'IP属地': location_list,
                '点赞数': like_list,
                '评论内容': comment_list,
            })
            if os.path.exists(outfile_path+outfile):
                header = False
            else:
                header = True
            # 把评论数据保存到csv文件
            df.to_csv(outfile_path+outfile, mode='a+', encoding='utf_8_sig', index=False, header=header)
        except Exception as e:
            print('爬评论发生异常: {}，继续..'.format(str(e)))


if __name__ == '__main__':

    # 输入需要爬取的视频分享链接（电脑端：分享->嵌入代码）
    #share_info = '<iframe src="//player.bilibili.com/player.html?aid=1101309534&bvid=BV11w4m1o7Qu&cid=1456802121&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>'
    share_info = '<iframe src="//player.bilibili.com/player.html?aid=1152252628&bvid=BV1pZ421t7zA&cid=1485024400&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>'
    # use re to extract aid and bvid from share_info
    aid = re.search('aid=(\d+)', share_info)
    bvid = re.search('bvid=(\w+)', share_info)

    if aid and bvid:
        aid = aid.group(1)
        bvid = bvid.group(1)
        print(f"aid: {aid}, bvid: {bvid}")
    else:
        print("aid or bvid not found in share_info")

    aid_list=[aid]
    aid_bvid_dict = {aid:bvid}

    scrolling = "no"
    border = "0"
    frameborder = "no"
    framespacing = "0"
    allowfullscreen = "true"
    #['BV1LT411D7NA', 'BV1Ev4y1r737', 'BV1dX4y1D7Tk']
    # 评论最大爬取页（每页20条评论）
    max_page = 500
    # 获取当前时间戳
    now = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # 循环爬取这几个视频的评论

    print('爬虫开始执行！')
    for aid in aid_list:
        # 输出文件名
        outfile = 'b站评论_{}.csv'.format(now)
        outfile_path = 'plot/'+aid_bvid_dict[aid] +'/'
        if not os.path.exists(outfile_path):
            os.mkdir(outfile_path)

        # 爬取评论
        get_comment(v_aid=aid, v_bid=aid_bvid_dict[aid])
    print('爬虫正常结束！')

###########################################################################################
# visualization part

