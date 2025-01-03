from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaDocument, Message 
from PIL import Image
from datetime import datetime
from .mrsyd import process_queue
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


@Client.on_message(filters.command("begin") & filters.user(1733124290))  # Replace YOUR_USER_ID with your user ID
async def start_processing(client, message):
    global allowed_chats
    try:
        # Extract chat_id from the command
        if len(message.command) != 2:
            await message.reply_text("Usage: /begin <chat_id>")
            return
        
        chat_id = int(message.command[1])
        await message.reply_text(f"Processing started for existing messages in chat ID: {chat_id}")
        
        # Process existing messages in the chat
        await process_existing_messages(client, chat_id)
    except ValueError:
        await message.reply_text("Invalid chat ID. Please provide a valid integer.")

async def process_existing_messages(client, chat_id):
    global mrsydt_g, processing
    try:
        async for message in client.iter_history(chat_id):
            if message.media:
                file = getattr(message, message.media.value)
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
                    mrsydt_g.append(sydfile)
        
        # Start processing the queue if not already processing
        if not processing:
            processing = True
            await process_queue(client)
    except Exception as e:
        logger.error(f"An error occurred while fetching messages: {e}")
