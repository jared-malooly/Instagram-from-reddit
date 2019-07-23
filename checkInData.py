###
### By Jared Malooly
### Uses img_and_caption file to get image and caption data and send it to instagram posting script, then clears it.
### Also, more importantly, resizes the images so that instagram can actually post them.
###


import mayabot
#import grampost
import time
import glob, os
from PIL import Image

def process_image(post_caption):
    '''
    Makes the image "Instagram Friendly," by making it a square

    post_caption: Instructions containing post info and image file name
    '''

    # Finds filenames inside a Gallery folder
    if len(post_caption) == 3:
        files = []
        directory = 'pics/' + post_caption[1]
        for f in os.listdir(directory):
            files.append(f)
        if len(files) > 10:
            print("u dummy I cant post this")
            files = []

    try:
        image = Image.open("pics/" + post_caption[1])
        image.show()
    except:
        "Couldn't find the image"
amount = 0
while True:
    mayabot.run(amount)
    amount += 1
    directory = open("img_and_caption.txt", "r+")
    for line in directory:
        post_caption = line.rstrip().split(" | ")
        process_image(post_caption)

    # Clear img_and_caption for next set of instructions
    directory.truncate(0)
    print('Cleared instruction sheet.')
    directory.close()
    #grampost.run()
    time.sleep(100)
