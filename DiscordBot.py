from supabase_py import create_client, Client
from os import linesep
import discord
import requests
import pandas as pd
from pandas import DataFrame, read_csv
import sys

TOKEN = sys.argv[1]

client = discord.Client()

# requires beta supabase
supabase: Client = create_client(sys.argv[2], sys.argv[3])

# Pushes file to supabase with bytestream
def push_file(path, file, headers):
    storageObject = supabase.storage().StorageFileAPI(id_= "timetables")
    requests.post(
                f"{storageObject.url}/object/{path}", data=file, headers=dict(storageObject.headers, **headers)
            )

#Bot loggin confirmation
@client.event
async def on_ready():
    print(f"Logged in as {format(client)}")

#Testing for splitting user messages
#With file pushing
@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username} said: {user_message} from: #{channel}")
    if (message.attachments):
        for attachment in message.attachments:
            if True:#attachment.content_type=="text/plain; charset=utf-8":
                push_file("timetables/"+message.author.id+"/"+attachment.filename, requests.get(attachment.url, allow_redirects=True).content, {"Content-Type": attachment.content_type})

#reading xls timetable and storing data
def xls_read(file):
    with open("usyd_units.txt") as unit_file:
        Lines = unit_file.readlines()
    dataframe = pd.read_excel(file)
    unit = (dataframe["subject Code"]).split("-")[0]
    isvalidunit = False
    for units in Lines:
        if unit == units:
            isvalidunit = True
        else:
            print("Invalid unit code identified, nice try bucko")
    unit_description = dataframe["Description"]
    event_type = dataframe["Group"]
    activity = dataframe["Activity"]
    day = dataframe["Day"]
    time = dataframe["Time"]
    campus = dataframe["Campus"]
    duration = dataframe["Duration"]
    dates = dataframe["Dates"]
    if dataframe["Location"] == "-":
        return
    building = (dataframe["Location"]).split(".")[3] + " " + (dataframe["Location"]).split(".")[4] 
    


def check_valid_channel(guild, channel_name):
    for t_channel in guild.text_channels:
        if channel_name == t_channel.name:
            return t_channel


def find_or_create_channel(guild, channel_name):
    channel = check_valid_channel(guild, channel_name)
    if not channel:
        channel = channel_name


    

#Previous attempt at channel joining

# @client.event
# async def on_message(message):
#     if message.content == 'test':
#         #await channel.set_permissions(member, overwrite=None)
#         await find_channel(message.guild, "randy").set_permissions(message.author, read_messages=True, send_messages=False)


    
#     async def on_message(message):
#         guild = ctx.message.guild
#         await guild.create_text_channel('cool-channel')



client.run(TOKEN)
