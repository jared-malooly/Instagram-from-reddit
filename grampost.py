import InstagramAPI as ig
import time
import cv2

def main():

    username = ''
    password = ''
    InstagramAPI = ig.InstagramAPI(username, password)
    instructions = open("img_and_caption.txt", 'r')

    for instruction in instructions:
        InstagramAPI.login()  # login
        instruction = instruction.rstrip('\n')
        stuff = instruction.split(" | ")
        file = stuff[1]
        caption = stuff[0]

        buzzwords = ["wholesome"]
        words = caption.split(" ")
        for word in words:
            if word.lower() in buzzwords:
                words[words.index(word)] = "#" + word
        caption = " ".join(words)


        type = file.split(".")

        print(file)

        try:
            if "mp4" in type:
                print('Attempting to post mp4...')
                video_path = 'pics/' + file
                print(video_path)
                thumbnail = get_thumbnail('pics/' + file, type[0])
                InstagramAPI.uploadVideo(video_path, thumbnail, caption)
                print("Made post!")

            elif "jpg" in type:
                print('Attempting to post jpg...')
                photo_path = 'pics/' + file
                print(photo_path)
                InstagramAPI.uploadPhoto(photo_path, caption)
                print("Made post!")

        except:
            print("Something went wrong with posting the image")

        InstagramAPI.logout()
        time.sleep(30)

def get_thumbnail(directory, file):
    vidcap = cv2.VideoCapture(directory)
    success, image = vidcap.read()
    cv2.imwrite("pics/" + file + ".jpg", image)
    return "pics/" + file + ".jpg"

def run():
    main()
