from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from helper.database import madflixbotz

@Client.on_message(filters.private & filters.command("set_format"))
async def auto_renme_command(client, message):
    user_id = message.from_user.id

    # Extract the format from the command
    format_template = message.text.split("/set_format", 1)[1].strip()

    # Save the format template to the database
    await madflixbotz.set_format_template(user_id, format_template)

    await message.reply_text("**Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Fᴏʀᴍᴀᴛ Uᴘᴅᴀᴛᴇᴅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!✅**")
    
@Client.on_message(filters.private & filters.command("see_format"))
async def auto_rename_command(client, message):
    user_id = message.from_user.id
    syd = await madflixbotz.get_format_template(user_id)
    await message.reply_text(f'⚡ Yᴏᴜʀ ꜰᴏʀᴍᴀᴛ ; {syd}')



@Client.on_message(filters.private & filters.command("setmedia"))
async def set_media_command(client, message):
    user_id = message.from_user.id    
    media_type = message.text.split("/setmedia", 1)[1].strip().lower()

    # Save the preferred media type to the database
    await madflixbotz.set_media_preference(user_id, media_type)

    await message.reply_text(f"**Mᴇᴅɪᴀ Pʀᴇꜰᴇʀᴇɴᴄᴇ Sᴇᴛ Tᴏ :** {media_type} ✅")






# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Developer @JishuDeveloper
