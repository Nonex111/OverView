# Overview

### This is a web app, which is basically scraping and analyzing comments of a video from Bilibili, showing some plots about the statistics of all comments and some text analyses generated by calling the OpenAI API.

All the technical stuff are done by one member with the role of technical expert. Due to lack of time, the functionality about scraping comments and sending the result plots to the frontend is incomplete, but its implementation is similar to the process of interaction between frontend and backend when calling the OpenAI API for analyses, if you want to realize that.
The part of calling theOpenAI API is commented for the fluency of demo, you can reproduce that functionality by uncommenting it, which is specified in step 4 below.


### Simple version: Steps to reproduce the demo 
>(Just to show the workflow, no actual interaction between frontend and backend. Pages are static.)
- 1.In the frontend folder, modify all the paths in all html files 
- 2.Open the home-page.html


### Full version: Steps to test all the functionalities/continue on this project
>(You have to make more twists to reproduce all the functionalities)
- 1.Install requirements.txt in the backend folder
- 2.In the frontend folder, modify all the paths in all html files 
- 3.Add your OpenAI API key in basic_flask_app.py at line 57
- 4.In basic_flask_app.py at line 62 to 64, do some commenting and uncommenting
- 5.Run basic_flask_app.py as the server
- 6.Open the home-page.html
- 7.You can try the functionality of calling the OpenAI API in Analyze-page-II.html


---
## About each back-end file
- ### Bilibili_comments_scraping.py
- **Description:** Scraping comments from Bilibili
- **How to use:** Change the share_info variable to the video sharing link you want to crawl, then run the program. The result is saved in a csv file in "plot/BVxxxxxxx/"
- ##### P.S. The cookie in the headers variable needs to be updated regularly, otherwise the location cannot be crawled.




- ### Visualization.py
- **Description:** Generate four plots from the comments scraped.
- **How to use:** Change the directory and csv_file_name in the visualization function, and run the program. The result is saved in directory path: "plot/BVxxxxxxx/"

- ### analyze_with_GPT_API.py
- **Description:** This file is used to analyze the comments of a video with GPT API. The comments are extracted from a csv file, and the comments are summarized and categorized with the number of likes as the weight.
- **How to use:** Change the directory to the path of the csv file(line 17), add your additional prompts if you want, then run the program.

### (The first three python programs can run independently.)

- ### basic_flask_app.py
- **Description:**  This is a basic Flask app that receives a string from the frontend, processes it(calls GPT API), and returns the response. It listens on port 5000 and receives requests from Analyze-page-II.
- **How to use:** Make sure you comment the code for demo first. Run this file as the server, and send requests by clicking the "Analyze" button on Analyze-page-II.




