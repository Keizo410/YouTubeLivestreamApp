import requests
import os 

class WebSub:
    def __init__(self):
        pass
    def get_grok_url(self):
        try:
            response = requests.get('http://ngrok:4040/api/tunnels')
            tunnels = response.json().get('tunnels', [])
            for tunnel in tunnels:
                if tunnel['proto'] == 'https':
                    return tunnel['public_url'] + "/youtube-callback"
            return None
        except Exception as e:
            print("Error in get_grok_url function: ", e)

    def subscribe_to_channel(self, channelId):
        print("Subscription started...")
        hub_url = os.getenv('HUB_URL')
        topic_url = os.getenv('BASE_TOPIC_URL')+channelId
        callback_url = self.get_grok_url() or os.getenv('CALLBACK_URL')

        data = {
            'hub.mode': 'subscribe',
            'hub.topic': topic_url,
            'hub.callback': callback_url,
        }
        response = requests.post(hub_url, data=data)
        if response.status_code == 202:
            print('Subscribed successfully!')
            return 201
        else:
            print("Failed to subscribe: ", response.status_code, response.text)
            return response.status_code


    