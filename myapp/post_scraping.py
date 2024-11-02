import googleapiclient.discovery
import googleapiclient.errors
import numpy as np
import requests
import os
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

developer_key_youtube = os.getenv("DEVELOPER_KEY_YOUTUBE")
twitter_api = os.getenv("API_KEY_TWITTER")
instagram_api = os.getenv("API_KEY_INSTAGRAM")


def youtube_scrap(link):
    res = []
    # vid_id = str(link)
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = developer_key_youtube

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=link,
        maxResults=100
    )
    response = request.execute()

    for item in response['items']:
        res.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])

    return np.array(res)

def twitter_scrap(link):
    results = []
    url = "https://twitter241.p.rapidapi.com/comments"
    querystring = {"pid":link.split('/')[-1].split('?')[0],"count":"100"}
    headers = {
        "X-RapidAPI-Key": twitter_api,
        "X-RapidAPI-Host": "twitter241.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    n = len(response.json()['result']['instructions'][0]['entries'])

    for i, post in enumerate(response.json()['result']['instructions'][0]['entries']):
        if i == 0:
            results.append(post['content']['itemContent']['tweet_results']['result']['legacy']['full_text'])
        elif i == n-1:
            break
        else:
            results.append(post['content']['items'][0]['item']['itemContent']['tweet_results']['result']['legacy']['full_text'])

    return np.array(results)

def instagram_scrap(link):
    results=[]
    url = "https://instagram-scraper-api2.p.rapidapi.com/v1/comments"
    querystring = {"code_or_id_or_url":link}
    headers = {
        "X-RapidAPI-Key": instagram_api,
        "X-RapidAPI-Host": "instagram-scraper-api2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.json()['data']['additional_data']['caption']['text']:
        results.append(response.json()['data']['additional_data']['caption']['text'])

    for comm in response.json()['data']['items']:
        results.append(comm['text'])

    return np.array(results)
