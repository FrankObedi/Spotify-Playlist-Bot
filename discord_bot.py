import discord
import os
from time import sleep
import sqlite3

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

# create sqlite db
connection = sqlite3.connect(r"C:\Users\frank\Desktop\Programming\Playlist Bot\song_db.db")
# get cursor to execute sql statements
cursor = connection.cursor()


@client.event
# even for when bot is ready
async def on_ready():
    print("{0.user} is ready".format(client))


def add_song_db(song):
    status = ""
    # Check if song already in db
    cursor.execute("SELECT 1 FROM Song WHERE Name = ?", (song,))
    db_result = cursor.fetchone()
    if(db_result is None):
        cursor.execute("INSERT INTO Song (Name) VALUES (?)", (song,))
        status = f'"{song}" added to playlist'
        connection.commit()
    else:
        status = f'"{song}" already added to playlist'
    return status
    


# bot to act when message is sent to "add-song" channel
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if message.channel.name == "add-song":
        if msg.startswith("$add"):
            # print("{0} typed: {1}".format(message.author, message.content))
            song = msg.split("$add ", 1)[1]
            status = add_song_db(song)            
            await message.channel.send(status)

client.run(os.getenv("DISCORD_TOKEN"))
