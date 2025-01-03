from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaDocument, Message 
from PIL import Image
from datetime import datetime
#from .mrsyd import process_queue
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.ffmpeg import syd as syyyyyyyyydddddd
from helper.utils import progress_for_pyrogram, humanbytes, convert, download_image
from helper.database import madflixbotz
from config import Config
import os
import time, asyncio
import logging
import re
#import shutil
fulsyd = "fair"
db = madflixbotz
mrsydt_g = []
processing = False
MRSYD = -1002289521919
sydtg = -1002305372915
Syd_T_G = -1002160523059
renaming_operations = {}
logger = logging.getLogger(__name__)
last_season_number = 0
syd_top = 0
syd_qua = "None"
syd_mov = "None"


  # Flag to avoid multiple simultaneous processing

@Client.on_message(filters.command("begin") & filters.user(1733124290))  # Replace with your user ID
async def start_processing(client, message):
    try:
        # Validate and extract chat_id from the command
        if len(message.command) != 2:
            await message.reply_text("Usage: /begin <chat_id>")
            return

        chat_id = message.command[1]
        try:
            chat_id = int(chat_id)
        except ValueError:
            await message.reply_text("Invalid chat ID. Please provide a valid integer.")
            return

        await message.reply_text(f"Processing started for existing messages in chat ID: {chat_id}")

        # Collect message IDs
        message_ids = []
        async for msg in client.get_chat_history(chat_id, reverse=True):  # Fetch in chronological order
            message_ids.append(msg.id)

        print(f"Collected {len(message_ids)} message IDs for chat ID: {chat_id}")

        # Process each message ID one by one
        for message_id in message_ids:
            await process_existing_messages(client, chat_id, message_id)

        print("All messages processed.")
    except Exception as e:
        logger.error(f"An error occurred in start_processing: {e}")
        await message.reply_text("An error occurred while starting the processing.")

async def process_existing_messages(client, chat_id, message_id):
    global mrsydt_g
    try:
        # Fetch the message by ID
        message = await client.get_messages(chat_id=chat_id, message_ids=message_id)
        
        if message.media:
            file = getattr(message, message.media.value, None)
            if file and file.file_size > 10 * 1024 * 1024:  # > 10 MB
                sydmen = await db.get_sydson(1733124290)
                syd = file.file_name
                await asyncio.sleep(1)
                mrsyd = await db.get_topic(1733124290)
                mrsydt = await db.get_rep(1733124290)
                syd1 = mrsydt['sydd']
                syd2 = mrsydt['syddd']

                sydfile = {
                    'file_name': syd,
                    'file_size': file.file_size,
                    'message_id': message.id,
                    'media': file,
                    'topic': mrsyd,
                    'season': sydmen,
                    'repm': syd1,
                    'repw': syd2,
                    'message': message
                }
                mrsydt_g.append(sydfile)  # Add to the queue in order
                print(f"Added file {file.file_name} to the queue.")
    except Exception as e:
        logger.error(f"An error occurred while processing message {message_id}: {e}")

async def process_queue(client):
    global mrsydt_g, processing
    try:
        while mrsydt_g:
            sydfile = mrsydt_g.pop(0)  # Process the first file in the queue
            # Add your processing logic here
            print(f"Processing file: {sydfile['file_name']} of size {sydfile['file_size']} bytes")
            await asyncio.sleep(1)  # Simulate processing delay
        print("All messages processed from the queue.")
    except Exception as e:
        logger.error(f"An error occurred while processing the queue: {e}")
    finally:
        processing = False  # Reset the processing flag
