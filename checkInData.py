###
### By Jared Malooly
### Uses img_and_caption file to get image and caption data and send it to instagram posting script, then clears it.
### Also, more importantly, resizes the images so that instagram can actually post them.
###

import mayabot
#import grampost
import time

def process_image(post_caption):
    '''
    Makes the image "Instagram Friendly," by making it a square

    post_caption: Instructions containing post info and image file name
    '''




while True:
    mayabot.run()
    directory = open("img_and_caption.txt", "r+")
    for line in directory:
        post_caption = line.rstrip().split(" | ")
        process_image(post_caption)

    # Clear img_and_caption for next set of instructions
    directory.truncate(0)
    print('Cleared instruction sheet.')
    directory.close()
    #grampost.run(True)
    time.sleep(100)
