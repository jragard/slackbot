import time
import os
import re
import signal
import requests
import logging
import random
from dotenv import load_dotenv
from slackclient import SlackClient

logger = logging.getLogger(__name__)

# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
exit_flag = False
start_time = None
slack_client = None


def parse_bot_commands(slack_events):
    global starterbot_id
    """
        Parses a list of events coming from the Slack RTM API to find bot
        commands. If a bot command is found, this function returns a tuple of
        command and channel. If it's not found, then this function
        returns None, None.
    """
    # print slack_events
    for event in slack_events:
        if event["type"] == "message" and "subtype" not in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message
        text and returns the user ID which was mentioned.  If there is no
        direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # first group contains username, second group contains remaining message
    return (matches.group(1),
            matches.group(2).strip()) if matches else (None, None)


def handle_command(command, channel):
    """
        Executes a bot command if the command is known
    """
    print "channel", channel
    global exit_flag

    default_response = """Not sure what you mean.
    Try *{}*.""".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    attachments = None
    # This is where you start to implement more commands
    if command.startswith(EXAMPLE_COMMAND):
        res = command[3:]
        response = res + " " + res + " " + res
    elif command == "exit":
        response = "See ya later!"
        logger.info(command)
        logger.info('Starterbot is Disconnecting')
        exit_flag = True
    elif command == "ping":
        response = "ryanbot is active, uptime = {} seconds".format(
            time.time() - start_time)
        logger.info(command)
        logger.info(response)
    elif command == "help":
        response = """Here is a list of commands:
        exit - Shut me down
        ping - Check my uptime
        help - Display a list of commands for me
        do - Tell me to do something
        bitcoin - Ask me the bitcoin price"""
        logger.info(command)
        logger.info(response)
    elif command == "bitcoin":
        r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        response = "The current bitcoin price in USD is {}".format(
            r.json()['bpi']['USD']['rate'])
        logger.info(command)
        logger.info(response)
    elif command == "loops":
        loops_list = ["https://i.imgur.com/YlfxtAY.jpg",
                      "https://i.imgur.com/Ced9EYj.jpg",
                      "https://i.imgur.com/6CveK8A.jpg",
                      "https://i.imgur.com/CRkrxO9.jpg",
                      "https://i.imgur.com/adVaC1K.jpg",
                      "https://i.kym-cdn.com/photos/images/newsfeed/001/396/303/e34.png",
                      "https://i.kym-cdn.com/photos/images/newsfeed/001/393/674/922.jpg_large",
                      "https://i.kym-cdn.com/photos/images/newsfeed/001/395/618/35d.png",
                      "https://i.imgur.com/Fuax18P.jpg", "https://i.imgflip.com/2g5iig.jpg",
                      "https://i.kym-cdn.com/photos/images/newsfeed/001/393/662/8dc.jpg",
                      "https://i.chzbgr.com/full/9206136064/h7517E5E7/"]

        response = random.choice(loops_list) 
        attachments = {
            "image_url": response
        }
        logger.info(command)
        logger.info(response)
    else:
        response = default_response
    return (response, attachments)


def signal_handler(sig_num, frame):
    global exit_flag

    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here
    as well (SIGHUP?) Basically it just sets a global flag, and main() will
    exit it's loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """

    signame = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                   if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.debug(
        """Received {}, Disconnecting, uptime = {} seconds""".format(
            signame[sig_num], time.time() - start_time))
    exit_flag = True


def setup_logging():
    load_dotenv()
    LOGGING_LEVEL = int(os.getenv('LOGGING_LEVEL'))

    # sets up logger
    logger = logging.getLogger()
    logger.setLevel(LOGGING_LEVEL)

    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler('slackbot.log')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def main():
    global start_time
    global slack_client
    global starterbot_id
    load_dotenv()
    setup_logging()
    SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
    start_time = time.time()

    # instantiate Slack client

    slack_client = SlackClient(SLACK_BOT_TOKEN)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        if slack_client.rtm_connect(with_team_state=False):
            print("Starter Bot connected and running!")
            logger.info('StarterBot connected')

            # Read bot's user ID by calling Web API method `auth.test`
            starterbot_id = slack_client.api_call("auth.test")["user_id"]

            # Send a message to a channel announcing bot is online
            connect_message = "I am online!"

            slack_client.api_call(
                "chat.postMessage",
                channel="CCD7USCR0",
                text=connect_message
            )

            while exit_flag is False:
                try:
                    command, channel = parse_bot_commands(
                        slack_client.rtm_read())
                    if command:
                        response = handle_command(command, channel)[0]
                        attachments = handle_command(command, channel)[1]
                        # Sends the response back to the channel
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=channel,
                            text=response,
                            attachments=attachments
                        )
                    time.sleep(RTM_READ_DELAY)
                except Exception as e:
                    logger.debug(e)
                    time.sleep(5)
        else:
            print("Connection failed. Exception traceback printed above")
    except Exception as failed_connection:
        logger.debug(failed_connection)


if __name__ == "__main__":
    main()
