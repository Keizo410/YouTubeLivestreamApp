import os
import pytest
from unittest.mock import patch, MagicMock, Mock
from utilities.youtube import YouTube
from nltk.tree import Tree

sample_api_response = {
    'items': [{
        'id': 'UC1234567890',
        'snippet': {
            'title': 'Sample Channel',
            'description': 'This is a sample channel description with John Doe and Jane Smith.'
        }
    }]
}

expected_id = 'UC1234567890'
expected_title = 'Sample Channel'
expected_persons = ['John Doe', 'Jane Smith']

sample_text = '''
    John Doe and Jane Smith are the owners of the YouTube channel. 
    Their channel is dedicated to tech tutorials.
    '''

@patch('requests.get')
def test_is_livestream(mock_get):
    """Test the is_livestream method."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'items': [{'snippet': {}, 'liveStreamingDetails': {}}]
    }
    mock_get.return_value = mock_response

    youtube = YouTube()
    result = youtube.is_livestream("sample_video_id")

    assert result is True  

    mock_response.json.return_value = {'items': [{}]}  
    result = youtube.is_livestream("sample_video_id")
    assert result is False  

@patch('requests.get')
def test_get_videoId(mock_get):
    """Test the get_videoId method."""
    youtube = YouTube()

    mock_entry = MagicMock()
    mock_entry.find.return_value.text = 'sample_video_id'  
    mock_author_name = MagicMock()
    mock_author_name.text = 'sample_channel_id'  

    mock_root = MagicMock()
    mock_root.findall.return_value = [mock_entry]  

    mock_entry.find.side_effect = [MagicMock(text='sample_video_id'), mock_author_name]

    video_id, channel_id = youtube.get_videoId(mock_root)

    assert video_id == 'sample_video_id'
    assert channel_id == 'sample_channel_id'


def test_get_channelHolderName():
    """Test get_channelHolderName method."""
    youtube = YouTube()
    sample_text = """
    John Doe and Jane Smith are the owners of the YouTube channel. 
    Their channel is dedicated to tech tutorials.
    """
    
    with patch('nltk.tokenize.word_tokenize') as mock_tokenize, \
         patch('nltk.pos_tag') as mock_pos_tag, \
         patch('nltk.ne_chunk') as mock_ne_chunk:

        mock_tokenize.return_value = ['John', 'Doe', 'and', 'Jane', 'Smith', 'are', 'the', 'owners']
        mock_pos_tag.return_value = [('John', 'NNP'), ('Doe', 'NNP'), ('and', 'CC'), 
                                     ('Jane', 'NNP'), ('Smith', 'NNP'), ('are', 'VBP'), 
                                     ('the', 'DT'), ('owners', 'NNS')]

        mock_ne_chunk.return_value = Tree('S', [
            Tree('PERSON', [('John', 'NNP'), ('Doe', 'NNP')]),
            ('and', 'CC'),
            Tree('PERSON', [('Jane', 'NNP'), ('Smith', 'NNP')])
        ])
        
        person_list = youtube.get_channelHolderName(sample_text)

        assert person_list == ['John Doe', 'Jane Smith']

def test_get_channelId_success():
    """Test get_channelId when the API response is successful."""
    youtube = YouTube()
    
    handle_name = '@samplehandle'
    
    with patch.dict(os.environ, {'API_KEY': 'mock_api_key'}):
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_api_response
            mock_get.return_value = mock_response
            
            with patch.object(youtube, 'get_channelHolderName', return_value=expected_persons):
                
                id, title, persons, status_code = youtube.get_channelId(handle_name)
                
                assert id == expected_id
                assert title == expected_title
                assert persons == expected_persons
                assert status_code == 200

def test_get_channelId_no_channel_found():
    """Test get_channelId when no channel is found."""
    youtube = YouTube()
    
    handle_name = '@nonexistenthandle'
    
    with patch.dict(os.environ, {'API_KEY': 'mock_api_key'}):
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'items': []}
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception, match=f"No channel found for handle: {handle_name}"):
                youtube.get_channelId(handle_name)

def test_get_channelId_api_error():
    """Test get_channelId when the API request fails."""
    youtube = YouTube()
    
    handle_name = '@samplehandle'
    
    with patch.dict(os.environ, {'API_KEY': 'mock_api_key'}):
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500  # Simulate a server error
            mock_response.text = 'Internal Server Error'
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception, match="Search API failed with status 500: Internal Server Error"):
                youtube.get_channelId(handle_name)