import time
import re
import settings
import signal
from slackclient import SlackClient

# instantiate Slack client
slack_client = SlackClient(settings.SLACK_BOT_TOKEN)


# starterbot's user ID in Slack: value is assigned after the bot starts up

starterbot_id = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
exit_flag = True


def parse_bot_commands(slack_events):
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
    global exit_flag
    # Default response is help text for the user
    default_response = """Not sure what you mean.
    Try *{}*.""".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands
    if command.startswith(EXAMPLE_COMMAND):
        # response = "Sure...write some more code then I can do that!"
        res = command[3:]
        response = res + " " + res + " " + res
    if command == "exit":
        response = "See ya later!"
        settings.logger.info(command)
        settings.logger.info('Starterbot is Disconnecting, uptime = {} seconds'.format(
            time.time() - start_time
        ))
        exit_flag = False
    if command == "ping":
        response = "ryanbot is active, uptime = {} seconds".format(
            time.time() - start_time)
        settings.logger.info(command)
        settings.logger.info(response)
    if command == "help":
        response = """Here is a list of commands:
        exit
        ping
        help
        do
                   """
        settings.logger.info(command)
        settings.logger.info(response)

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

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
    print 'Signal Number ', sig_num
    signame = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                   if v.startswith('SIG') and not v.startswith('SIG_'))
    settings.logger.debug('Received {}, Disconnecting, uptime = {} seconds'.format(signame[sig_num], time.time() - start_time))
    exit_flag = False


if __name__ == "__main__":
    start_time = time.time()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        settings.logger.info('StarterBot connected')
        
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]

        # Send a message to a channel announcing bot is online
        connect_message = "I am online!"

        # slack_client.api_call(
        #     "chat.postMessage",
        #     channel="CCD7USCR0",
        #     text=connect_message
        # )

        while exit_flag is True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
        
    else:
        print("Connection failed. Exception traceback printed above")
