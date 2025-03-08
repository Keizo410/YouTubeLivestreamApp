import os
import requests
import nltk 
from nameparser.parser import HumanName
import numpy

class YouTube:
    def __init__(self):
        """Initilize a YouTube object"""
        pass

    def is_livestream(self, video_id):
        """
        A method to check if a specific video_id is livestream video.

        Parameters:
        video_id - a string for YouTube video id

        Returns:
        boolean - True or False
        """
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
        """
        A method to find a specific video_id out of root text.

        Parameters:
        root - a string that contains video_id.

        Returns:
        videoId - A string for YouTube video id.
        channel_id - A string for YouTube channel id. 
        """
        namespaces = {
            'ns0': 'http://www.w3.org/2005/Atom',
            'ns1': 'http://www.youtube.com/xml/schemas/2015'
        }
        for entry in root.findall('ns0:entry', namespaces):
            videoId = entry.find('ns1:videoId', namespaces).text
            channel_id = entry.find('ns0:author/ns0:name', namespaces).text  
            
        return videoId, channel_id

    def get_channelHolderName(self, text):
        """
        A method to get a channel holder name out of input.

        Parameters:
        text - a string that contains channel description.

        Returns:
        person_list - a list of human name appeared in the description.
        """
        nltk.download('punkt_tab')
        nltk.download('averaged_perceptron_tagger_eng')
        nltk.download('maxent_ne_chunker_tab')
        nltk.download('words')
        tokens = nltk.tokenize.word_tokenize(text)
        pos = nltk.pos_tag(tokens)
        sentt = nltk.ne_chunk(pos, binary = False)
        person_list = []
        person = []
        name = ""
        for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
            for leaf in subtree.leaves():
                person.append(leaf[0])  # Collect parts of the name
            if len(person) > 1:  # If it's a full name (not just a single part)
                full_name = ' '.join(person)  # Join first and last names
                if full_name not in person_list:  # Avoid duplicates
                    person_list.append(full_name)
                person = []  # Reset for the next name
        # for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        #     for leaf in subtree.leaves():
        #         person.append(leaf[0])
        #     if len(person) > 1: 
        #         for part in person:
        #             name += part + ' '
        #         if name[:-1] not in person_list:
        #             person_list.append(name[:-1])
        #         name = ''
        #     person = []
        return person_list

    def get_channelId(self, handle_name):
        """
        A method to get a channel id by search with handle name.

        Parameters:
        handle_name - a string that contains YouTube handle (@....).

        Returns:
        id - a string for channel id 
        title - a string for channel name
        persons - a list of channel holder names
        search_response.status_code - int value for status code of search feature
        """
        API_KEY = os.getenv('API_KEY')
        if not API_KEY:
            raise ValueError("API_KEY is not set in environment variables.")

        # Using search endpoint to find channel by handle
        SEARCH_API_URL = 'https://www.googleapis.com/youtube/v3/channels'
        search_params = {
            'part': 'snippet',
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

        # Extract channel ID & channel name from search results
        id = search_results['items'][0]['id']
        title = search_results['items'][0]['snippet']['title']
        persons = self.get_channelHolderName(f"""{search_results['items'][0]['snippet']['description']}""")

        return id, title, persons, search_response.status_code

