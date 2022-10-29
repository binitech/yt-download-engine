from pytube import Channel
from time import process_time
import re
from pytube.exceptions import LiveStreamError
from pyrogram import Client
import schedule
import datetime
import os
from configs import api_id, api_hash, youtube_channel, running_interval, regex_matches, chat_id

print('started at', datetime.datetime.now())


bot = Client('bot', api_id, api_hash)
bot.start()
id_trash = eval(open('id_trash.txt', 'r').read())


def update_id(vid):
    """Update channel id store if new id available"""
    id_trash.append(vid)
    open('id_trash.txt', 'w').write(f'{id_trash}')


def get_channel():
    """Recursive function to find list of videos from given channel"""
    channel = Channel(youtube_channel)
    if len(channel) > 15:
        return channel
    else:
        return get_channel()


def find_video():
    """Function to find new video from given channel and sending the video to telegram chat"""
    print(datetime.datetime.now())
    start = process_time()
    ch = get_channel()
    print(len(ch))
    for video in ch.videos[:10]:
        if video.video_id not in id_trash:
            if re.match(regex_matches, video.title):
                if video.vid_info['playabilityStatus']['status'] == 'OK':
                    print(video.title)
                    try:
                        stream = video.streams.filter(resolution='720p', progressive=True,  file_extension='mp4')[0]
                        dow = stream.download()
                        if dow:
                            print('downloaded')
                            bot.send_video(chat_id, dow, duration=video.length, thumb='thumb.png')
                            # update_id(video.video_id)
                            os.remove(dow)
                    except LiveStreamError:
                        print('passed')
            else:
                id_trash.append(video.video_id)

    end = process_time()
    print(f'Finished in {end - start} seconds at', datetime.datetime.now())


# Scheduler to run the program on a given interval
schedules = schedule.Scheduler()
schedules.every(running_interval).minutes.do(find_video)

while True:
    schedules.run_pending()
