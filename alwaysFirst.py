import json
import re
import requests
import urllib
import time
import pickle
import os

from selenium import webdriver
from pytube import YouTube
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError


# 0Auth Stuff
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
channel_id =''

# This authenticates the user that wants to be "first" on the video
def get_authenticated_service():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    #  Check if the credentials are invalid or do not exist
    if not credentials or not credentials.valid:
        # Check if the credentials have expired
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_console()

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

# This fuctions gets the most recent video id from a desire channel.
def newUploadId():
    api_key = "AIzaSyDjiporEA3z0T8riyrm-qgycE0qaaqPVtI"
    channel_id = "UCX6OQ3DkcsbYNE6H8uQQuVA"

    baseVideoUrl = 'https://www.youtube.com/watch?v='
    baseSearchUrl = 'https://www.googleapis.com/youtube/v3/search?'

    url = baseSearchUrl + 'key={}&channelId={}&part=snippet,id&order=date&maxResults=1'.format(api_key, channel_id)
    inp = urllib.urlopen(url)
    resp = json.load(inp)

    videoId = resp['items'][0]['id']['videoId']

    return(videoId)

# Gets title of most recent video
#def newUploadTitle():
    

# Deploys the comment on the most recent video
def insert_comment(service, channel_id, video_id, text):
    insert_result = service.commentThreads().insert(
        part="snippet",
        body=dict(
            snippet=dict(
                channelId=channel_id,
                videoId=video_id,
                topLevelComment=dict(
                    snippet=dict(
                        textOriginal=text)
                )
            )
        )
    ).execute()

    comment = insert_result["snippet"]["topLevelComment"]
    author = comment["snippet"]["authorDisplayName"]
    text = comment["snippet"]["textDisplay"]
    print("you're first")
    
    


# Checks to see if the user has already been authenticated
if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()


# Comments on the most recent video on the desired channel
insert_comment(service, channel_id, newUploadId(), "first")



    

