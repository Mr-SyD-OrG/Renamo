from config import Config
from pyrogram import Client, filters, enums


API_ID = Config.API_ID
API_HASH = Config.API_HASH
ADMINS = Config.ADMIN

@Client.on_message(filters.command("clone") & filters.user(ADMINS))
async def clone_menu(client, message):
    if len(message.command) == 1:
        return await message.reply_text("**__Give The ᴅᴜᴍᴩ ᴄʜᴀɴɴᴇʟ ɪᴅ__\n\nExᴀᴍᴩʟᴇ:- `/set_dump -1002042969565`**")
    mrsyd = message.text.split(" ", 1)[1]
    syd = Client(
        f"{mrsyd}", API_ID, API_HASH,
        bot_token=mrsyd,
        plugins={"root": "Syd"}
    )
    await syd.start()
    await message.reply_text("✅")

@Client.on_message(filters.command("create") & filters.user(ADMINS))
async def clone_mu(client, message):
    if len(message.command) == 1:
        return await message.reply_text("**__Give The ᴅᴜᴍᴩ ᴄʜᴀɴɴᴇʟ ɪᴅ__\n\nExᴀᴍᴩʟᴇ:- `/set_dump -1002042969565`**")
    mrsyd = message.text.split(" ", 1)[1]
    syd = Client(
        f"{mrsyd}", API_ID, API_HASH,
        bot_token=mrsyd,
        plugins={"root": "Sydon"}
    )
    await syd.start()
    await message.reply_text("✅")

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import re
import asyncio
from datetime import datetime

@Client.on_message(filters.command("addbot") & filters.private)
async def add_bot_handler(client, message: Message):
    async def ask_user(prompt: str):
        sent = await message.reply(f"{prompt}\n\nType /cancel to cancel.")
        try:
            response = await client.listen(
                chat_id=message.chat.id,
                timeout=300
            )
            if response.text.lower() == "/cancel":
                await sent.delete()
                await response.reply("❌ Cancelled.")
                return None
            return response
        except asyncio.TimeoutError:
            await sent.reply("⏰ Timed out.")
            return None

    await message.reply("🔍 Let's gather the details for the new bot.")

    # Step 1: Refer Link
    q1 = await ask_user("Send the referral link:\n`https://t.me/username?start=173290`")
    if not q1: return
    match = re.search(r"https://t\.me/([\w\d_]+)\?start=\d+", q1.text)
    if not match:
        return await message.reply("❌ Invalid referral link format.")
    username = match.group(1)
    name = username.replace("_", "")
    ref_link = f"https://t.me/{username}?start=173290"
    name_link = f"[{name}]({ref_link})"

    # Step 2: Category
    q2 = await ask_user("Category? (`stars | premium | stars and premium`)")
    if not q2: return
    cat = q2.text

    # Step 3: Criteria
    q3 = await ask_user("Criteria? (`game | refer`)")
    if not q3: return
    cri = q3.text

    # Step 4: Verified
    q4 = await ask_user("Verified? (`true | false`)")
    if not q4: return
    ver = q4.text

    # Step 5: Validity
    q5 = await ask_user("Validity? (`unknown | few days | today | expired`)")
    if not q5: return
    val = q5.text

    # Step 6: Per Refer
    q6 = await ask_user("Per refer? (`1 star | 2 star | 3 star`)")
    if not q6: return
    ref = q6.text

    # Step 7: Min Withdraw
    q7 = await ask_user("Minimum withdrawal amount?")
    if not q7: return
    min_amt = q7.text

    # Step 8: More Info (optional)
    q8 = await ask_user("More info? (or type /skip)")
    more = q8.text if q8 and q8.text.lower() != "/skip" else "—"

    # Final Message
    final_text = f"""\
ɴᴇᴡ ʙᴏᴛ       : {name_link}
ᴄᴀᴛᴇɢᴏʀʏ      : {cat}
ᴄʀɪᴛᴇʀɪᴀ       : {cri}
ᴠᴇʀɪꜰɪᴇᴅ       : {ver}
ᴠᴀʟɪᴅɪᴛʏ       : {val}
ᴩᴇʀ ʀᴇꜰᴇʀ     : {ref}
ᴍɪɴ ᴡɪᴛʜᴅʀᴀᴡ : {min_amt}
ᴍᴏʀᴇ ɪɴꜰᴏ     : {more}

({cat.lower()})
🔗 {ref_link}
"""

    await client.send_message(
        chat_id=YOUR_CHANNEL_ID,  # Replace this with your actual channel ID
        text=final_text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴏᴩᴇɴ ʙᴏᴛ", url=ref_link)]]
        ),
        disable_web_page_preview=True
    )

    await message.reply("✅ Bot info successfully sent.")
