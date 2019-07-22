import praw
from bs4 import BeautifulSoup
import requests
import time
import urllib.request
import random

def main():
    r = praw.Reddit(client_id = '1scCXWF6gu7Ecg',
                    client_secret = 'BcRWHiN-UXTagFSlvjgm6m_zQMg',
                    username = 'Mayabot',
                    password = 'CoolPasswordDude',
                    user_agent='mayabotV1')

    user = r.redditor('mayaxs')

    get_post_ids(user, r)

def get_post_ids(user, r):
    '''
    Scrapes profile for post IDs and stores used IDs in a text file named
    used_ids_txt so they aren't repeated.
    If a new ID appears (If maya posts something) the program will send the post id to
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

        #time.sleep(5) #For use in final in case the rpi requests too often

        sub = str(submission.subreddit)
        if sub == "u_mayaxs":
            print("Crap! Self post")
        #SHOULD ignore account posts and posts that are already in the used_ids text file
        if submission not in used_ids and sub != "u_mayaxs":
            post_ids.append(submission.id)
            used_ids_txt.write(submission.id + '\n')
            title, link_to_image, id = get_image(submission.id, submission.title)
            #SHOULD key out duplicate posts!
            new_posts[title] = [link_to_image, id]
    if post_ids == []:
        print('All posts accounted for!')

    #Decides which API to use to download image/gif
    for key in new_posts:
        type = []
        type = new_posts[key][0].split("/")
        if "i.redd.it" in type:
            ireddit_download(new_posts, key)
            pass
        elif 'gfycat.com' in type:
            gfycat_download(new_posts, key)
        elif 'imgur.com' in type:
            imgur_download(new_posts, key)

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
                return title, "/".join(possible_link), id

def gfycat_download(new_posts, key):
    pass #Gfycat is stupid anyway i'll figure out its API later

def imgur_download(new_posts, key):
    pass

def ireddit_download(new_posts, key):
    '''
    downloads image from ireddit.com and stores in pics folder
    Also adds to captions list file so we post with the same caption as the picture

    new_posts: dictionary containing caption, image id, and link
    key: finds the correct picture/caption within the dictionary
    '''

    link = new_posts[key][0]
    name = new_posts[key][1] + '.jpg'
    caption = key
    urllib.request.urlretrieve(link, 'pics/' + name)

    to_upload = open("img_and_caption.txt", "a")
    to_upload.write(caption + ' | ' + name + "\n")
    to_upload.close()



main()
