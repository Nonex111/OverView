# How to use: Change the directory and csv_file_name in the visualization function, and run the file.
import pandas as pd
import matplotlib.pyplot as plt
from snownlp import SnowNLP  # 中文情感分析库
from wordcloud import WordCloud  # 绘制词云图
import numpy as np
from PIL import Image  # 读取图片
import jieba.analyse  # jieba分词
import matplotlib.dates as mdates


def crop_png(image_path, crop_box):
    with Image.open(image_path) as img:
        cropped_img = img.crop(crop_box)
        cropped_img.save(image_path)

# 一、读取数据
# 读取csv数据
directory = 'plot/BV11w4m1o7Qu/'
csv_file_name = 'b站评论_20240325223606.csv'

def visualization(directory,csv_file_name):
    df = pd.read_csv(directory+csv_file_name)
    # 查看列名
    #print('所有列:\n', df.columns)
    # 查看前3行
    #print('前3行:\n', df.head(3))
    # 查看数据形状
    #print('数据形状:\n', df.shape)
    # 查看每列的信息
    #print('列信息:\n', df.info())

    # 二、数据清洗
    # 统计IP属地的空值
    #print('IP属地1:\n', df['IP属地'].isnull().value_counts())
    # 填充空值
    df['IP属地'].fillna('未知', inplace=True)
    # 再次统计IP属地的空值
    #print('IP属地2:\n', df['IP属地'].isnull().value_counts())
    # 检查重复
    #print('检查重复:\n', df.duplicated().value_counts())

    # 三、可视化分析
    # 设置颜色主题
    plt.style.use('dark_background')
    # 解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    # 3.1 IP属地分析-柱形图
    # 查看前10的地区
    #print(df['IP属地'].value_counts().nlargest(10))
    df['IP属地'].value_counts().nlargest(10).plot.bar(figsize=(12, 6))
    plt.title('IP属地TOP10统计-柱形图')
    plt.xlabel('省份')
    plt.ylabel('数量')
    plt.legend()
    plt.savefig(directory+'IP属地TOP10统计-柱形图.png')
    # plt.show()
    plt.close()
    #print('已生成：IP属地TOP10统计-柱形图.png')
    df['IP属地'].value_counts().plot.pie(autopct='%.2f%%', figsize=(8, 8))  # 画饼图
    plt.title('IP属地')
    plt.savefig(directory+'IP属地-饼图.png')  # 保存图片
    plt.close()

    crop_png(directory+'IP属地-饼图.png', (100, 60, 756, 690))


    # 3.2 评论时间分析-折线图
    start_day = 1
    end_day = 30
    df['评论时间2'] = pd.to_datetime(df['评论时间'])  # 转换为日期格式
    df['评论日期'] = df['评论时间2'].dt.date  # 提取日期
    df_cmt_date = df['评论日期'].value_counts()  # 分组统计数量
    df_cmt_date = df_cmt_date.reset_index()  # 重置索引

    df_cmt_date.columns = ['评论日期', '评论数量']  # 设置列名
    df_cmt_date.sort_values('评论日期', inplace=True)
    df_cmt_date_sliced = df_cmt_date.iloc[start_day:end_day]
    #df_cmt_date_sliced.plot(x='评论日期', y='评论数量', figsize=(12, 6))

    df_cmt_date_sliced.plot(x='评论日期',y='评论数量',alpha=0.8,marker='o',linewidth=1,figsize=(20, 6))
    plt.title('评论数量统计')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.savefig(directory+'评论数量统计-折线图.png')

    # plt.show()
    plt.close()
    #print('已生成：评论数量统计-折线图.png')
    crop_png(directory + '评论数量统计-折线图.png', (210, 40, 1812, 585))


    # 3.4 评论内容-情感分布饼图
    # 情感分析打标
    def sentiment_analyse(v_cmt_list):
        """
        情感分析打分
        :param v_cmt_list: 需要处理的评论列表
        :return:
        """
        score_list = []  # 情感评分值
        tag_list = []  # 打标分类结果
        pos_count = 0  # 计数器-积极
        neg_count = 0  # 计数器-消极
        mid_count = 0  # 计数器-中性

        for comment in v_cmt_list:
            tag = ''
            sentiments_score = SnowNLP(comment).sentiments
            if sentiments_score < 0.2:
                tag = '消极'
                neg_count += df['点赞数']
            elif sentiments_score > 0.3:
                tag = '积极'
                pos_count += df['点赞数']
            else:
                tag = '中性'
                mid_count += df['点赞数']
            score_list.append(sentiments_score)  # 得分值
            tag_list.append(tag)  # 判定结果
        df['情感得分'] = score_list
        df['分析结果'] = tag_list
        grp = df['分析结果'].value_counts()
        grp.plot.pie(autopct='%.2f%%', figsize=(8, 8))  # 画饼图
        plt.title('情感分布')
        plt.savefig(directory+'情感分布-饼图.png')  # 保存图片
        plt.close()
        crop_png(directory+'情感分布-饼图.png', (100, 60, 720, 690))
        # 把情感分析结果保存到excel文件
        df.to_excel(directory+'情感评分结果.xlsx', index=None)
        #print('已生成：情感判定结果.xlsx')

    v_cmt_list = df['评论内容'].values.tolist()  # 评论内容列表
    # print('评论内容总数据量为: ', len(v_cmt_list))
    v_cmt_list = [str(i) for i in v_cmt_list]  # 数据清洗-list所有元素转换成字符串
    v_cmt_str = ' '.join(str(i) for i in v_cmt_list)  # 评论内容转换为字符串
    # 情感分析打分
    sentiment_analyse(v_cmt_list=v_cmt_list)

    # 3.5 评论内容-词云图
    # 停用词
    stopwords = ['的', '了', '我', '你', '都', '就', '也', '是', '还是', '真的', '吧', '吗', '说', '很', '能',
                     '有', '啊', '不', '和', '现在', '这', '没', '就是', '还', '在', '好', '他', '没有', '这个', '给',
                     '被']
     # 初始化词云图对象
    wc = WordCloud(
        background_color="black",  # 背景颜色
        width=1500,  # 图宽
        height=1200,  # 图高
        max_words=100,  # 最多字数
        font_path="C:\Windows\Fonts\simhei.ttf",  # Windows系统字体文件路径
        stopwords=stopwords,  # 停用词
        # mask=np.array(Image.open('背景图2.png')),  # 背景图片
    )
    jieba_text = " ".join(jieba.lcut(v_cmt_str))  # jieba分词
    wc.generate_from_text(jieba_text)  # 生成词云图
    wc.to_file(directory + '评论内容_词云图.jpg')  # 保存图片文件
    #print('已生成：评论内容_词云图.jpg')

    return [directory+'IP属地-饼图.png', directory+"评论数量统计-折线图.png", directory+'情感分布-饼图.png', directory+'评论内容_词云图.jpg']

if __name__ == '__main__':
    visualization(directory,csv_file_name)
