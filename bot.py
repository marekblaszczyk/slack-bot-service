import os
import re
from importlib import import_module

from slackclient import SlackClient

from plugin import PluginProvider


EXAMPLE_COMMAND = "!help"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


class Bot(object):

    default_msg = "Nie wiem o co Ci chodzi, informatyku? Spróbuj wpisać *{}*.".format(
        EXAMPLE_COMMAND
    )

    def __init__(self, name, emoji, plugins):
        self.name = name
        self.emoji = ':{}:'.format(emoji)
        self.slack_bot_token = os.environ.get('SLACK_BOT_TOKEN')
        self.starterbot_id = None
        self.slack_client = SlackClient(self.slack_bot_token)
        self.load_plugins(plugins)
        self.plugins = PluginProvider.get_plugins()

    def auth(self):
        self.starterbot_id = self.slack_client.api_call("auth.test")["user_id"]

    # def dynamic_import(self, abs_module_path, class_name):
    #     module_object = import_module(abs_module_path)
    #     target_class = getattr(module_object, class_name)
    #     return target_class

    @staticmethod
    def load_plugins(plugins):
        """Later add selective plugins import."""
        import_module('plugins', package=__name__)

    def parse_bot_commands(self, slack_events):
        """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event['type'] == 'message' and not 'subtype' in event:
                user_id, message = self.parse_exclamation_mark_message(event['text'])
                if not user_id:
                    user_id, message = self.parse_direct_mention(event['text'])
                if user_id == self.starterbot_id:
                    return message, event['channel']
        return None, None

    def parse_exclamation_mark_message(self, message_text):
        """
        Find all messages with exclamation_mark and return the user ID
        and message for further service.
        """
        if message_text.startswith('!'):
            return self.starterbot_id, message_text.strip()
        return None, None

    @staticmethod
    def parse_direct_mention(message_text):
        """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def handle_command(self, command, channel):
        """Executes bot command if the command is known"""
        # Default response is help text for the user
        default_response = self.default_msg

        # Finds and executes the given command, filling in response
        response = None
        # This is where you start to implement more commands!
        if command.startswith(EXAMPLE_COMMAND):
            response = "Uuuu działa, ale jeszcze nic nie umiem!"

        # Sends the response back to the channel
        self.slack_client.api_call(
            "chat.postMessage", channel=channel, username=self.name, icon_emoji=self.emoji,
            text=response or default_response
        )
