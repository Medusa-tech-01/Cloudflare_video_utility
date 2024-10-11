# Cloudflare Video Python Utility Function

## Description
This Python utility interacts with Cloudflare's Stream API, providing functions to upload videos, generate signed URLs with optional access control rules, and handle domain-restricted video playback. It's designed to automate video management on Cloudflare's platform and includes functionality for adding custom security to your video content.

## Installation

Prerequisites
Python 3.x
Cloudflare account with Stream API enabled.
An API token with the necessary permissions (Account Stream Write).

1> Clone the repository:

git clone https://github.com/your-username/cloudflare-video-utility.git
cd cloudflare-video-utility

2> Set up a virtual environment (optional but recommended):

python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
.\venv\Scripts\activate   # For Windows

3> Install dependencies:

pip install -r requirements.txt

4> Set up environment variables for your Cloudflare API credentials:

export CLOUDFLARE_API_TOKEN='your_api_token'
export CLOUDFLARE_ACCOUNT_ID='your_account_id'

5> Or create a .env file in the project root with the following:

CLOUDFLARE_API_TOKEN=your_api_token
CLOUDFLARE_ACCOUNT_ID=your_account_id

6> Update the Domain Restriction: In the upload_video function, replace 'yourdomain.com' with the actual domain you want to allow for video playback.


## Usage
1> Upload a Video
To upload a video to Cloudflare, use the upload_video method.

Example usage:
from cloudflare_video_utility import CloudflareVideoUtility

video = CloudflareVideoUtility()
upload_result = video.upload_video('path/to/your/video.mp4')

if upload_result['success']:
    print(f"Video uploaded successfully. ID: {upload_result['video_id']}")
    print(f"Playback URL: {upload_result['playback_url']}")
else:
    print(f"Upload failed. Error: {upload_result['error']}")



2> Generate a Signed URL with Access Control
You can generate signed URLs with optional expiration, not-before (nbf) times, and access control rules.

Example usage:
from cloudflare_video_utility import CloudflareVideoUtility
import time

video = CloudflareVideoUtility()

access_rules = [
    {"action": "block", "country": ["US", "MX"], "type": "ip.geoip.country"},
    {"action": "allow", "ip": ["93.184.216.0/24"], "type": "ip.src"},
    {"action": "block", "type": "any"}
]

tokenized_result = video.generate_signed_url(
    video_id='your_video_id', 
    exp=int(time.time()) + 7200,  # Expiration in 2 hours
    access_rules=access_rules
)

if tokenized_result['success']:
    print(f"Tokenized URL: {tokenized_result['tokenized_url']}")
else:
    print(f"Failed to generate tokenized URL. Error: {tokenized_result['error']}")

