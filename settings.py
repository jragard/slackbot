import os
from os.path import join, dirname
from dotenv import load_dotenv
import logging

dotenv_path = join(dirname(__file__), 'commands.env')
load_dotenv('./commands.env')

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

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

if len(log_text) > 1000:
    log = open('./slackbot.log', 'w')
    log.write(" ")
    logger.debug('Log file too long, overwriting')
