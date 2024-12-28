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
    try:
        metadata = await bot.ask(text=Txt.SEND_METADATA, chat_id=message.from_user.id, filters=filters.text, disable_web_page_preview=True)
    except:
        return 
    if metadata == "/cancel":
        return
    print(metadata.text)
    ms = await message.reply_text("**Please Wait...**", reply_to_message_id=metadata.id)
    await db.set_metadata_code(message.from_user.id, metadata_code=metadata.text)
    await ms.edit("**Your Metadta Code Set Successfully ✅**")
