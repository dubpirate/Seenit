from multiprocessing.spawn import import_main_path
from time import sleep
from seenit_bot import SeenitBot

if __name__ == "__main__":
    bot = SeenitBot("Seenit_BOT", "SeenitBotTesting")

    while True:
        bot.scan_mentions()

        # Wait for 10 seconds.
        sleep(10)