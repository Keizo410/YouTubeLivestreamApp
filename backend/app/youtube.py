import os
import requests

class YouTube:
    def __init__(self):
        pass

    def is_livestream(self, video_id):
        API_KEY = os.getenv('API_KEY')
        YOUTUBE_API_URL = os.getenv('API_URL')
        params = {
            'id': video_id,
            'part': 'snippet, liveStreamingDetails',
            'key': API_KEY
        }
        response = requests.get(YOUTUBE_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                item = data['items'][0]
                if 'liveStreamingDetails' in item:
                    return True
        return False
    
    
    def get_videoId(self, root):
        namespaces = {
            'ns0': 'http://www.w3.org/2005/Atom',
            'ns1': 'http://www.youtube.com/xml/schemas/2015'
        }
        for entry in root.findall('ns0:entry', namespaces):
            videoId = entry.find('ns1:videoId', namespaces).text
            return videoId
    
    def get_channelId(self, handle_name):
        API_KEY = os.getenv('API_KEY')
        if not API_KEY:
            raise ValueError("API_KEY is not set in environment variables.")

        # Using search endpoint to find channel by handle
        SEARCH_API_URL = 'https://www.googleapis.com/youtube/v3/channels'
        search_params = {
            'part': 'id',
            'forHandle': handle_name,
            'key': API_KEY
        }
        search_response = requests.get(SEARCH_API_URL, params=search_params)

        if search_response.status_code != 200:
            raise Exception(
                f"Search API failed with status {search_response.status_code}: {search_response.text}"
            )

        search_results = search_response.json()
        if 'items' not in search_results or not search_results['items']:
            raise Exception(f"No channel found for handle: {handle_name}")

        # Extract channel ID from search results
        id = search_results['items'][0]['id']

        return id, search_response.status_code
