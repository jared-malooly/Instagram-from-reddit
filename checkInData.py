import mayabot
import grampost
import time

#Gets new posts, if any, and posts to instagram every 24 hours (86400s)
while True:
    mayabot.run(True)
    grampost.run(True)
    time.sleep(86400)
