from bs4 import BeautifulSoup
import requests
import json
import re


# get data from https://www.youtube.com/feed/trending
# parse with lxml

def get_top_video(obj):
    video_list = obj['items']
    items = []
    for video in video_list:
        video_info = video['videoRenderer']
        line = []

        video_id = video_info['videoId']
        line.append(video_id)

        line.append('top')

        video_title = video_info['title']['runs'][0]['text']
        line.append(video_title)

        video_label = video_info['title']['accessibility']['accessibilityData']['label']
        line.append(video_label)

        video_thumbnail = video_info['thumbnail']['thumbnails'][-1]['url']
        line.append(video_thumbnail)

        video_url = 'https://www.youtube.com' + \
                    video_info['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
        line.append(video_url)

        video_view_count = video_info['viewCountText']['simpleText']
        line.append(video_view_count)

        # print(line)

        items.append(line)
    return items


def get_short_video(obj):
    video_list = obj['items']
    items = []
    for video in video_list:
        video_info = video['reelItemRenderer']
        line = []

        video_id = video_info['videoId']
        line.append(video_id)

        line.append('short')

        video_title = video_info['headline']['simpleText']
        line.append(video_title)

        video_label = video_info['accessibility']['accessibilityData']['label']
        line.append(video_label)

        video_thumbnail = video_info['thumbnail']['thumbnails'][-1]['url']
        line.append(video_thumbnail)

        video_url = 'https://www.youtube.com' + \
                    video_info['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
        line.append(video_url)

        video_view_count = video_info['viewCountText']['simpleText']
        line.append(video_view_count)

        # print(line)

        items.append(line)
    return items


def get_now_popular_video(obj):
    video_list = obj['items']
    items = []

    for video in video_list:
        video_info = video['videoRenderer']
        line = []

        video_id = video_info['videoId']
        line.append(video_id)

        line.append('now')

        video_title = video_info['title']['runs'][0]['text']
        line.append(video_title)

        video_label = video_info['title']['accessibility']['accessibilityData']['label']
        line.append(video_label)

        video_thumbnail = video_info['thumbnail']['thumbnails'][-1]['url']
        line.append(video_thumbnail)

        video_url = 'https://www.youtube.com' + \
                    video_info['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
        line.append(video_url)

        video_view_count = video_info['shortViewCountText']['simpleText']
        line.append(video_view_count)

        # print(line)

        items.append(line)
    return items


def get_resent_popular_video(obj):
    video_list = obj['items']
    items = []

    for video in video_list:
        video_info = video['videoRenderer']
        line = []

        video_id = video_info['videoId']
        line.append(video_id)

        line.append('recent')

        video_title = video_info['title']['runs'][0]['text']
        line.append(video_title)

        video_label = video_info['title']['accessibility']['accessibilityData']['label']
        line.append(video_label)

        video_thumbnail = video_info['thumbnail']['thumbnails'][-1]['url']
        line.append(video_thumbnail)

        video_url = 'https://www.youtube.com' + \
                    video_info['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
        line.append(video_url)

        video_view_count = video_info['shortViewCountText']['simpleText']
        line.append(video_view_count)

        # print(line)
        items.append(line)
    return items


def get_youtube_popular_list():
    url = 'https://www.youtube.com/feed/trending?app=desktop&hl=zh-CN&gl=GB'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    pattern = re.compile("var ytInitialData = .")
    script = soup.find("script", string=pattern)
    javascript_code = script.string[script.string.index('=') + 1:-1]
    yt_data = json.loads(javascript_code)
    # print(yt_data)

    items = []

    # get top video
    print('------------------ get top video ------------------')
    top_video_obj_tmp = \
        yt_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content'][
            'sectionListRenderer'][
            'contents'][0]['itemSectionRenderer']['contents'][0]
    if 'shelfRenderer' in top_video_obj_tmp and 'expandedShelfContentsRenderer' in top_video_obj_tmp['shelfRenderer']['content']:
        top_video_obj = top_video_obj_tmp['shelfRenderer']['content']['expandedShelfContentsRenderer']
        items.extend(get_top_video(top_video_obj))
    else:
        print('------------------ get top video -----no data-------------')

    # get short video
    print('------------------ get short video ------------------')
    short_video_obj_tmp = \
        yt_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content'][
            'sectionListRenderer'][
            'contents'][1]['itemSectionRenderer']['contents'][0]
    if 'reelShelfRenderer' in short_video_obj_tmp:
        short_video_obj = short_video_obj_tmp['reelShelfRenderer']
        items.extend(get_short_video(short_video_obj))
    else:
        print('------------------ get short video -----no data-------------')

    # get now popular video
    print('------------------ get now popular video ------------------')
    now_popular_video_obj_tmp = \
        yt_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content'][
            'sectionListRenderer'][
            'contents'][2]['itemSectionRenderer']['contents'][0]
    if 'shelfRenderer' in now_popular_video_obj_tmp and 'expandedShelfContentsRenderer' in now_popular_video_obj_tmp['shelfRenderer']['content']:
        now_popular_video_obj = now_popular_video_obj_tmp['shelfRenderer']['content']['expandedShelfContentsRenderer']
        items.extend(get_now_popular_video(now_popular_video_obj))
    else:
        print('------------------ get now popular video -----no data-------------')

    # get recent popular video
    print('------------------ get recent popular video ------------------')
    resent_popular_video_obj_tmp = \
        yt_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content'][
            'sectionListRenderer'][
            'contents'][3]['itemSectionRenderer']['contents'][0]
    if 'shelfRenderer' in resent_popular_video_obj_tmp and 'expandedShelfContentsRenderer' in resent_popular_video_obj_tmp['shelfRenderer']['content']:
        resent_popular_video_obj = resent_popular_video_obj_tmp['shelfRenderer']['content']['expandedShelfContentsRenderer']
        items.extend(get_resent_popular_video(resent_popular_video_obj))

    print('------------------ all video info ------------------')
    # print(items)
    return items

# if __name__ == '__main__':
#     get_youtube_popular_list()
