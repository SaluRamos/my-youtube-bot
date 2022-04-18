from scripts.general import create_webdriver
import os

class vars():

    API_KEYS = os.environ.get("MyYoutubeBotYoutubev3APIKeys").split(",")
    print(API_KEYS)
    API_KEY_IN_USE = None
    API_URL = "https://www.googleapis.com/youtube/v3/"
    youtube_api = None
    webdriver = create_webdriver()