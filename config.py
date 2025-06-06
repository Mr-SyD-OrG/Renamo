import re, os, time
id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "")
    API_HASH  = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 
    BT_TOKEN = os.environ.get("BT_TOKEN", "") 

    # database config
    DB_NAME = os.environ.get("DB_NAME","cluster0")     
    DB_URL  = os.environ.get("DB_URL","")
    DB_URI  = os.environ.get("DB_URI","")
 
    # other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "https://envs.sh/Z0b.jpg")  
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '').split()]
    FORCE_SUB   = os.environ.get("FORCE_SUB", "Bot_Cracker") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))
    
    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", "True"))


class Txt(object):
    # part of text configuration

    LOG_TEXT_P = """#NewUser
    
Iᴅ - <code>{}</code>
Nᴀᴍᴇ - {} """
    START_TXT = """Hᴇʏ {},
    
➻ Tʜɪꜱ Iꜱ Aɴ Aᴅᴠᴀɴᴄᴇᴅ Aɴᴅ Yᴇᴛ Pᴏᴡᴇʀꜰᴜʟ Rᴇɴᴀᴍᴇ Bᴏᴛ.
➻ Uꜱɪɴɢ Tʜɪꜱ Bᴏᴛ Yᴏᴜ Cᴀɴ AUTO Rᴇɴᴀᴍᴇ Yᴏᴜʀ Fɪʟᴇꜱ.
➻ Tʜɪꜱ Bᴏᴛ Aʟꜱᴏ Sᴜᴩᴩᴏʀᴛꜱ Cᴜꜱᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ Aɴᴅ Cᴀᴩᴛɪᴏɴ.
    
<b>Bot Is Made By @Bot_Cracker</b>"""
    
    FILE_NAME_TXT = """<b><u>SETUP AUTO RENAME FORMAT</u></b>
   
Use These Keywords To Setup Custom File Name

/see_format - Tᴏ ꜱᴇᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ꜰᴏʀᴍᴀᴛ ꜰᴏʀ ꜰɪʟᴇꜱ
/set_format - Tᴏ ꜱᴇᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ꜰᴏʀᴍᴀᴛ ꜰᴏʀ ꜰɪʟᴇꜱ

✓ <code>{episode}</code> :- To Replace Episode Number
✓ <code>{quality}</code> :- To Replace Video Resolution
✓ <code>{season}</code> :- To Rᴇᴩʟᴀᴄᴇ Sᴇᴀꜱᴏɴ Nᴜᴍʙᴇʀ

<b>➻ Example :</b> <code> /set_format Naruto Shippuden S02 - EP{episode} - {quality}  [Dual Audio] - @GetTGLinks </code>

<b>➻ Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Fᴏʀᴍᴀᴛ :</b> <code>{format_template}</code> """
    
    ABOUT_TXT = f"""<b>⋄ Mʏ Nᴀᴍᴇ :</b> <a href='https://t.me/Mr_File_Rename_Bot'>Auto Rename Bot ⚡</a>
<b>⋄ Lᴀɴɢᴜᴀɢᴇ :</b> <a href='https://t.me/+0Zi1FC4ulo8zYzVl'>ꜱᴀᴍᴇ ꜱᴀᴍᴇ ✨</a>
<b>⋄ Lɪʙʀᴀʀʏ :</b> <a href='https://t.me/+-VpGTWWWTldhZWNl'>ᴡᴏʀʟᴅ 🫠</a>
<b>⋄ Sᴇʀᴠᴇʀ :</b> <a href='https://t.me/+vK-YpztZ-x8wYTNl'>TG</a>
<b>⋄ Cʜᴀɴɴᴇʟ :</b> <a href='https://t.me/Bot_cracker'>Bᴏᴛ Cʀᴀᴄᴋᴇʀ 🎋</a>
<b>⋄ Dᴇᴠᴇʟᴏᴩᴇʀ :</b> <a href='https://t.me/Syd_Xyz'>ᴍʀ ꜱʏᴅ 🍪</a>"""

    
    THUMBNAIL_TXT = """<b><u>🖼️  HOW TO SET THUMBNAIL</u></b>
    
⦿ You Can Add Custom Thumbnail Simply By Sending A Photo To Me....
    
⦿ /viewthumb - Use This Command To See Your Thumbnail
⦿ /delthumb - Use This Command To Delete Your Thumbnail"""

    CAPTION_TXT = """<b><u>Hᴏᴡ Tᴏ Sᴇᴛ Cᴀᴩᴛɪᴏɴ 🎼 :</u></b>
    
⦿ /set_caption - Use Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Sᴇᴛ Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ
⦿ /see_caption - Use Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Sᴇᴇ Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ
⦿ /del_caption - Use Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ"""

    PROGRESS_BAR = """\n
<b>📁 Size</b> : {1} | {2}
<b>⏳️ Done</b> : {0}%
<b>🚀 Speed</b> : {3}/s
<b>⏰️ ETA</b> : {4} """

    PRESUF_TXT = """◽ <b><u>Sᴇᴛ ꜱᴜꜰꜰɪx ᴀɴᴅ ᴩʀᴇꜰɪx.</b></u>
<b>•></b> /set_prefix - Sᴇᴛ ᴩʀᴇꜰɪx(ꜰɪʀꜱᴛ ᴡᴏʀᴅ)
<b>•></b> /set_suffix - Sᴇᴛ ꜱᴜꜰꜰɪx(ʟᴀꜱᴛ ᴡᴏʀᴅ)
<b>•></b> /see_prefix - Sᴇᴇ ᴩʀᴇꜰɪx
<b>•></b> /see_suffix - Sᴇᴇ ꜱᴜꜰꜰɪx
<b>•></b> /del_prefix - Dᴇʟᴇᴛᴇ ᴩʀᴇꜰɪx
<b>•></b> /del_suffix - Dᴇʟᴇᴛᴇ ꜱᴜꜰꜰɪx"""
    
    DONATE_TXT = """<b>🥲 Thanks For Showing Interest In Donation! ❤️</b>
    
If You Like My Bots & Projects, You Can 🎁 Donate Me Any Amount From 10 Rs Upto Your Choice.
    
<b>🛍 UPI ID:</b> <code>ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ</code> """

    SEND_METADATA = """ᴀᴅᴅ"""
    HELP_TXT = """<b>Hᴇʏ</b> {} ✨
    
Hᴇʀᴇ Iꜱ Tʜᴇ Hᴇʟᴩ Fᴏʀ Mʏ Cᴏᴍᴍᴀɴᴅꜱ."""





# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Developer @JishuDeveloper

