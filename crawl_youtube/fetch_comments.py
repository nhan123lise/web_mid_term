import csv

import googleapiclient.discovery

# Your API Key. See readme for more info.
# DEVELOPER_KEY = "AIzaSyDHSML5WW5n8JI03D1nblOsqXH2iW-FKqQ"
# DEVELOPER_KEY = "AIzaSyBCQZ8gYbaD5Zsb0cGWotxazGCyHTX1vMc"
# DEVELOPER_KEY = "AIzaSyCmksh3PppyMY3c9WOyvjL_In59Ffazp_U"
# DEVELOPER_KEY = "AIzaSyBgYhUMv42MlNVfBTVEiE4-0Eu_UY1EBFo"
# DEVELOPER_KEY = "AIzaSyDcrp8m8g0RpF5cmg3fPd1p4-ceNwxZtKY"
# DEVELOPER_KEY = "AIzaSyA0a9Pf6GPAx1r7YEHKDrNNDl-W3GKccPw"
DEVELOPER_KEY = "AIzaSyBmwigMXZthtJEsaM7Avm9pZcS198lXoVY"


# Video ID of youtube video you want to scrape
VIDEO_ID = "JXhWyqy7iHM"

api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)


def top_level_info(comment: dict):
    """
    For a given comment, return dictionary of author name, comment text,
    like and reply count.
    """

    author_name = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
    comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
    like_count = comment['snippet']['topLevelComment']['snippet']['likeCount']
    reply_count = comment['snippet']['totalReplyCount']

    return {'Author': author_name, 'Comment Text': comment_text,
            'Likes': like_count, 'Replies': reply_count}


def child_info(reply: dict):
    """
    For a given reply, return dictionary of author name, reply
    text and reply count.
    """

    reply_text = reply['snippet']['textOriginal']

    return {'text': reply_text}


def main():
    with open('chuibay.csv', mode='a') as f:
        column_names = ["text"]
        writer = csv.DictWriter(f, fieldnames=column_names)
        writer.writeheader()

        next_page_token = ''
        with open("/Users/mac/Desktop/crawl_youtube/crawl_youtube/Data/TrungnghiaVlog.txt") as file:
            for line in file:
                print(line)
                VIDEO_ID = line.rstrip("\n")
                while True:
                    request = youtube.commentThreads().list(
                        part="snippet",
                        videoId=VIDEO_ID,
                        pageToken=next_page_token)

                    try:
                        response = request.execute()
                    except Exception as e:
                        print(e)

                    next_page_token = response.get('nextPageToken', None)

                    all_comments = response['items']
                    for comment in all_comments:
                        writer.writerow({"text": comment['snippet']['topLevelComment']['snippet']['textOriginal']})
                        number_of_replies = comment['snippet']['totalReplyCount']

                        if number_of_replies != 0:
                            next_reply_page = ''
                            while True:
                                request = youtube.comments().list(
                                    part='snippet',
                                    parentId=comment['id'],
                                    pageToken=next_reply_page)

                                response = request.execute()
                                next_reply_page = response.get('nextPageToken', None)
                                replies = response['items']

                                for reply in replies:
                                    writer.writerow({"text": reply['snippet']['textOriginal']})

                                if not next_reply_page:
                                    break

                    if not next_page_token:
                        break



if __name__ == "__main__":
    main()
