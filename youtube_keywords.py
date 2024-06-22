import csv
import time
import os
import sys
import gpt4
import requests
import json
import re
import ssl

from bs4 import BeautifulSoup
import youtube_api_proxy


def get_youtube_video_info(url):
    # print("geting info from youtube...")
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    # print("parsing information from youtybe...")
    pattern = re.compile("var ytInitialPlayerResponse = .")
    script = soup.find("script", string=pattern)
    javascript_code = script.string[script.string.index('=') + 1:-1]
    yt_data = json.loads(javascript_code)
    # print(yt_data)
    videoDetails = yt_data['videoDetails']
    # print(videoDetails)
    videoId = yt_data['videoDetails']['videoId']
    # print("videoId="+videoId)
    title = yt_data['videoDetails']['title']
    # print("title="+title)
    description = yt_data['videoDetails']['shortDescription']
    # print("description="+description)
    # print("get information from youtube------:")
    result = {'title': title, 'description': description}
    # print(result)
    return result

def get_youtube_video_keywords(items):
    ind = 0
    for item in items:
        ind = ind +1
        print(str(ind)+":"+item[1]+"------------>"+item[5])
        # if ind > 10:
        #     break
        content = get_youtube_video_info(item[5])
        #print("Youtube video info :"+json.dumps(content))
        keywords = gpt4.get_keywords_by_content(content['title'] + content['description'])
        print(keywords)
        item.append(keywords)
    return items

def sink_youtube_video_info_to_csv(items):
    root_path = os.getenv('OPENAI_DATA_ROOT')
    items.insert(0, ["id","video_type","title","label","thumbnail","url","view_count","keywords"])

    # Name of csv file
    time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    filename = root_path+"youtube_"+time_str+".csv"
    # Writing to csv file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # Writing the data rows
        csvwriter.writerows(items)
    print("sink to csv file -------------------------------->"+filename)

dt_time = ''
if __name__ == '__main__':
    if len(sys.argv) > 1:
        dt_time = sys.argv[1]
    print('dt_time=', dt_time)
    videos = youtube_api_proxy.get_youtube_popular_list()
    items = get_youtube_video_keywords(videos)
    sink_youtube_video_info_to_csv(items)
