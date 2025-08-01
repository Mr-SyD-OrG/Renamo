from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InputMediaDocument, Message, InlineKeyboardButton, InlineKeyboardMarkup
from PIL import Image
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, humanbytes, convert
from helper.database import madflixbotz
from config import Config
import os
import time
import asyncio
import re

db = madflixbotz
renaming_operations = {}
user_queues = {}

# Pattern 1: S01E02 or S01EP02
pattern1 = re.compile(r'S(\d+)(?:E|EP)(\d+)')
# Pattern 2: S01 E02 or S01 EP02 or S01 - E01 or S01 - EP02
pattern2 = re.compile(r'S(\d+)\s*(?:E|EP|-\s*EP)(\d+)')
# Pattern 3: Episode Number After "E" or "EP"
pattern3 = re.compile(r'(?:[([<{]?\s*(?:E|EP)\s*(\d+)\s*[)\]>}]?)')
# Pattern 3_2: episode number after - [hyphen]
pattern3_2 = re.compile(r'(?:\s*-\s*(\d+)\s*)')
# Pattern 4: S2 09 ex.
pattern4 = re.compile(r'S(\d+)[^\d]*(\d+)', re.IGNORECASE)
# Pattern X: Standalone Episode Number
patternX = re.compile(r'(\d+)')

season_pattern1 = re.compile(r'(?:S|Season)\s*[-:]?\s*(\d+)', re.IGNORECASE)
# Pattern 2: Flexible detection with explicit prefixes only
season_pattern2 = re.compile(r'(?:^|[^\w])(?:S|Season)\s*[-:]?\s*(\d+)(?=[^\d]|$)', re.IGNORECASE)

#QUALITY PATTERNS 
# Pattern 5: 3-4 digits before 'p' as quality
pattern5 = re.compile(r'\b(?:.*?(\d{3,4}[^\dp]*p).*?|.*?(\d{3,4}p))\b', re.IGNORECASE)
# Pattern 6: Find 4k in brackets or parentheses
pattern6 = re.compile(r'[([<{]?\s*4k\s*[)\]>}]?', re.IGNORECASE)
# Pattern 7: Find 2k in brackets or parentheses
pattern7 = re.compile(r'[([<{]?\s*2k\s*[)\]>}]?', re.IGNORECASE)
# Pattern 8: Find HdRip without spaces
pattern8 = re.compile(r'[([<{]?\s*HdRip\s*[)\]>}]?|\bHdRip\b', re.IGNORECASE)
# Pattern 9: Find 4kX264 in brackets or parentheses
pattern9 = re.compile(r'[([<{]?\s*4kX264\s*[)\]>}]?', re.IGNORECASE)
# Pattern 10: Find 4kx265 in brackets or parentheses
pattern10 = re.compile(r'[([<{]?\s*4kx265\s*[)\]>}]?', re.IGNORECASE)

def extract_quality(filename):
    # Try Quality Patterns
    match5 = re.search(pattern5, filename)
    if match5:
        print("Matched Pattern 5")
        quality5 = match5.group(1) or match5.group(2)  # Extracted quality from both patterns
        print(f"Quality: {quality5}")
        return quality5

    match6 = re.search(pattern6, filename)
    if match6:
        print("Matched Pattern 6")
        quality6 = "4k"
        print(f"Quality: {quality6}")
        return quality6

    match7 = re.search(pattern7, filename)
    if match7:
        print("Matched Pattern 7")
        quality7 = "2k"
        print(f"Quality: {quality7}")
        return quality7

    match8 = re.search(pattern8, filename)
    if match8:
        print("Matched Pattern 8")
        quality8 = "HdRip"
        print(f"Quality: {quality8}")
        return quality8

    match9 = re.search(pattern9, filename)
    if match9:
        print("Matched Pattern 9")
        quality9 = "4kX264"
        print(f"Quality: {quality9}")
        return quality9

    match10 = re.search(pattern10, filename)
    if match10:
        print("Matched Pattern 10")
        quality10 = "4kx265"
        print(f"Quality: {quality10}")
        return quality10    

    # Return "Unknown" if no pattern matches
    unknown_quality = "Unknown"
    print(f"Quality: {unknown_quality}")
    return unknown_quality
    

