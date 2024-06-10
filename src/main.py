from config import Config
from trigger_bot import TriggerBot
from colorama import init
from hashlib import sha256
from random import random
from version import __version__


def main():
    init()
    
    hash = sha256(str(random()).encode('utf-8')).hexdigest()
    print(f'Vigilance {__version__} | {hash}')

    config = Config.load_config()
    TriggerBot(config).run()

    
if __name__ == '__main__':
    main()
