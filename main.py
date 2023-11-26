import requests
from bs4 import BeautifulSoup

import re
def Find(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]

class discudemy:
    completed = []
    @staticmethod
    def getLinks(url:str):
        return BeautifulSoup(requests.get(url).content,'html.parser').find_all('a')

    @staticmethod
    def firstPagediskUdemy(url:str):
        allLinks = discudemy.getLinks(url)
        if "Take Course" in str(allLinks[12]):
            return discudemy.secondPagediskUdemy(allLinks[12].get('href'))
        else:
            return False

    @staticmethod
    def secondPagediskUdemy(url:str):
        allLinks = discudemy.getLinks(url)
        return allLinks[11].get('href')

    @staticmethod
    def checkAvailable(message:str):
        with open('completed.txt','r') as f:
            discudemy.completed = f.read().split(',')
        if message in discudemy.completed:
            return False
        else:
            return True

    @staticmethod
    def make(message):
        try:
            discLink = Find(message)[0]
            print(discudemy.completed)
            if discudemy.checkAvailable(discLink):
                link = discudemy.firstPagediskUdemy(discLink)
                if link:
                    discudemy.completed.append(discLink)
                    with open('completed.txt','w') as f:
                        f.write(','.join(discudemy.completed))
                    print('After Update',discudemy.completed)
                else:
                    print(discLink,'Expired!')
                return link
            else:
                return False
        except:
            return False

from telethon.sync import TelegramClient, events

from asyncio import run

api_id = '26989318'
api_hash = '062a6050a2c00efbd633b53c434a4f5b'
session_name = 'my-laptop-script'
phone_number = '+918220853158'
async def channel_info():
    client =  TelegramClient(session_name,api_id,api_hash)

    @client.on(events.NewMessage())
    async def handler(event):
        message = event.message
        sender = await message.get_sender()
        forwardId = 1002102875081
        text = message.text
        media = message.media
        if sender.id==1494678304 or sender.id==2102875081:
            text = discudemy.make(text)
            if not text:
                print(text)
                return False
            await client.send_message(forwardId, message=text)
            print(f"Received text message: '{text}' and forwarded as it is.")

    async def list_channels():
        await client.start()
        dialogs = await client.get_dialogs()
        for dialog in dialogs:
            if dialog.is_channel:
                print(f"Channel Name: {dialog.title}, Sender ID: {dialog.id}")
    # await list_channels()

    await client.start(phone=phone_number)
    await client.run_until_disconnected()

run(channel_info())
