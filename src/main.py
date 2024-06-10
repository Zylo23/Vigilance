from config import Config
from trigger_bot import TriggerBot
from colorama import init, Fore, Style
from hashlib import sha256
from random import random
from version import __version__


def main():
    init(autoreset=True)
    
    hash_value = sha256(str(random()).encode('utf-8')).hexdigest()[:8]
    print(f'{Style.BRIGHT}{Fore.BLUE}Vigilance {__version__} | {hash_value}{Style.RESET_ALL}')

    config = Config.load_config()
    bot = TriggerBot(config)
    bot.run()

    
if __name__ == '__main__':
    main()
