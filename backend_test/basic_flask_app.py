# This is a basic Flask app that receives a string from the frontend, processes it(calls GPT API), and returns the response.
# It listens on port 5000 and receives requests from Analyze-page-II.
# How to use: run this file as the server, and send requests by clicking the "Analyze" button on Analyze-page-II.
from flask import Flask, request, jsonify
from flask_cors import CORS
from Bilibili_comments_scraping import get_comment
from visualization import visualization
from analyze_with_GPT_API import getAnalysis
import requests  # 发送请求
import pandas as pd  # 保存csv文件
import os  # 判断文件是否存在
import time
from time import sleep  # 设置等待，防止反爬
import random  # 生成随机数
import re

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/process-string', methods=['POST'])
def process_string():
    # Assuming the character string is sent in the body of the request
    data = request.json
    user_string = data['userString']

    def scraping():
        #= '<iframe src="//player.bilibili.com/player.html?aid=1101309534&bvid=BV11w4m1o7Qu&cid=1456802121&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>'
        share_info = user_string
        # use re to extract aid and bvid from share_info
        aid = re.search('aid=(\d+)', share_info)
        bvid = re.search('bvid=(\w+)', share_info)

        if aid and bvid:
            aid = aid.group(1)
            bvid = bvid.group(1)
            print(f"aid: {aid}, bvid: {bvid}")
        else:
            print("aid or bvid not found in share_info")

        scrolling = "no"
        border = "0"
        frameborder = "no"
        framespacing = "0"
        allowfullscreen = "true"
        max_page = 500
        # 获取当前时间戳
        now = time.strftime("%Y%m%d%H%M%S", time.localtime())
        # 循环爬取这几个视频的评论

        print('爬虫开始执行！')
        # 输出文件名
        outfile = 'b站评论_{}.csv'.format(now)
        outfile_path = 'plot/' + bvid + '/'
        if not os.path.exists(outfile_path):
            os.mkdir(outfile_path)

        # 爬取评论
        get_comment(aid, bvid)


    # and generate images and additional strings.
    #generated_image_urls = visualization(outfile_path,outfile)
    #generated_image_urls = ["C:/Code/GTSI Course/ECE6001/backend_test/plot/BV1d54y1g7db/评论数量统计 - 折线图.png", "C:/Code/GTSI Course/ECE6001/backend_test/plot/BV1d54y1g7db/评论内容_词云图.jpg"]

    #original_text = getAnalysis(user_string, 'gpt-3.5-turbo')  # uncomment this line to use the real API
    # The code below↓ is for demo. To be commented out when using the real API
    original_text = """### Summary and Categorization of Perspectives:\n\n1. **Revealing Unethical Practices**: Several comments highlight how students use answer guides like "全解' to mimic responses during classes, suggesting a lack of original thought and potzdential ethical concerns with overreliance on such materials.\n\n2. **Recalling Past Experiences**: Many users share personal anecdotes from their school days, reminiscing about classmates using answer guides, interactions with teachers, being scolded for using external materials, and moments of humor or awkwardness during class.\n\n3. **Criticism of Teaching Methods**: There is criticism directed at teachers for merely reading from auxiliary materials during classes, leading to a lack of engagement or original teaching methods, which some view as detrimental to the learning process.\n\n### Recommendations for Video Improvement:\n\n1. **Diverse Teaching Strategies**: Encourage teachers to adopt varied teaching strategies beyond reading from answer guides, fostering critical thinking and engagement among students.\n2. **Interactive Sessions**: Promote interactive sessions where students discuss and analyze texts, encouraging active participation and deep understanding.\n3. **Authentic Learning**: Emphasize the value of original thinking and discourage the use of external materials as shortcuts to understanding materials.\n\n### Opportunities for Increased Profit:\n\n1. **Engagement Strategies**: Developing interactive sessions or supplementary materials that promote active learning could attract more viewers and engagement.\n2. **Premium Content**: Offering exclusive content or advanced guides could be monetized to benefit students seeking additional resources.\n3. **Collaborations**: Partnering with educators or experts to create specialized content tailored to specific subject areas could attract a larger audience.\n\nThese strategies aim to improve the educational value of the video content while exploring opportunities for maximizing profitability."""

    additional_strings = re.sub(r'(\d+)\.', '- ', original_text)
    # Returning the URLs and strings as a JSON response
    response = {
        #"imageUrls": generated_image_urls,
        "additionalStrings": additional_strings
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
