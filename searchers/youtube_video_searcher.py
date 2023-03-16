from youtubesearchpython import VideosSearch

SEARCH_LIMIT = 1
DICT_KEY_FOR_RESULT = 'result'
DICT_KEY_FOR_URL = 'link'

def search_for_video_link(text):
    videosSearch = VideosSearch(text, limit=SEARCH_LIMIT).result()
    return videosSearch[DICT_KEY_FOR_RESULT][0][DICT_KEY_FOR_URL] if len(videosSearch[DICT_KEY_FOR_RESULT]) > 0 else None