def extract_episode_number(filename):    
    # Try Pattern 1
    match = re.search(pattern1, filename)
    if match:
        print("Matched Pattern 1")
        return match.group(2)  # Extracted episode number
    
    # Try Pattern 2
    match = re.search(pattern2, filename)
    if match:
        print("Matched Pattern 2")
        return match.group(2)  # Extracted episode number

    # Try Pattern 3
    match = re.search(pattern3, filename)
    if match:
        print("Matched Pattern 3")
        return match.group(1)  # Extracted episode number

    # Try Pattern 3_2
    match = re.search(pattern3_2, filename)
    if match:
        print("Matched Pattern 3_2")
        return match.group(1)  # Extracted episode number
        
    # Try Pattern 4
    match = re.search(pattern4, filename)
    if match:
        print("Matched Pattern 4")
        return match.group(2)  # Extracted episode number

    # Try Pattern X
    match = re.search(patternX, filename)
    if match:
        print("Matched Pattern X")
        return match.group(1)  # Extracted episode number
        
    # Return None if no pattern matches
    return None

def extract_season_number(filename):    
    # Try Pattern 1
    match = re.search(season_pattern1, filename)
    if match:
        print("Matched Pattern 1")
        return match.group(1)  # Extracted episode number
    
    # Try Pattern 2
    match = re.search(season_pattern2, filename)
    if match:
        print("Matched Pattern 2")
        return match.group(1)  # Extracted episode number
    return None

# Example Usage:
filename = "Naruto Shippuden S01 - EP07 - 1080p [Dual Audio] @Madflix_Bots.mkv"
episode_number = extract_episode_number(filename)
print(f"Extracted Episode Number: {episode_number}")

# Inside the handler for file uploads
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def auto_rename_files(client, message):
  #  await message.reply_text("Yo")
    user_id = message.from_user.id
    if Config.FORCE_SUB:
        buttons = [[InlineKeyboardButton(text="⊛ ᴊᴏɪɴ ᴜᴩᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ⊛", url=f"https://t.me/{Config.FORCE_SUB}") ]]
        text = "<b>Hᴇʟʟᴏ ✨, \n\nYᴏᴜ Hᴀᴠᴇ Tᴏ Jᴏɪɴ Oᴜʀ Uᴩᴀᴅᴇᴛ Cʜᴀɴɴᴇʟ Tᴏ Uꜱᴇ Mᴇ 🌡️\nSᴏ Pʟᴇᴀꜱᴇ Jᴏɪɴ Iɴ Tʜᴇ Cʜᴀɴɴᴇʟ Tᴏ Cᴏɴᴛɪɴᴜᴇ...</b>"
        try:
            user = await client.get_chat_member(Config.FORCE_SUB, message.from_user.id)    
            if user.status == enums.ChatMemberStatus.BANNED:                                   
                return await client.send_message(message.from_user.id, text="Sorry You Are Banned To Use Me")  
        except UserNotParticipant:                       
            return await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
        except Exception as e:
            try:
                await client.send_message(1733124290, f"FsUb : {e}")
            except:
                pass
   # await message.reply_text("Yo")
    if user_id not in user_queues:
        user_queues[user_id] = asyncio.Queue()
        asyncio.create_task(process_user_queue(client, user_id, message))
  #  await message.reply_text("Yo")
    await user_queues[user_id].put(message)
    syd = await message.reply_text("Your file has been queued for renaming. Please wait...")
    await asyncio.sleep(100)
    await syd.delete()
    
    
async def process_user_queue(client, user_id, message):
    queue = user_queues[user_id]
    active_tasks = set()
    while True:
        try:
            if not queue.empty() and len(active_tasks) < 2:
                msg = await queue.get()
                task = asyncio.create_task(auto_rname_files(client, msg))
                active_tasks.add(task)
                task.add_done_callback(lambda t: active_tasks.discard(t))
                await asyncio.sleep(10)  # small delay to avoid spam
            else:
                await asyncio.sleep(20)

            if queue.empty() and len(active_tasks) == 0:
                del user_queues[user_id]
                break

        except Exception as e:
            try:
                await client.send_message(
                    user_id,
                    f"❌ Error in queue processor:\n<code>{e}</code>"
                    
                )
            except:
                pass
            break

    

    syd = await message.reply_text("Pʀᴏᴄᴇꜱꜱ ᴇɴᴅᴇᴅ...!")
    await asyncio.sleep(3000)
    await syd.delete()
