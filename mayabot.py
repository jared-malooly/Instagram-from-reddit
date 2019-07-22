###
### For Maya:
### Parses out the important stuff from your posts, and assigns them to a dictonary to be downloaded and posted
### to instagram
###


import praw
from bs4 import BeautifulSoup
import requests
import time

def main():
    r = praw.Reddit(client_id = '1scCXWF6gu7Ecg',
                    client_secret = 'BcRWHiN-UXTagFSlvjgm6m_zQMg',
                    username = 'Mayabot',
                    password = 'Samsung88',
                    user_agent='mayabotV1')

    user = r.redditor('mayaxs')

    get_post_ids(user, r)

def get_post_ids(user, r):
    '''
    Scrapes profile for post IDs and stores used IDs in a text file named
    used_ids_txt so they aren't repeated.
    If a new ID appears (If maya posts something) the porgram will send the post id to
    get_image, where the caption and image will be stripped and stored to be posted to IG

    user: u/mayaxs
    r: reddit instance
    '''

    used_ids = []
    post_ids = []
    new_posts = {}
    used_ids_txt = open('used_ids.txt', 'r')
    #read text file to list of used ids so the program doesnt repeat posts
    for line in used_ids_txt:
        used_ids.append(line.rstrip())
    used_ids_txt.close()
    used_ids_txt = open('used_ids.txt', 'a')
    for submission in user.submissions.new(limit=10):
        time.sleep(5)
        sub = str(submission.subreddit)
        #SHOULD ignore account posts and posts that are already in the used_ids text file
        if submission not in used_ids and sub != "u_mayaxs":
            post_ids.append(submission.id)
            used_ids_txt.write(submission.id + '\n')
            title, link_to_image = get_image(submission.id, submission.title)
            #SHOULD key out duplicate posts!
            new_posts[title] = link_to_image
    if post_ids == []:
        print('All posts accounted for!')
    for key in new_posts:
        print("\n\n")
        print(key)
        print(new_posts[key])
    used_ids_txt.close()

def get_image(id, title):
    '''
    Gets data for post title and image/gif URL and returns to get_post_ids to add to post dictionary

    id: Post id to find HTML file
    title: Title of post
    return: title and URL of image/GIF
    '''
    url = "https://www.reddit.com/" + id + "/"
    web_request = requests.get(url, headers = {'User-agent': 'mayabotV1'})
    data = web_request.text
    soup = BeautifulSoup(data, "html.parser")
    for link in soup.find_all('a', href=True):
        possible_link = (link['href'])
        possible_link = possible_link.split('/')
        for i in possible_link:
            if i == "gfycat.com" or i == "imgur.com" or i == "i.redd.it":
                return title, "/".join(possible_link)

main()
