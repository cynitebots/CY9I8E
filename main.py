# (c) @RoyalKrrishna

from configs import Config
from pyrogram import Client, filters, idle
from pyrogram.errors import QueryIdInvalid
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent
from TeamTeleRoid.forcesub import ForceSub
import asyncio

# Bot Client for Inline Search
Bot = Client(
    session_name=Config.BOT_SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# User Client for Searching in Channel.
User = Client(
    session_name=Config.USER_SESSION_STRING,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

@Bot.on_message(filters.private & filters.command("start"))
async def start_handler(_, event: Message):
	await event.reply_photo("https://telegra.ph/file/90687a45c08f28709ea59.jpg",
                                caption=Config.START_MSG.format(event.from_user.mention),
                                reply_markup=InlineKeyboardMarkup([
                                    [InlineKeyboardButton("'⚚ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⚚", url="http://t.me/CynitemdiskBoT?startgroup=true")],
                                    [InlineKeyboardButton("🔮ᴏᴜʀ ᴄʜᴀɴɴᴇʟ🔮", url="https://t.me/Cynitemovies"),
                                     InlineKeyboardButton("👥ᴏᴜʀ ɢʀᴏᴜᴘ👥", url="https://t.me/CyniteMoviesGroup")],
                                    [InlineKeyboardButton("💠ʜᴇʟᴘ", callback_data="Help_msg"),
                                     InlineKeyboardButton("🔰ᴀʙᴏᴜᴛ", callback_data="About_msg")]]))

@Bot.on_message(filters.private & filters.command("help"))
async def help_handler(_, event: Message):

    await event.reply_text(Config.ABOUT_HELP_TEXT.format(event.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔮ᴏᴜʀ ᴄʜᴀɴɴᴇʟ🔮", url="https://t.me/CyniteMovies"),
             InlineKeyboardButton("👥ᴏᴜʀ ɢʀᴏᴜᴘ👥", url="https://t.me/CynitemoviesGroup"), 
             InlineKeyboardButton("🔰ᴀʙᴏᴜᴛ", callback_data="About_msg")]
        ])
    )

@Bot.on_message(filters.incoming)
async def inline_handlers(_, event: Message):
    if event.text == '/start':
        return
    answers = f'**📂 Results For ➠ {event.text} \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n➠ Type Only Movie Name With Correct Spelling.✍️\n➠ Add Year For Better Result.🗓️\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n**'
    async for message in User.search_messages(chat_id=Config.CHANNEL_ID, limit=50, query=event.text):
        if message.text:
            thumb = None
            f_text = message.text
            msg_text = message.text.html
            if "|||" in message.text:
                f_text = message.text.split("|||", 1)[0]
                msg_text = message.text.html.split("|||", 1)[0]
            answers += f'**🍿 Title ➠ ' + '' + f_text.split("\n", 1)[0] + '' + '\n\n📜 About ➠ ' + '' + f_text.split("\n", 2)[-1] + ' \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\nLink Will Auto Delete In 60Sec...⏰\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n**'
    try:
        msg = await event.reply_text(answers)
        await asyncio.sleep(60)
        await event.delete()
        await msg.delete()
    except:
        print(f"[{Config.BOT_SESSION_NAME}] - Failed to Answer - {event.from_user.first_name}")


@Bot.on_callback_query()
async def button(bot, cmd: CallbackQuery):
        cb_data = cmd.data
        if "About_msg" in cb_data:
            await cmd.message.edit(
			text=Config.ABOUT_BOT_TEXT,
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("🔮ᴏᴜʀ ᴄʜᴀɴɴᴇʟ🔮", url="https://t.me/Cynitemovies"),
						InlineKeyboardButton("👥ᴏᴜʀ ɢʀᴏᴜᴘ👥", url="https://t.me/CyniteMoviesGroup")
					],
					[
						InlineKeyboardButton("💻ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/teamx69"),
						InlineKeyboardButton("🏠ʜᴏᴍᴇ", callback_data="gohome")
					]
				]
			),
			parse_mode="html"
		)
        elif "Help_msg" in cb_data:
            await cmd.message.edit(
			text=Config.ABOUT_HELP_TEXT,
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("🔰ᴀʙᴏᴜᴛ", callback_data="About_msg"),
						InlineKeyboardButton("🔮ᴏᴜʀ ᴄʜᴀɴɴᴇʟ🔮", url="https://t.me/Cynitemovies")
					], 
                                        [
						InlineKeyboardButton("🗣️Owner", url="https://t.me/teamx69"),
						InlineKeyboardButton("🏠ʜᴏᴍᴇ", callback_data="gohome")
					]
				]
			),
			parse_mode="html"
		)
        elif "gohome" in cb_data:
            await cmd.message.edit(
			text=Config.START_MSG.format(cmd.from_user.mention),
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
                                        [
						InlineKeyboardButton("💠ʜᴇʟᴘ", callback_data="Help_msg"),
						InlineKeyboardButton("🔰ᴀʙᴏᴜᴛ", callback_data="About_msg")
					],
					[
						InlineKeyboardButton("📞sᴜᴘᴘᴏʀᴛ", url="https://t.me/teamx69"),
						InlineKeyboardButton("🔮ᴏᴜʀ ᴄʜᴀɴɴᴇʟ🔮", url="https://t.me/cynitemovies")
					]
				]
			),
			parse_mode="html"
		)

# Start Clients
Bot.start()
User.start()
# Loop Clients till Disconnects
idle()
# After Disconnects,
# Stop Clients
Bot.stop()
User.stop()
