import csv
import pandas as pd
import googleapiclient.discovery

# Your API Key. See readme for more info.
# DEVELOPER_KEY = "AIzaSyDHSML5WW5n8JI03D1nblOsqXH2iW-FKqQ"
# DEVELOPER_KEY = "AIzaSyBCQZ8gYbaD5Zsb0cGWotxazGCyHTX1vMc"
# DEVELOPER_KEY = "AIzaSyCmksh3PppyMY3c9WOyvjL_In59Ffazp_U"
# DEVELOPER_KEY = "AIzaSyBgYhUMv42MlNVfBTVEiE4-0Eu_UY1EBFo"
# DEVELOPER_KEY = "AIzaSyDcrp8m8g0RpF5cmg3fPd1p4-ceNwxZtKY"
# DEVELOPER_KEY = "AIzaSyA0a9Pf6GPAx1r7YEHKDrNNDl-W3GKccPw"
# DEVELOPER_KEY = "AIzaSyBmwigMXZthtJEsaM7Avm9pZcS198lXoVY"


# Video ID of youtube video you want to scrape
VIDEO_ID = "JXhWyqy7iHM"

api_service_name = "youtube"
api_version = "v3"


# youtube = googleapiclient.discovery.build(
#     api_service_name, api_version, developerKey=DEVELOPER_KEY)


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


def get_comments(youtube, id_list, list_comments):
    next_page_token = ''
    while True:
        # Check ID VIDEO
        # Get IG to fetch comments and break while false
        if len(id_list) > 0:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=id_list.pop(),
                pageToken=next_page_token)

            try:
                response = request.execute()
            except Exception as e:
                print(e)
                break

            next_page_token = response.get('nextPageToken', None)

            all_comments = response['items']
            for comment in all_comments:
                # writer.writerow({"text": comment['snippet']['topLevelComment']['snippet']['textOriginal']})
                number_of_replies = comment['snippet']['totalReplyCount']
                list_comments.append(
                    comment['snippet']['topLevelComment']['snippet']['textOriginal'])
                print(comment['snippet']['topLevelComment']
                      ['snippet']['textOriginal'])

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
                            # writer.writerow({"text": reply['snippet']['textOriginal']})
                            list_comments.append(
                                reply['snippet']['textOriginal'])
                            print(reply['snippet']['textOriginal'])
                        if not next_reply_page:
                            break

            if not next_page_token:
                break
        else:
            break


def main():
    DEVELOPER_KEYS = ['AIzaSyDHSML5WW5n8JI03D1nblOsqXH2iW-FKqQ', 'AIzaSyBCQZ8gYbaD5Zsb0cGWotxazGCyHTX1vMc',
                      'AIzaSyCmksh3PppyMY3c9WOyvjL_In59Ffazp_U', 'AIzaSyBgYhUMv42MlNVfBTVEiE4-0Eu_UY1EBFo',
                      'AIzaSyDcrp8m8g0RpF5cmg3fPd1p4-ceNwxZtKY', 'AIzaSyA0a9Pf6GPAx1r7YEHKDrNNDl-W3GKccPw',
                      'AIzaSyBmwigMXZthtJEsaM7Avm9pZcS198lXoVY']

    # Create a list contains all IDs
    with open('../Data/chuongsrtv.txt') as f:
        id_list = f.readlines()
        f.close()
    id_list = [i.strip() for i in id_list]

    # Create a list contains all comments -> finish write all comments to file
    list_comments = []

    while len(DEVELOPER_KEYS) > 0:
        try:
            # DEVELOPER_KEYS.pop()
            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, developerKey=DEVELOPER_KEYS.pop())

            get_comments(youtube, id_list, list_comments)
        except Exception as e:
            continue

    feed_df = pd.DataFrame({'text': list_comments})
    feed_df.to_csv('chuibay.csv')


def crawl_comments(list_ids):
    DEVELOPER_KEYS = ['AIzaSyDHSML5WW5n8JI03D1nblOsqXH2iW-FKqQ', 'AIzaSyBCQZ8gYbaD5Zsb0cGWotxazGCyHTX1vMc',
                      'AIzaSyCmksh3PppyMY3c9WOyvjL_In59Ffazp_U', 'AIzaSyBgYhUMv42MlNVfBTVEiE4-0Eu_UY1EBFo',
                      'AIzaSyDcrp8m8g0RpF5cmg3fPd1p4-ceNwxZtKY', 'AIzaSyA0a9Pf6GPAx1r7YEHKDrNNDl-W3GKccPw',
                      'AIzaSyBmwigMXZthtJEsaM7Avm9pZcS198lXoVY']

    # Create a list contains all IDs
    id_list = list_ids

    # Create a list contains all comments -> finish write all comments to file
    list_comments = []

    while len(DEVELOPER_KEYS) > 0:
        try:
            # DEVELOPER_KEYS.pop()
            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, developerKey=DEVELOPER_KEYS.pop())

            get_comments(youtube, id_list, list_comments)
        except Exception as e:
            continue

    feed_df = pd.DataFrame({'text': list_comments})

    return feed_df


if __name__ == "__main__":
    main()
