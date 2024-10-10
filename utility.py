import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

class CloudflareVideoUtility:
    def __init__(self):
        self.account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        self.api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        self.api_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/stream"

    def upload_video(self, file_path):
        headers = {
            'Authorization': f'Bearer {self.api_token}'
        }

        # setting domain restrictions
        json_data = {
            'requiredSignedURLs': 'true',
            'allowedOrigins': ['yourdomain.com'],
        }

        # open the video file 
        with open(file_path, 'rb') as video:
            files = {'file': video}

            response = requests.post(self.api_url, headers=headers, files=files, json=json_data)

        if response.status_code == 200:
            result = response.json()['result']
            video_id = result['uid']
            playback_url = result['playback']['hls']
            return {
                'success': True,
                'video_id': video_id,
                'playback_url': playback_url
            }
        else:
            return {
                'success': False,
                'error': response.json()['errors']
            }
        
    def generate_signed_url(self, video_id, exp=None, nbf=None, downloadable=False, access_rules=None):
        Signed_api_url = f'{self.api_url}/{video_id}/token'
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        data = {
            "downloadable": downloadable,
            "exp": exp if exp else int(time.time()) + 3600,
            "nbf": nbf if nbf else int(time.time()) + 3600,
            "access_rules": access_rules if access_rules else []
        }
        response = requests.post(Signed_api_url, headers=headers, json=data)
        if response.status_code == 200:
            tokenized_url = response.json()['result']['token']
            return {
                "success": True,
                'tokenized_url': tokenized_url
            }
        else:
            return {
                "success": False,
                'error': response.json()['errors']
            }
        

if __name__ == "__main__":
    video = CloudflareVideoUtility()
    upload_result = video.upload_video('C:/Users/Desktop/My Video.mp4')

    if upload_result['success']:
        video_id = upload_result['video_id']
        print(f"Video uploaded successfully. ID: {video_id}")
        print(f"Playback URL: {upload_result['playback_url']}")

        access_rules = [
            {"action": "block", "country": ["US", "MX"], "type": "ip.geoip.country"},
            {"action": "allow", "ip": ["93.184.216.0/24"], "type": "ip.src"},
            {"action": "block", "type": "any"},
        ]
        tokenized_result = video.generate_signed_url(video_id, exp=int(time.time()) + 7200, access_rules=access_rules)
        if tokenized_result['success']:
            print(f"Tokenized URL: {tokenized_result['tokenized_url']}")
        else:
            print(f"Failed to generate tokenized URL, Error: {tokenized_result['error']}")
    else:
        print(f"Upload failed. Error: {upload_result['error']}")