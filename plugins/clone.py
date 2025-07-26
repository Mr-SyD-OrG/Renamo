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

@Client.on_message(filters.command("addbot") & filters.private)
async def add_bot_handler(client, message: Message):
    async def ask_user(text):
        try:
            return await client.ask(
                chat_id=message.chat.id,
                text=text + "\n\nType /cancel to cancel.",
                filters=filters.text & ~filters.command("cancel"),
                timeout=300
            )
        except Exception:
            return None

    await message.reply("🔍 Let's gather the details for the new bot.")

    # Name & Refer link
    q1 = await ask_user("Send the referral link:\n`https://t.me/username?start=173290`")
    if not q1 or q1.text.lower() == "/cancel":
        return await message.reply("❌ Cancelled.")
    match = re.search(r"https://t\.me/([\w\d_]+)\?start=\d+", q1.text)
    if not match:
        return await message.reply("❌ Invalid referral link format.")
    username = match.group(1)
    name = username.replace("_", "")
    ref_link = f"https://t.me/{username}?start=173290"
    name_link = f"[{name}]({ref_link})"

    # Category
    q2 = await ask_user("Category? (`stars | premium | stars and premium`)")
    if not q2 or q2.text.lower() == "/cancel":
        return await message.reply("❌ Cancelled.")
    cat = q2.text

    # Criteria
    q3 = await ask_user("Criteria? (`game | refer`)")
    if not q3 or q3.text.lower() == "/cancel":
        return await message.reply("❌ Cancelled.")
    cri = q3.text

    # Verified
    q4 = await ask_user("Verified? (`true | false`)")
    if not q4 or q4.text.lower() == "/cancel":
        return await message.reply("❌ Cancelled.")
    ver = q4.text

    # Validity
    q5 = await ask_user("Validity? (`unknown | few days | today | expired`)")
    if not q5 or q5.text.lower() == "/cancel":
        return await message.reply("❌ Cancelled.")
    val = q5.text

    # Per Refer
    q6 = await ask_user("Per refer? (`1 star | 2 star | 3 star`)")
    if not q6 or q6.text.lower() == "/cancel":
        return await message.reply("❌ Cancelled.")
    ref = q6.text

    # Min Withdraw
    q7 = await ask_user("Minimum withdrawal amount?")
    if not q7 or q7.text.lower() == "/cancel":
        return await message.reply("❌ Cancelled.")
    min_amt = q7.text

    # More Info (optional)
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

    # Send with inline button
    await client.send_message(
        chat_id=YOUR_CHANNEL_ID,  # Replace with actual channel ID
        text=final_text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴏᴩᴇɴ ʙᴏᴛ", url=ref_link)]]
        ),
        disable_web_page_preview=True
    )

    await message.reply("✅ Bot info successfully shared.")
