import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler

import finn

TOKEN = "5417799349:AAEn8AYUDpEuHBCMkGy2bk1NLlrv7CWJ0sw"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Send any non-command message, and I'll list you my commands!")


async def show_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["/set_job_notification"], 
                ["/set_boat_notification"], 
                ["/unset_job_notification"], 
                ["/unset_boat_notification"]]
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="Here are my available commands",
                                   disable_notification=True,
                                   reply_markup=ReplyKeyboardMarkup(keyboard))


if __name__ == '__main__':
    global sheila_job
    sheila_job = finn.SheilaJob()

    global jon_boat
    jon_boat = finn.JonBoat()

    application = ApplicationBuilder().token(TOKEN).build()
    
    # Finn commands
    application.add_handler(CommandHandler('set_job_notification', sheila_job.set_notification))
    application.add_handler(CommandHandler('unset_job_notification', sheila_job.unset_notification))
    application.add_handler(CommandHandler('set_boat_notification', jon_boat.set_notification))
    application.add_handler(CommandHandler('unset_boat_notification', jon_boat.unset_notification))

    # Other commands
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), show_commands))
    
    application.run_polling()
