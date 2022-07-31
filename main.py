from datetime import datetime, timedelta
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler

from check_finn import SheilaJob

TOKEN = "5417799349:AAEn8AYUDpEuHBCMkGy2bk1NLlrv7CWJ0sw"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def notify_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id
    try:
        name = str(chat_id)+":job_notificatin"
        job_removed = remove_job_if_exists(name, context)
        first_time = datetime(2022, 7, 30, 8)
        context.job_queue.run_repeating(send_notification, 1800, first=first_time, chat_id=chat_id, name=name)

        text = "Job notification setup successfully."
        if job_removed:
            text += "\nOld one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")


async def send_notification(context: ContextTypes.DEFAULT_TYPE):
    job = context.job

    message_parts = sheila_job.get_new_articles()
    if len(message_parts) == 0:
        return

    message = "New jobs have been posten on Finn! Check them out:\n\n"
    for message_part in message_parts:
        message += "\n" + message_part + "\n"

    await context.bot.send_message(chat_id=job.chat_id, text=message)


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id)+":job_notificatin", context)
    text = "Notification successfully cancelled!" if job_removed else "You have no active notification."
    await update.message.reply_text(text)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.text)
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


if __name__ == '__main__':
    global sheila_job
    sheila_job = SheilaJob()

    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('notify', notify_job))
    application.add_handler(CommandHandler('unset', unset))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    
    application.run_polling()
