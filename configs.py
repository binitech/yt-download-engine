import os

youtube_channel = os.getenv('yt_channel', '')
running_interval = os.getenv('run_interval', 1)
api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
regex_matches = os.getenv('regex_matches', r"(ዉሳኔ ክፍል|Wesane episode|ሥም ክፍል|Matter of Respect)")
chat_id = os.getenv('chat_id', 362993991)
bot_token = os.getenv('bot_token')
