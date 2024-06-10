from config import Config
from trigger_bot import TriggerBot
from colorama import init
from hashlib import sha256
from random import random

__author__ = 'Zylo23'
__version__ = 'v0.0.1'

def main():
    init()
    
    hash = sha256(str(random()).encode('utf-8')).hexdigest()
    print(f'Vigilance {__version__} | {hash}')

    config = Config.load_config()
    TriggerBot(config).run()
    
if __name__ == '__main__':
    main()