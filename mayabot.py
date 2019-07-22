import praw
import bs4
import requests

print('praw version: {}'.format(praw.__version__))
print('bs4 version: {}'.format(bs4.__version__))

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
    used_ids_txt = open('used_ids.txt', 'r')
    #read text file to list of used ids so the program doesnt repeat posts
    for line in used_ids_txt:
        used_ids.append(line.rstrip())
    used_ids_txt.close()
    used_ids_txt = open('used_ids.txt', 'a')
    for submission in user.submissions.new(limit = 1000):
        sub = str(submission.subreddit)
        #SHOULD ignore account posts and posts that are already in the used_ids text file
        if submission not in used_ids and sub != "u_mayaxs":
            post_ids.append(submission.id)
            used_ids_txt.write(submission.id + '\n')
            get_image(submission.id, submission.subreddit)
    if post_ids == []:
        print('All posts accounted for!')
    used_ids_txt.close()

def get_image(id, sub):
    sub = str(sub)
    url = "https://www.reddit.com/r/" + sub + "/" + id + "/"
    print(url)


main()