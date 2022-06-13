import telegram.ext
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO)
logging.info('Starting bot')

with open('token.txt', 'r') as f:
    TOKEN = f.read()


# Insert Group chat's ID with - sign
group_id = '-XXXXXXXXXXXXX'

updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher
j = updater.job_queue


def alarm(context):
    context.bot.send_message(chat_id=group_id, text='Insert text to send')


def timer(update, context):
    context.bot.send_message(text='Started sending messages', chat_id=update.message.chat_id)

    # measured in seconds, currently for 5 seconds, change interval, first only
    context.job_queue.run_repeating(alarm, interval=5, first=5, name='timer')


def remove_job_if_exists(name, context):
    current_jobs = j.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def start(update, context):
    context.bot.send_message(text='''
    Hi!
    to start sending messages use /timer
    to stop sending use /stop
    ''', chat_id=update.message.chat_id)


def stop(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(name='timer', context=context.bot)
    text = 'Stopped sending messages' if job_removed else 'You have no active session'
    context.bot.send_message(text=text, chat_id=chat_id)


def error(update, context):
    logging.error(f'Error {context.error}')


def start_bot():
    disp.add_handler(telegram.ext.CommandHandler('start', start))
    disp.add_handler(telegram.ext.CommandHandler('timer', timer))
    disp.add_handler(telegram.ext.CommandHandler('stop', stop))

    disp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


start_bot()
