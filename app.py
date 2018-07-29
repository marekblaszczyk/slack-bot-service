import time

from bot import Bot

RTM_READ_DELAY = 1

if __name__ == "__main__":
    bot = Bot(name='Ziomuś', emoji='cubimal_chick', plugins=['image', 'joke'])
    if bot.slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        bot.auth()
        while True:
            command, channel = bot.parse_bot_commands(bot.slack_client.rtm_read())
            if command:
                bot.handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
