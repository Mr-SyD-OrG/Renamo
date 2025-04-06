import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery, Message, InputMediaPhoto

from helper.database import madflixbotz
from config import Config, Txt  
db = madflixbotz
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    await madflixbotz.add_user(client, message)                
    button = InlineKeyboardMarkup([[
      InlineKeyboardButton('◇ Uᴩᴅᴀᴛᴇ', url='https://t.me/Bot_Cracker'),
      InlineKeyboardButton('Sᴜᴩᴩᴏʀᴛ ◇', url='https://t.me/Mod_Moviez_X')
    ],[
      InlineKeyboardButton('❂ Hᴇʟᴩ', callback_data='help'),
      InlineKeyboardButton('Aʙᴏᴜᴛ ❂', callback_data='about')
    ]])
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)       
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)   

@Client.on_message(filters.private & filters.command("season"))
async def sydson(client, message):
    mrsyd = await db.get_sydson(message.from_user.id)
    if mrsyd == "True":
        button = InlineKeyboardMarkup([[
          InlineKeyboardButton('Fᴀʟꜱᴇ ✖️', callback_data='season_false')
          ],[
          InlineKeyboardButton("✖️ Close", callback_data="close")
        ]])
    else:
        button = InlineKeyboardMarkup([[
          InlineKeyboardButton('Tʀᴜᴇ ✅', callback_data='season_true')
          ],[
          InlineKeyboardButton("✖️ Close", callback_data="close")
        ]])
    await message.reply_text(text="Sᴇᴛ ᴛʀᴜᴇ ᴏʀ ꜰᴀʟꜱᴇ, ɪꜰ ꜱᴇᴀꜱᴏɴ ɴᴜᴍʙᴇʀ ɪꜱ ᴛᴏ ʙᴇ ɪɴ ꜰɪʟᴇ ᴇᴠᴇʀʏᴛɪᴍᴇ (ɪꜰ ꜰɪʟᴇ ᴅᴏɴᴛ ʜᴀᴠᴇ ꜱᴇᴀꜱᴏɴ ɴᴏ. ɪᴛ ᴡɪʟʟ ʙᴇ ᴅᴇꜰᴜᴀʟᴛ ᴛᴏ 1) ᴏʀ ꜰᴀʟꜱᴇ ᴛᴏ ᴀᴠᴏɪᴅ ꜱᴇᴀꜱᴏɴ ᴛᴀɢ", reply_markup=button)   

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    user_id = query.from_user.id  
    
    if data == "home":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton('◇ Uᴩᴅᴀᴛᴇ', url='https://t.me/Bot_Cracker'),
                InlineKeyboardButton('Sᴜᴩᴩᴏʀᴛ ◇', url='https://t.me/Mod_Moviez_X')
                ],[
                InlineKeyboardButton('❂ Hᴇʟᴩ', callback_data='help'),
                InlineKeyboardButton('Aʙᴏᴜᴛ ❂', callback_data='about')
            ]])
        )
    elif data == "caption":
        await query.message.edit_text(
            text=Txt.CAPTION_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⛒ Cʟᴏꜱᴇ ⛒", callback_data="close"),
                InlineKeyboardButton("⇇ Bᴀᴄᴋ", callback_data="help")
            ]])            
        )
    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⛭ Sᴇᴛᴜᴩ AᴜᴛᴏRᴇɴᴀᴍᴇ Fᴏʀᴍᴀᴛ ⛭", callback_data='file_names')
                ],[
                InlineKeyboardButton('◼ Tʜᴜᴍʙɴᴀɪʟ', callback_data='thumbnail'),
                InlineKeyboardButton('Pʀᴇ-ꜱᴜꜰꜰɪx', callback_data='thumbnail'),
                InlineKeyboardButton('Cᴀᴩᴛɪᴏɴ ✎', callback_data='caption')
                ],[
                InlineKeyboardButton('⌂ Hᴏᴍᴇ', callback_data='home'),
                InlineKeyboardButton('Dᴏɴᴀᴛᴇ ◇', callback_data='donate')
                ]])
        )


    elif data == "fix":
        await query.message.edit_text(
            text=Txt.PRESUF_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⛒ Cʟᴏꜱᴇ ⛒", callback_data="close"),
                InlineKeyboardButton("⇇ Bᴀᴄᴋ", callback_data="help")
            ]])            
        )
    elif data == "donate":
        await query.message.edit_text(
            text=Txt.DONATE_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⛒ Cʟᴏꜱᴇ ⛒", callback_data="close"),
                InlineKeyboardButton("⇇ Bᴀᴄᴋ", callback_data="help")
            ]])          
        )
    
    elif data == "file_names":
        season = "{season}"
        episode = "{episode}"
        format_template = await madflixbotz.get_format_template(user_id)
        await query.message.edit_text(
            text=Txt.FILE_NAME_TXT.format(season=season, episode=episode, format_template=format_template),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⛒ Cʟᴏꜱᴇ ⛒", callback_data="close"),
                InlineKeyboardButton("⇇ Bᴀᴄᴋ", callback_data="help")
            ]])
        )      
    
    elif data == "thumbnail":
        await query.message.edit_caption(
            caption=Txt.THUMBNAIL_TXT,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⛒ Cʟᴏꜱᴇ ⛒", callback_data="close"),
                InlineKeyboardButton("⇇ Bᴀᴄᴋ", callback_data="help"),
            ]]),
        )

    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⛒ Cʟᴏꜱᴇ ⛒", callback_data="close"),
                InlineKeyboardButton("⇇ Bᴀᴄᴋ", callback_data="home")
            ]])          
        )

    elif data == "season_false":
        await db.set_sydson(user_id, "False")
        await query.message.edit_text(
            text="Sᴇᴛ ᴛʀᴜᴇ ᴏʀ ꜰᴀʟꜱᴇ, ɪꜰ ꜱᴇᴀꜱᴏɴ ɴᴜᴍʙᴇʀ ɪꜱ ᴛᴏ ʙᴇ ɪɴ ꜰɪʟᴇ ᴇᴠᴇʀʏᴛɪᴍᴇ (ɪꜰ ꜰɪʟᴇ ᴅᴏɴᴛ ʜᴀᴠᴇ ꜱᴇᴀꜱᴏɴ ɴᴏ. ɪᴛ ᴡɪʟʟ ʙᴇ ᴅᴇꜰᴜᴀʟᴛ ᴛᴏ 1) ᴏʀ ꜰᴀʟꜱᴇ ᴛᴏ ᴀᴠᴏɪᴅ ꜱᴇᴀꜱᴏɴ ᴛᴀɢ",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Tʀᴜᴇ ✅", callback_data="season_true")
            ],[
                InlineKeyboardButton("✖️ Close", callback_data="close")
            ]])          
        )
            
    elif data == "season_true":
        await db.set_sydson(user_id, "True")
        await query.message.edit_text(
            text="Sᴇᴛ ᴛʀᴜᴇ ᴏʀ ꜰᴀʟꜱᴇ, ɪꜰ ꜱᴇᴀꜱᴏɴ ɴᴜᴍʙᴇʀ ɪꜱ ᴛᴏ ʙᴇ ɪɴ ꜰɪʟᴇ ᴇᴠᴇʀʏᴛɪᴍᴇ (ɪꜰ ꜰɪʟᴇ ᴅᴏɴᴛ ʜᴀᴠᴇ ꜱᴇᴀꜱᴏɴ ɴᴏ. ɪᴛ ᴡɪʟʟ ʙᴇ ᴅᴇꜰᴜᴀʟᴛ ᴛᴏ 1) ᴏʀ ꜰᴀʟꜱᴇ ᴛᴏ ᴀᴠᴏɪᴅ ꜱᴇᴀꜱᴏɴ ᴛᴀɢ",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Fᴀʟꜱᴇ ✖️", callback_data="season_false")
            ],[
                InlineKeyboardButton("✖️ Close", callback_data="close")
            ]])          
        )
    
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()






# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Developer @JishuDeveloper
