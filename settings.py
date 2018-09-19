import os
from os.path import join, dirname
from dotenv import load_dotenv
import logging

dotenv_path = join(dirname(__file__), 'commands.env')
# print 'dotenv path', dotenv_path
load_dotenv('./commands.env')

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

# Sets up logger basic config
# logging.basicConfig(level=logging.DEBUG, filename='slackbot.log', format='%(levelname)s:%(name)s:%(message)s')

# sets up logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('slackbot.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

log_object = open('./slackbot.log', 'r')
log_text = log_object.read()
print 'log length', len(log_text)

if len(log_text) > 15000:
    log = open('./slackbot.log', 'w')
    log.write("""Log File too long, overwriting
                --------------------------------
              """)
