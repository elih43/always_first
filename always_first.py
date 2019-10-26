import json
import re
import requests
import urllib

from pytube import YouTube

class Helper:
    def __init__(self):
        pass

    def title_to_underscore_title(self, title):
        title = re.sub('[\W_]+', "_", title)
        return title.lower()

    def id_from_url(self, url):
        return url.rsplit("/", 1)[1]

class YouTubeStats:
    def __init__(self, url):
        self.json_url = urllib.urlopen(url)
        self.json_url = requests.get(url)
        self.data = json.loads(self.json_url.text)
        
    def print_data(self):
        print(self.data)

    def get_video_title(self):
        return self.data["items"][0]["snippet"]["title"]

    def get_video_description(self):
        return self.data["items"][0]["snippet"]["description"]


api_key = "AIzaSyDjiporEA3z0T8riyrm-qgycE0qaaqPVtI"

link_file = "links.csv"

with open(link_file, "r") as f:
    content = f.readlines()

content = list(map(lambda s: s.strip(), content))
content = list(map(lambda s: s.strip(','), content))

helper = Helper()

for youtube_url in content:
    video_id = helper.id_from_url(youtube_url)
    url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id=" + video_id + "&key=" + api_key
    yt_stats = YouTubeStats(url)
    title = yt_stats.get_video_title()
    title = helper.title_to_underscore_title(title)

    description = yt_stats.get_video_description()

    #data = yt_stats.print_data()
    print(title)