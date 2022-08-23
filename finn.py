from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes


########## Classes #########################################################################################

class FinnSearch:
    def __init__(self):
        self.seen_links = []
        self.url = None
        self.name_ending = ""
        self.time_interval = 1800

    def get_new_articles(self):
        if not self.url:
            return []

        page = urlopen(self.url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        result_set = soup.find_all("a", attrs={"class":"ads__unit__link"})
        new_results = []
        for article in result_set:
            link = str(article).split(" ")[2][6:-1]
            if link not in self.seen_links:
                self.seen_links.append(link)
                new_results.append(link)
        
        return new_results
    

    def remove_job_if_exists(self, name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Remove job with given name. Returns whether job was removed."""
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()

        jobs_saved = self.save_jobs_to_file(context)
        if not jobs_saved:
            print("Error: could not save jobs.")
        return True


    async def send_notification(self, context: ContextTypes.DEFAULT_TYPE):
        job = context.job

        message_parts = self.get_new_articles()
        if len(message_parts) == 0:
            return

        elif len(message_parts) == 1:
            message = "A new job has been posten on Finn! Check it out:\n\n"
        else:
            message = "New jobs have been posten on Finn! Check them out:\n\n"

        for message_part in message_parts:
            message += "\n" + message_part + "\n"

        await context.bot.send_message(chat_id=job.chat_id, text=message)


    async def set_notification(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_message.chat_id
        try:
            name = str(chat_id)+self.name_ending
            job_removed = self.remove_job_if_exists(name, context)
            # first_time = datetime(2022, 7, 30, 8)
            context.job_queue.run_repeating(self.send_notification, self.time_interval, chat_id=chat_id, name=name)

            jobs_saved = self.save_jobs_to_file(context)
            if not jobs_saved:
                print("Error: could not save jobs.")

            text = "Notification setup successfully."
            if job_removed:
                text += "\nOld one was removed."
            await update.effective_message.reply_text(text)

        except (IndexError, ValueError):
            await update.effective_message.reply_text("Error: failed to set notification")
        
        await show_notifications(update, context)


    async def unset_notification(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Remove the job if the user changed their mind."""
        chat_id = update.message.chat_id
        job_removed = self.remove_job_if_exists(str(chat_id)+self.name_ending, context)
        text = "Notification successfully cancelled!" if job_removed else "You have no active notification."
        await update.message.reply_text(text)
        await show_notifications(update, context)


    def save_jobs_to_file(self, context: ContextTypes.DEFAULT_TYPE):
        try:
            file = open("jobs.txt", "w")
            jobs = context.job_queue.jobs()
            for job in jobs:
                file.write(job.name+"\n")
            file.close()
            return True
        except:
            print("Couldn't save jobs to file...")
            return False



async def show_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = [job for job in context.job_queue.jobs() if job.name.split(":")[0] == str(update.effective_chat.id)]

    if len(jobs) == 0:
        message = "You have no active notifications"
    else:
        message = "Your active notifcation(s):"
        for job in jobs:
            message += "\n"+job.name.split(":")[1]

    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=message,
                                   disable_notification=True)





########## Search classes #########################################################################################

class SheilaJob(FinnSearch):
    def __init__(self):
        super().__init__()
        self.url = "https://www.finn.no/job/fulltime/search.html?industry=1&industry=14&industry=3&industry=51&industry=53&lat=63.39188178422313&location=2.20001.20016.20318&lon=10.436492112530033&published=1&radius=7000&sort=RELEVANCE"
        self.name_ending = ":job_notification"

class JonBoat(FinnSearch):
    def __init__(self):
        super().__init__()
        self.url = "https://www.finn.no/boat/forsale/search.html?class=2186&length_feet_from=9&length_feet_to=10&location=20016&published=1&sort=PUBLISHED_DESC"
        self.name_ending = ":boat_notification"


    