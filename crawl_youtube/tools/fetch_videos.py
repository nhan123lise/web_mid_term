import json
import time

import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import chromedriver_binary
import os
from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_argument("--headless")
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options


def get_video_links(channel_url, verbose, sleep_time):
    videos_url = channel_url + '/videos'
    options = Options()
    options.headless = True

    # if you get error look at readme file for instructions
    driver = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install())
    driver.get(videos_url)


    time.sleep(sleep_time)

    # scroll dow to the button of the page
    if verbose:
        print("Opening the channel in FireFox and scrolling to the bottom of the page ....")
    while True:
        old_height = driver.execute_script(
            "return document.documentElement.scrollHeight")
        driver.execute_script("window.scrollTo(0, " + str(old_height) + ");")
        time.sleep(sleep_time)
        new_height = driver.execute_script(
            "return document.documentElement.scrollHeight")

        if new_height == old_height:
            break

    # parse the html and get the links for the videos
    soup = bs(driver.page_source, "html.parser")
    video_tags = soup.findAll(
        'a', attrs={'class': 'yt-simple-endpoint style-scope ytd-grid-video-renderer'})

    if verbose:
        print("##################")
        print("Video links:")

    links = []
    for tag in video_tags:
        if 'href' in tag.attrs:
            links.append(tag.attrs['href'])
            if verbose:
                print(tag.attrs['href'])
    return links


def get_video_info(video_url):
    """ gets a youtube video url and returns its info in a json format"""
    information = {'url': video_url}
    response = requests.get(video_url)
    soup = bs(response.content, "html.parser")

    description_tag = soup.find('p', id='eow-description')
    if description_tag:
        information['description'] = description_tag.text
    else:
        information['description'] = ''

    return information


def get_article_title(description):
    """ gets a description of a video in 2 min paper channel and returns the title of article"""

    keyword = 'The paper "'
    try:
        if keyword in description:
            description = description[description.index(
                keyword) + len(keyword):]
            title = description[0:description.index('"')]
        else:
            title = 'unknown'
    except:
        title = 'unknown'
    return title


def crawl_youtube_channel(channel_url, verbose=False, sleep_time=3, links_path=None):
    """ gets a Youtube channel url and returns a dictionary containing info about the videos"""

    if links_path:
        links = []
        links_file = open(links_path, "r")
        lines = links_file.readlines()
        for line in lines:
            links.append(line)
        links_file.close()
    else:
        links = get_video_links(
            channel_url, verbose=verbose, sleep_time=sleep_time)

    return links


if __name__ == '__main__':
    # provide the youtube channel url here
    youtube_url = 'https://www.youtube.com/c/TrungnghiaVlog'
    data = crawl_youtube_channel(youtube_url, verbose=True)

    cur_dir = os.getcwd()
    with open(os.path.join(cur_dir, 'crawl_youtube/Data',  youtube_url.split('/')[-1] + '.txt'), 'w') as outfile:
        json.dump(data, outfile, indent=4)
