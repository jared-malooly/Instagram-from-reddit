###
### By Jared Malooly
### Uses img_and_caption file to get image and caption data and send it to instagram posting script, then clears it.
### Also, more importantly, resizes the images and videos so that instagram can actually post them.
###


import mayabot
import grampost
import time
import glob, os
from PIL import Image
import math
import random
import cv2
import shutil

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
        for image in files:
            img_or_vid = image.split(".")
            if "mp4" in img_or_vid:
                print("Mp4 found in gallery:", image)
            elif "jpg" in img_or_vid:

                try:
                    image = Image.open("pics/" + post_caption[1])
                    w, h = image.size

                    if int(w) > int(h):
                        image = wide_image(image, False)
                        image.save("pics/" + post_caption[1])

                    elif int(w) < int(h):
                        image = tall_image(image, False)
                        image.save("pics/" + post_caption[1])
                    else:
                        pass
                    time.sleep(1)
                except Exception as e:
                    print(e)

    type = post_caption[1].split(".")

    if "jpg" in type:
        try:
            image = Image.open("pics/" + post_caption[1])
            w, h = image.size

            if int(w) > int(h):
                image = wide_image(image, False)
                image.save("pics/" + post_caption[1])


            elif int(w) < int(h):
                image = tall_image(image, False)
                image.save("pics/" + post_caption[1])

            else:
                pass
            time.sleep(1)
        except Exception as e:
            print(e)

    elif "mp4" in type:
        try:
            pass
            # process_video("pics/" + post_caption[1], post_caption[1].rstrip(".mp4")) UNTIL I LEARN HOW TO PROPERLY ENCODE THIS
        except Exception as e:
            print(e)

def process_video(video_directory, folder_name):
    '''
    If the file is a video, run this.

    Strips the frames of the video into a folder, and for each photo, adds square background.

    video_directory: Video location
    folder_name: name of folder to store frames
    '''

    print("Stripping frames from video and adding square background for file: " + folder_name + ".mp4")
    vidcap = cv2.VideoCapture(video_directory)
    success, image = vidcap.read()

    try:
        os.mkdir("pics/" + folder_name)
    except:
        print("Folder already exists dummy")

    frames = []
    count = 0
    while success:
        success, image = vidcap.read()

        cv2.imwrite("frame%d.jpg" % count, image)  # save frame as JPEG file
        os.rename("frame%d.jpg" % count, "pics/" + folder_name + "/" + "frame%d.jpg" % count)

        try:
            image = Image.open("pics/" + folder_name + "/" + "frame%d.jpg" % count)
            w, h = image.size

            frames.append("pics/" + folder_name + "/" + "frame%d.jpg" % count)

            if int(w) > int(h):
                image = wide_image(image, True)
                image.save("pics/" + folder_name + "/" + "frame%d.jpg" % count)

            elif int(w) < int(h):
                image = tall_image(image, True)
                image.save("pics/" + folder_name + "/" + "frame%d.jpg" % count)
        except:
            pass
        count += 1

    make_video(frames, folder_name)


def make_video(frames, file_name):
    '''
    Stitches frames back together and saves to

    frames: list of file locations (locations of frames)
    file_name: Name of new video file
    '''

    print("Converting frames back to mp4 for file: " + file_name + ".mp4\n")

    img = cv2.imread(frames[0])
    height, width, layers = img.shape
    size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*"PIM1")
    out = cv2.VideoWriter("pics/" + file_name + '.avi', fourcc, 30, size)

    for i in frames:
        img = cv2.imread(i)
        out.write(img)

    out.release()
    shutil.rmtree("pics/" + file_name)


def wide_image(image, is_video):
    '''
    If the image is wide, add height until square

    image: Image to be fixed
    is_video: Is the image from a video? Then don't add random color!
    '''

    w, h = image.size

    canvas_width = w
    canvas_height = w
    # Center the image
    x1 = int(math.floor((canvas_width - w) / 2))
    y1 = int(math.floor((canvas_width - h) / 2))

    mode = image.mode
    if len(mode) == 1:  # L, 1
        new_background = (255)
    if len(mode) == 3:  # RGB
        if not is_video:
            new_background = random_pastel(mode)
        else:
            new_background = (117, 201, 204)
    if len(mode) == 4:  # RGBA, CMYK
        if not is_video:
            new_background = random_pastel(mode)
        else:
            new_background = (117, 201, 204, 255)

    newImage = Image.new(mode, (canvas_width, canvas_height), new_background)
    newImage.paste(image, (x1, y1, x1 + w, y1 + h))

    return newImage

def tall_image(image, is_video):
    '''
    If the image is tall, add width until square

    image: Image to be fixed
    is_video: Is the image from a video? Then don't add random color!
    '''

    w, h = image.size

    canvas_width = h
    canvas_height = h
    # Center the image
    x1 = int(math.floor((canvas_width - w) / 2))
    y1 = int(math.floor((canvas_width - h) / 2))

    mode = image.mode
    if len(mode) == 1:  # L, 1
        new_background = (255)
    if len(mode) == 3:  # RGB
        if not is_video:
            new_background = random_pastel(mode)
        else:
            new_background = (117, 201, 204)
    if len(mode) == 4:  # RGBA, CMYK
        if not is_video:
            new_background = random_pastel(mode)
        else:
            new_background = (117, 201, 204, 255)

    newImage = Image.new(mode, (canvas_width, canvas_height), new_background)
    newImage.paste(image, (x1, y1, x1 + w, y1 + h))

    return newImage

def random_pastel(mode):
    '''
    Return a random pastel color

    mode: Image mode (1, 3, 4)
    '''
    availible_pastels = [(242, 187, 172), (251, 219, 206), (175, 223, 219), (117, 201, 204)]
    if len(mode) == 3:
        return availible_pastels[random.randint(0, len(availible_pastels) - 1)]
    if len(mode) == 4:
        return availible_pastels[random.randint(0, len(availible_pastels) - 1)]

amount = 1
while True:
    mayabot.run(amount)
    amount += 1
    directory = open("img_and_caption.txt", "r+")
    test_for_new = []
    for line in directory:
        post_caption = line.rstrip().split(" | ")
        process_image(post_caption)
        test_for_new.append(post_caption)


    if len(test_for_new) > 0:
        grampost.run()

    print("Made post!")
    # Clear img_and_caption for next set of instructions
    directory.truncate(0)
    print('Cleared instruction sheet.')
    directory.close()
    time.sleep(60)
