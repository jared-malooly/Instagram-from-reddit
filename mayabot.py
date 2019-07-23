### For Maya, thanks for the project

import praw
from bs4 import BeautifulSoup
import requests
import time
import urllib.request
import os

def main():
    username = 'mayaxs'
    r = praw.Reddit(client_id = '1scCXWF6gu7Ecg',
                    client_secret = 'BcRWHiN-UXTagFSlvjgm6m_zQMg',
                    username = 'Mayabot',
                    password = 'CoolPasswordDude',
                    user_agent='mayabotV1')

    user = r.redditor(username)
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
    for submission in user.submissions.new(limit=5):

        #time.sleep(5) #For use in final in case the rpi requests too often

        sub = str(submission.subreddit)
        #SHOULD ignore account posts and posts that are already in the used_ids text file
        if submission not in used_ids and sub != "u_" + user.name:
            try:
                post_ids.append(submission.id)
                used_ids_txt.write(submission.id + '\n')
                title, link_to_image, id, imgur_type = get_image(submission.id, submission.title) #Fuck me heres the issue
                #SHOULD key out duplicate posts!
                new_posts[title] = [link_to_image, id, imgur_type]
            except Exception as e:
                print(e, submission.id)
                print('The post may be deleted or an invalid (text based) post')

    if post_ids == []:
        print('All posts accounted for!')
    else:
        print('\n\nNew Post!\n\n')
    #Decides which API to use to download image/gif
    for key in new_posts:
        type = []
        type = new_posts[key][0].split("/")
        if "i.redd.it" in type:
            ireddit_download(new_posts, key)
            pass
        elif 'giant.gfycat.com' in type:
            gfycat_download(new_posts, key)
        elif 'external-preview.redd.it' in type:
            imgur_download(new_posts, key)
        elif 'DASH_480?source=fallback.mp4' in type:
            vreddit_download(new_posts, key)
        elif 'imgur.com' in type:
            if 'gallery' in type:
                extract_gallery(new_posts, key)
            else:
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
            if i == "gfycat.com" or i == "external-preview.redd.it" or i == "imgur.com" or i == "i.redd.it" or i == "gallery":
                if i == 'imgur.com':
                    #Three types of imgur links:
                    #    jpg
                    #    video
                    #    gallery
                    imgur_type = analyze_imgur("/".join(possible_link))

                    return title, "/".join(possible_link), id, imgur_type
                if i == "gfycat.com":

                    #need to get mp4 link

                    return title, get_gyfy_link("/".join(possible_link)), id, 'n/a'

                else:
                    return title, "/".join(possible_link), id, "n/a"

    for link in soup.find_all("video"):
        split_div = str(link)
        split_div = split_div.split(' ')
        for i in split_div:
            find_src = i.split('=')
            if 'src' in find_src:
                link = find_src[1].strip('"')
                link = link.strip('HLSPlaylist.m3u8')
                link = link + 'DASH_480?source=fallback.mp4'
                return title, link, id

def get_gyfy_link(url):
    '''
    Finds the source file for a gfycat link, and returns the source

    url: the original "site" url where the source is hosted
    '''

    web_request = requests.get(url, headers={'User-agent': 'mayabotV1'})
    data = web_request.text
    soup = BeautifulSoup(data, "html.parser")
    for div in soup.find_all("div", class_ = "video-container media-container noselect"):
        split_div = str(div)
        split_div = split_div.split('"')
        for item in split_div:
            possible_link = item.split('.')
            if "mp4" in possible_link:
                return item


def analyze_imgur(url):
    '''
    Decides whether the image on imgur should be treated like a video or an image.

    url: the original "site" url where the source is hosted
    '''

    web_request = requests.get(url, headers={'User-agent': 'mayabotV1'})
    data = web_request.text
    soup = BeautifulSoup(data, "html.parser")
    for link in soup.find_all("div", class_ = "post-image-container"):
        split_div = str(link)
        split_div = split_div.split(' ')
        if 'itemtype="http://schema.org/VideoObject">\n<div' in split_div:
            return 'video'
        elif 'itemtype="http://schema.org/ImageObject">\n<div' in split_div:
            return 'jpg'


def extract_gallery(new_posts, key):
    '''
    Creates a folder to extract all images from an imgur gallery to. Also updates img_and_caption.txt

    new_posts: dictionary containing caption, image id, and link
    key: finds the correct picture/caption within the dictionary
    '''

    url = new_posts[key][0]

    imgur_type = new_posts[key][2]
    web_request = requests.get(url, headers={'User-agent': 'mayabotV1'})
    data = web_request.text
    soup = BeautifulSoup(data, "html.parser")
    folder_name = new_posts[key][1]

    # create directory for extraction
    try:
        os.mkdir('pics/' + folder_name)
    except:
        print("Folder already exists dummy")

    for link in soup.find_all("div", class_="post-image-container"):
        try:
            possible_link = (link['id'])
            id = possible_link
            link = 'https://imgur.com/' + id

            if imgur_type == "video":
                link = link + ".mp4"
                name = id + '.mp4'
            else:
                name = id + '.jpg'
                link = link + '.jpg'

            urllib.request.urlretrieve(link, 'pics/' + folder_name + '/' + name)
        except Exception as e:
            print(e)

    to_upload = open("img_and_caption.txt", "a")
    to_upload.write(key + ' | ' + folder_name + ' | ' + "GALLERY" + "\n")
    to_upload.close()



def gfycat_download(new_posts, key):
    '''
    downloads video from gfycat and stores in pics folder
    Also adds to captions list file so we post with the same caption as the picture

    new_posts: dictionary containing caption, image id, and link
    key: finds the correct picture/caption within the dictionary
    '''
    link = new_posts[key][0]
    name = new_posts[key][1] + '.mp4'
    caption = key
    urllib.request.urlretrieve(link, 'pics/' + name)

    to_upload = open("img_and_caption.txt", "a")
    to_upload.write(caption + ' | ' + name + "\n")
    to_upload.close()

def imgur_download(new_posts, key):
    '''
    downloads file from imgur and stores in pics folder
    Also adds to captions list file so we post with the same caption as the picture

    new_posts: dictionary containing caption, image id, and link
    key: finds the correct picture/caption within the dictionary
    '''

    link = new_posts[key][0]
    imgur_type = new_posts[key][2]
    if imgur_type == "jpg":
        name = new_posts[key][1] + '.jpg'
        link = link + '.jpg'
    else:
        name = new_posts[key][1] + '.mp4'
        link = link+ ".mp4"
    caption = key
    urllib.request.urlretrieve(link, 'pics/' + name)

    to_upload = open("img_and_caption.txt", "a")
    to_upload.write(caption + ' | ' + name + "\n")
    to_upload.close()


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

def vreddit_download(new_posts, key):
    '''
    downloads file from v.redd.it and stores in pics folder
    Also adds to captions list file so we post with the same caption as the picture

    new_posts: dictionary containing caption, image id, and link
    key: finds the correct picture/caption within the dictionary
    '''

    link = new_posts[key][0]
    name = new_posts[key][1] + '.mp4'
    caption = key
    urllib.request.urlretrieve(link, 'pics/' + name)

    to_upload = open("img_and_caption.txt", "a")
    to_upload.write(caption + ' | ' + name + "\n")
    to_upload.close()


def run(run_me):
    '''
    Gives the ability to run from another program with import. Needed for automation
    '''
    if run_me:
        main()

#debugging
run(True)
