from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import madflixbotz as db
#from pyromod.exceptions import ListenerTimeout
from config import Txt
from plugins.features import features_button


@Client.on_message(filters.private & filters.command('metadata'))
async def handle_metadata(bot: Client, message: Message):

    ms = await message.reply_text("**Please Wait...**")
    user_metadata = await db.get_metadata_code(message.from_user.id)
    markup = await features_button(message.from_user.id)

    await ms.edit(f'**ʜᴇʀᴇ ᴛʜᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴇᴀᴛᴜʀᴇ** 🍀**\n\nYour Current Metadata:-\n\n➜ `{user_metadata}` ', reply_markup=markup)


@Client.on_message(filters.private & filters.command('set_metadata'))
async def handle_set_metadata(bot: Client, message: Message):
    if len(message.command) == 1:
        return await message.reply_text("**__Give The ᴅᴜᴍᴩ ᴄʜᴀɴɴᴇʟ ɪᴅ__\n\nExᴀᴍᴩʟᴇ:- `/set_dump -1002042969565`**")
    mrsyd = message.text.split(" ", 1)[1]
    ms = await message.reply_text("**Please Wait...**", reply_to_message_id=message.id)
    await db.set_metadata_code(message.from_user.id, metadata_code=mrsyd)
    await ms.edit("**Your Metadta Code Set Successfully ✅**")
