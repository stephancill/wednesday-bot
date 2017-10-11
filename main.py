import datetime
import os
import sys
import time
import telepot
from telepot.loop import MessageLoop

groups = set()
sent = False

try:
    with open("groups.txt", "r") as f:
        for line in f:
            groups.add(int(line[:-1]))
        print(list(groups))
except FileNotFoundError:
    print("No groups.txt yet")

def writeGroups():
    with open("groups.txt", "w") as f:
        for group in groups:
            f.write(str(group) + "\n")
def registerNewGroup(id):
    groups.add(id)
    writeGroups()

def removeGroup(id):
    try:
        groups.remove(id)
        writeGroups()
    except Exception as e:
        print(id, e)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == "new_chat_member":
        registerNewGroup(chat_id)
    elif content_type == "left_chat_member":
        removeGroup(chat_id)
    

TOKEN = None
try:
    TOKEN = os.environ["BOT_TOKEN"] #Hosting the bot on Heroku
except KeyError:
    TOKEN = sys.argv[1] 

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ("Listening ...")

# Keep the program running.
while 1:
    now = datetime.datetime.utcnow()
    if now.weekday() == 2 and now.hour == 5:
        if not sent:
            remove = []
            for group in groups:
                try:
                    bot.sendPhoto(group, "http://i0.kym-cdn.com/entries/icons/original/000/020/016/wednesday.jpg")
                except telepot.exception.TelegramError:
                    remove.append(group)
            [removeGroup(r) for r in remove]

            sent = True
    else:
        sent = False

    time.sleep(59)
   
