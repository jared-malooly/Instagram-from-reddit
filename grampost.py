from instapy_cli import client
import time


username = 'fluft_boys'
password = 'WhySoRude'


def main():

    posts = []
    instructions = open("img_and_caption.txt", "r")

    for instruction in instructions:
        instr = instruction.rstrip("\n")
        posts.append(instr.split(" | "))


    for instruction in posts:
        text = instruction[0]
        image = 'pics/' + instruction[1]
        try:
            with client(username, password) as cli:
                cli.upload(image, text)
        except Exception as e:
            print("Image type not supported yet :(")
            print(e)
        time.sleep(30)

def run():

    main()