async def auto_rname_files(client, message):
    user_id = message.from_user.id
    firstname = message.from_user.first_name
    format_template = await madflixbotz.get_format_template(user_id)
    media_preference = await madflixbotz.get_media_preference(user_id)

    if not format_template:
        return await message.reply_text("Please Set An Auto Rename Format First Using /set_format")

    # Extract information from the incoming file name
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
        media_type = media_preference or "document"  # Use preferred media type or default to document
    elif message.video:
        file_id = message.video.file_id
        file_name = f"{message.video.file_name}.mp4"
        media_type = media_preference or "video"  # Use preferred media type or default to video
    elif message.audio:
        file_id = message.audio.file_id
        file_name = f"{message.audio.file_name}.mp3"
        media_type = media_preference or "audio"  # Use preferred media type or default to audio
    else:
        return await message.reply_text("Unsupported File Type")

    
    

# Check whether the file is already being renamed or has been renamed recently
    if file_id in renaming_operations:
        elapsed_time = (datetime.now() - renaming_operations[file_id]).seconds
        if elapsed_time < 10:
            print("File is being ignored as it is currently being renamed or was renamed recently.")
            return  # Exit the handler if the file is being ignored
    
    # Mark the file as currently being renamed
    renaming_operations[file_id] = datetime.now()
    # Extract episode number and qualities
    episode_number = extract_episode_number(file_name)
    season_number = extract_season_number(file_name) if extract_season_number(file_name) else '01'
    
    
    if episode_number or season_number:
        # Replace episode placeholders
        if episode_number:
            placeholders = ["{episode}", "Episode", "EPISODE", "episode"]
            for placeholder in placeholders:
                format_template = format_template.replace(placeholder, f"{int(episode_number):02d}", 1)

        # Replace season placeholders
        if season_number:
            season_placeholders = ["{season}"]
            for season_placeholder in season_placeholders:
                format_template = format_template.replace(season_placeholder, f"{int(season_number):02d}", 1)

        # Add extracted qualities to the format template
        quality_placeholders = ["{quality}"]
        for quality_placeholder in quality_placeholders:
            if quality_placeholder in format_template:
                extracted_qualities = extract_quality(file_name)
                if extracted_qualities == "Unknown":
                    await message.reply_text("I Was Not Able To Extract The Quality Properly. Renaming As 'Unknown'...")
                    # Mark the file as ignored
                    del renaming_operations[file_id]
                    return  # Exit the handler if quality extraction fails
                
                format_template = format_template.replace(quality_placeholder, "".join(extracted_qualities))           
        
        _, file_extension = os.path.splitext(file_name)
        prefix = await db.get_prefix(user_id)
        suffix = await db.get_suffix(user_id)
        new_file_name = (f"{prefix + ' ' if prefix else ''}{format_template}{' ' + suffix if suffix else ''}{file_extension}")
        file_path = f"downloads/{new_file_name}"
        file = message
        download_msg = await message.reply_text(text="Trying To Download.....")
        try:
            path = await client.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("Download Started....", download_msg, time.time()))
        except Exception as e:
            # Mark the file as ignored
            del renaming_operations[file_id]
            return await download_msg.edit(e)     

        duration = 0
        try:
            metadata = extractMetadata(createParser(file_path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
        except Exception as e:
            print(f"Error getting duration: {e}")

        upload_msg = await download_msg.edit("Trying To Uploading.....")
        ph_path = None
        c_caption = await madflixbotz.get_caption(message.chat.id)
        c_thumb = await madflixbotz.get_thumbnail(message.chat.id)

        caption = c_caption.format(filename=new_file_name, filesize=humanbytes(message.document.file_size), duration=convert(duration)) if c_caption else f"**{new_file_name}**"

        if c_thumb:
            ph_path = await client.download_media(c_thumb)
            print(f"Thumbnail downloaded successfully. Path: {ph_path}")
        elif media_type == "video" and message.video.thumbs:
            ph_path = await client.download_media(message.video.thumbs[0].file_id)

        if ph_path:
            Image.open(ph_path).convert("RGB").save(ph_path)
            img = Image.open(ph_path)
            img.resize((320, 320))
            img.save(ph_path, "JPEG")    
        

        try:
            mrsyd = await db.get_dump(user_id)
            type = media_type  # Use 'media_type' variable instead
            if type == "document":
                sydfil = await client.send_document(
                    mrsyd,
                    document=file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started.....", upload_msg, time.time())
                )
            elif type == "video":
                sydfil = await client.send_video(
                    mrsyd,
                    video=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started.....", upload_msg, time.time())
                )
            elif type == "audio":
                sydfil = await client.send_audio(
                    mrsyd,
                    audio=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started.....", upload_msg, time.time())
                )
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            # Mark the file as ignored
            return await upload_msg.edit(f"Error: {e}")

        mrsyyd = sydfil.document.file_size if type == "document" else sydfil.video.file_size if type == "video" else sydfil.audio.file_size
        mrssyd = message.document.file_size if type == "document" else message.video.file_size if type == "video" else message.audio.file_size
        if mrsyyd != mrssyd:
            await sydfil.delete()
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            del renaming_operations[file_id]
            return await message.reply_text("Sɪᴢᴇ Eʀʀᴏʀ: Pʟᴇᴀꜱᴇ Rᴇɴᴀᴍᴇ Aɢᴀɪɴ...!")
        await download_msg.delete() 
        if user_id != 1733124290:
            await asyncio.sleep(8)
        await message.delete()
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)

# Remove the entry from renaming_operations after successful renaming
        del renaming_operations[file_id]
    else:
        await message.reply_text("Nᴏ ᴇᴩɪꜱᴏᴅᴇ ᴀɴᴅ ꜱᴇᴀꜱᴏɴ ɴᴏ. ᴄᴏᴍᴛɪɴᴜɪɴɢ ᴛʜᴇ ᴩʀᴏᴄᴄᴇꜱꜱ...!")
        quality_placeholders = ["{quality}"]
        for quality_placeholder in quality_placeholders:
            if quality_placeholder in format_template:
                extracted_qualities = extract_quality(file_name)
                if extracted_qualities == "Unknown":
                    await message.reply_text("I Was Not Able To Extract The Quality Properly. Renaming As 'Unknown'...")
                    # Mark the file as ignored
                    del renaming_operations[file_id]
                    return  # Exit the handler if quality extraction fails
                
                format_template = format_template.replace(quality_placeholder, "".join(extracted_qualities))           
            
        _, file_extension = os.path.splitext(file_name)
        prefix = await db.get_prefix(user_id)
        suffix = await db.get_suffix(user_id)
        new_file_name = f"{prefix} {format_template} {suffix}{file_extension}"
        file_path = f"downloads/{new_file_name}"
        file = message

        download_msg = await message.reply_text(text="Trying To Download.....")
        try:
            path = await client.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("Download Started....", download_msg, time.time()))
        except Exception as e:
            # Mark the file as ignored
            del renaming_operations[file_id]
            return await download_msg.edit(e)     

        duration = 0
        try:
            metadata = extractMetadata(createParser(file_path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
        except Exception as e:
            print(f"Error getting duration: {e}")

        upload_msg = await download_msg.edit("Trying To Uploading.....")
        ph_path = None
        c_caption = await madflixbotz.get_caption(message.chat.id)
        c_thumb = await madflixbotz.get_thumbnail(message.chat.id)

        caption = c_caption.format(filename=new_file_name, filesize=humanbytes(message.document.file_size), duration=convert(duration)) if c_caption else f"**{new_file_name}**"

        if c_thumb:
            ph_path = await client.download_media(c_thumb)
            print(f"Thumbnail downloaded successfully. Path: {ph_path}")
        elif media_type == "video" and message.video.thumbs:
            ph_path = await client.download_media(message.video.thumbs[0].file_id)

        if ph_path:
            Image.open(ph_path).convert("RGB").save(ph_path)
            img = Image.open(ph_path)
            img.resize((320, 320))
            img.save(ph_path, "JPEG")    
        

        try:
            mrsyd = await db.get_dump(user_id)
            type = media_type  # Use 'media_type' variable instead
            if type == "document":
                sydfil = await client.send_document(
                    mrsyd,
                    document=file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started.....", upload_msg, time.time())
                )
            elif type == "video":
                sydfil = await client.send_video(
                    mrsyd,
                    video=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started.....", upload_msg, time.time())
                )
            elif type == "audio":
                sydfil = await client.send_audio(
                    mrsyd,
                    audio=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started.....", upload_msg, time.time())
                )
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            # Mark the file as ignored
            return await upload_msg.edit(f"Error: {e}")

        mrsyyd = sydfil.document.file_size if type == "document" else sydfil.video.file_size if type == "video" else sydfil.audio.file_size
        mrssyd = message.document.file_size if type == "document" else message.video.file_size if type == "video" else message.audio.file_size
        if mrsyyd != mrssyd:
            await sydfil.delete()
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            del renaming_operations[file_id]
            return await message.reply_text("Sɪᴢᴇ Eʀʀᴏʀ: Pʟᴇᴀꜱᴇ Rᴇɴᴀᴍᴇ Aɢᴀɪɴ...!")
        await download_msg.delete() 
        if user_id != 1733124290:
            await asyncio.sleep(8)
        await message.delete()
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
        




# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Developer @JishuDeveloper
