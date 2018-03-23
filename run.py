#!/usr/bin/env python3
from discordant import Discordant, configure_logging
from time import sleep


if __name__ == '__main__':
    configure_logging()
    exit = False

    bot = Discordant()

    while not exit:
        try:
            bot.run()
        except ConnectionResetError as error:
            print(error)
            print('Reconnecting in 60 seconds...')
            sleep(60)
        except KeyboardInterrupt:
            exit = True
            print('Exiting...')
