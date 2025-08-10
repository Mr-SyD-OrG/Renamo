import random
from pyrogram import Client, filters, enums
import asyncio
from helper.database import db
from config import Config, Txt
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup



@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [[
                    InlineKeyboardButton('☒ Δᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴩ ☒', url=f'http://t.me/Pro_Moviez_Bot?startgroup=true')
                ],[
                    InlineKeyboardButton('📓 Gᴜɪᴅᴇ 📓', url="https://t.me/MoViE_2022_NT_Bot?start=help")
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(Txt.LOG_TEXT_P.format(message.from_user.mention if message.from_user else message.chat.title), reply_markup=reply_markup, disable_web_page_preview=True)
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(Config.LOG_CHANNEL, Txt.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_ser(message.from_user.id, message.from_user.first_name)
        await client.send_message(Config.LOG_CHANNEL, Txt.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        syd = ["⚡", "🎉", "🫥", "🔥", "🌟", "✨", "🥶", "💫", "🎊", "😶‍🌫️", "👀", "😇", "👾", "😁", "🧭"]
        await message.reply_text(random.choice(syd))
        m=await message.reply_text("<b><i>ꜱᴛᴀʀᴛɪɴɢ...</i></b>")
        await asyncio.sleep(1)
        await m.delete()
        buttons = [[
                    InlineKeyboardButton('☒ Δᴅᴅ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴩ ☒', url=f'http://telegram.me/Pro_Moviez_Bot?startgroup=true')
                ],[
                    InlineKeyboardButton('⌬ GʀᴏUP¹ ⌬', url='https://t.me/+FLScABTbUTI5NmQ1'),
                    InlineKeyboardButton('⇱ GʀᴏUP² ⇲', url='https://t.me/+SQE8nnzWK-Y3MWE9')
                ],[
                    InlineKeyboardButton('⚝ ᴜᴘᦔΔᴛꫀ𝘴 ⚝', url='https://t.me/Bot_Cracker'),
                    InlineKeyboardButton('⊛ Mᴏ∇ɪᴇ ⊛', url='https://t.me/Mod_Moviez_X')
                ],[
                    InlineKeyboardButton("◎   ʙᴏᴛꜱ   ◎", url='https://t.me/Bot_Cracker/17')
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=f"<b><blockquote>ʜᴇʏ, {message.from_user.mention}</blockquote> \n\nSᴇᴀʀᴄʜ ᴀɴʏ ᴍᴏᴠɪᴇꜱ ʏᴏᴜ ᴡᴀɴᴛ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴏɴ ʀᴇꜱᴩᴇᴄᴛɪᴠᴇ ʙᴜᴛᴛᴏɴ⚡ \n\n<u>Aɴʏ ᴛʜɪɴɢ ᴍɪꜱꜱɪɴɢ? ᴛʜᴇɴ ᴊᴜꜱᴛ ꜱᴇɴᴅ ɪᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴩ ᴀɴᴅ ʏᴏᴜ'ʟʟ ɢᴇᴛ ☺️</u></b>",
           # photo=random.choice(PICS),
           # caption=script.START_TXT.format(message.from_user.mention, gtxt, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return

import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

@Client.on_message(filters.command("forward", prefixes="/"))
async def forward_messages(client, message):
    try:
        # /forward from_chat to_chat start_id end_id pause_seconds
        parts = message.text.split()
        if len(parts) < 5:
            return await message.reply(
                "Usage: `/forward {from} {to} {start_id} {end_id} {pause_seconds}`",
                quote=True
            )

        from_chat = parts[1]
        to_chat = parts[2]
        start_id = int(parts[3])
        end_id = int(parts[4])
        pause_seconds = float(parts[5]) if len(parts) > 5 else 1.0

        sent_count = 0
        total_messages = end_id - start_id + 1
        progress_msg = await message.reply("Forwarding started...")

        for msg_id in range(start_id, end_id + 1):
            try:
                msg = await client.get_messages(from_chat, msg_id)
                if not msg:
                    continue

                while True:
                    try:
                        await msg.copy(to_chat)
                        sent_count += 1
                        break
                    except FloodWait as e:
                        print(f"FloodWait: Sleeping {e.value} seconds for message {msg_id}")
                        await asyncio.sleep(e.value)
                    except Exception as e:
                        print(f"Failed to copy message {msg_id}: {e}")
                        break

                if sent_count % 100 == 0:
                    try:
                        await progress_msg.edit_text(
                            f"📤 Forwarded {sent_count}/{total_messages} messages..."
                        )
                    except Exception as e:
                        print(f"Progress edit failed: {e}")

                await asyncio.sleep(pause_seconds)

            except Exception as e:
                print(f"Error fetching message {msg_id}: {e}")

        await progress_msg.edit_text("✅ Forwarding completed.")

    except Exception as e:
        await message.reply(f"❌ Error: {e}")
