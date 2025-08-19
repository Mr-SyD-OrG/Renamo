
from pyrogram import Client, filters, enums
import asyncio
from helper.database import db
from config import Config, Txt



@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(Config.LOG_CHANNEL, Txt.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_ser(message.from_user.id, message.from_user.first_name)
        await client.send_message(Config.LOG_CHANNEL, Txt.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
        return


@Client.on_message(filters.chat(SOURCE_CHAT_ID) & filters.incoming)
async def forward_and_edit(client, message):
    try:
        # Forward message
        fwd_msg = await message.forward(TARGET_CHAT_ID)

        # Detect file name
        file_name = None
        if message.document:
            file_name = message.document.file_name
        elif message.video:
            file_name = message.video.file_name
        elif message.audio:
            file_name = message.audio.file_name
        elif message.voice:
            file_name = "Voice Message"
        elif message.photo:
            file_name = "Photo"
        if file_name:
            try:
                await fwd_msg.edit_caption(file_name)
            except Exception:
                pass  # if no caption exists (like in photo), ignore

    except Exception as e:
        print("Error:", e)
