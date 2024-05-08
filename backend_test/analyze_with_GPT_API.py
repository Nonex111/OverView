# Description: This file is used to analyze the comments of a video with GPT API.
# The comments are extracted from a csv file, and the comments are summarized and categorized with the number of likes as the weight.
# How to use: Change the directory to the path of the csv file(line 17), add your additional prompts if you want, and run the file.
import openai
import tiktoken
import datetime
import pandas as pd


def getAnalysis(additional_prompt, gpt_model):
    encoding = tiktoken.get_encoding("cl100k_base")  # inclue GPT-4 and GPT-3.5-turbo
    client = openai.OpenAI(api_key='your-openai-api-key')
    prompt = "I'll provide you all the comments and theirs likes from a video. I want you to:1.summarize and categorize the comments, with the number of likes as the weight. 2.give some recommendations on how to improve this video based on these comments 3.if there are any possible opportunities to gain more profit. "
    if additional_prompt:
        prompt += "4." + additional_prompt

    directory = 'C:/Code/GTSI Course/ECE6001/backend_test/plot/BV15s4y1a7q1/'
    df = pd.read_csv(directory+'b站评论_20240320215947.csv')
    # take the "评论内容" that the username is "AI视频小助理"
    #video_summary = df[df['评论作者'] == 'AI视频小助理']
    #comments = str(video_summary['评论内容'].values.tolist())
    # take the"评论内容","点赞数" two columns of the csv file
    df = df[["评论内容", "点赞数"]]
    # convert the dataframe to a list
    comments = str(df.values.tolist())
    # remove the "\'" and "\\n" combo in the string
    comments = comments.replace("\'","").replace("\\n","")

    whole_prompt = prompt + comments
    tokens = len(encoding.encode(whole_prompt))
    if gpt_model == 'gpt-3.5-turbo' and tokens > 16385:
        whole_prompt = whole_prompt[:13500]


    # get current date with the format like "2021-09-01"
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI, based on the "
                                         + gpt_model + " architecture.\nKnowledge cutoff: 2021-09\nCurrent date: "+now,
            "role": "user", "content": whole_prompt,
        }],
        model=gpt_model,
        stream=False
    )

    return chat_completion.choices[0].message.content

if __name__ == '__main__':
    print(getAnalysis("", 'gpt-3.5-turbo'))
