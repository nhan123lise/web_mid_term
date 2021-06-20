from multiprocessing import Pool
from tools.fetch_videos import crawl_youtube_channel
from tools.fetch_comments_1 import crawl_comments

import time
import os
import json

from datetime import datetime

from apscheduler.scheduler import Scheduler

# Start the scheduler
sched = Scheduler()
sched.start()


def fetch_videos(youtube_url='https://www.youtube.com/c/TrungnghiaVlog'):
    cur_dir = os.getcwd()
    data_path = os.path.join(cur_dir, 'crawl_youtube/Data',
                             youtube_url.split('/')[-1] + '.txt')

    ex_data = set()

    if os.path.isdir(data_path):
        with open(data_path, 'r') as f:
            for line in f:
                ex_data.add(line)

    data = set(crawl_youtube_channel(youtube_url, verbose=True))

    with open(os.path.join(cur_dir, 'crawl_youtube/Data',  youtube_url.split('/')[-1] + '.txt'), 'w') as outfile:
        json.dump(list(data), outfile, indent=4)

    new_video_ids = list(data - ex_data)
    new_video_ids = [temp[9:] for temp in new_video_ids]

    new_comments = crawl_comments(new_video_ids)

    new_comments.to_csv('chuibay.csv', mode='a', header=False)
    return f'finished {data_path}'


youtube_channels = ['https://www.youtube.com/channel/UChk4_qcmkz547QYBr89FkNg',
                    'https://www.youtube.com/channel/UCSbMQSGCdZvgpaQP32ianjQ']

# with open('/Users/mac/Desktop/crawl_youtube/channels.txt', 'r') as f:
#     for line in f:
#         youtube_channels.append(line.strip())


def job():
    with Pool(3) as p:
        print(p.map(fetch_videos, youtube_channels))


# Schedule fetch video to be called every 7 days

sched.add_interval_job(job, minutes=1, start_date=str(datetime.now()))
print('Fetch videos has been scheduled for every 7 days')


if __name__ == '__main__':
    while True:
        try:
            time.sleep(1)
        except (Exception, KeyboardInterrupt):
            sched.shutdown()
            exit()
