from winsound import Beep
from mss import mss
from PIL import ImageGrab, Image
from ctypes import WinDLL
from time import perf_counter, sleep
from os import system
from keyboard import add_hotkey, is_pressed as is_key_pressed
from mouse import click, is_pressed as is_mouse_pressed
from colorama import Fore, Style
from version import __author__, __version__

S_HEIGHT, S_WIDTH = ImageGrab.grab().size
ZONE = 5
SWITCH_MODS_KEY = 'ctrl + tab'
MODES = [
    ('0.3s Delayer', 0.3),
    ('0.25s Delayer', 0.25),
    ('0.2s Delayer', 0.2),
    ('0.15s Delayer', 0.15),
    ('0.1s Delayer', 0.1),
    ('No Delay Full-Auto', 0),
]

user32 = WinDLL("user32", use_last_error=True)


class FoundEnemy(Exception):
    pass


class TriggerBot:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.is_running = True
        self.mode = 1
        self.last_reaction = 0
        self.setup_keys()
        self.print_state()
        Beep(500, 100)

    def setup_keys(self) -> None:
        add_hotkey(self.config['toggle_key'], self.toggle_state)
        add_hotkey(SWITCH_MODS_KEY, self.switch_mods, suppress=True)

    def toggle_state(self) -> None:
        self.is_running = not self.is_running
        if self.is_running:
            Beep(1000, 100)
            Beep(1000, 100)
        else:
            Beep(750, 100)
        self.print_state()

    def switch_mods(self) -> None:
        self.mode = (self.mode + 1) % len(MODES)
        Beep(1000, 100)
        self.print_state()

    def color_check(self, red: int, green: int, blue: int) -> bool:
        if green >= 0xAA:
            return False
        if green >= 0x78:
            return (abs(red - blue) <= 0x8 and
                    red - green >= 0x32 and
                    blue - green >= 0x32 and
                    red >= 0x69 and
                    blue >= 0x69)
        return abs(red - blue) <= 0xD and red - green >= 0x3C and blue - green >= 0x3C and red >= 0x6E and blue >= 0x64

    def grab(self) -> Image:
        with mss() as sct:
            bbox = (S_HEIGHT // 2 - ZONE, S_WIDTH // 2 - ZONE, S_HEIGHT // 2 + ZONE, S_WIDTH // 2 + ZONE)
            sct_img = sct.grab(bbox)
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

    def scan(self) -> None:
        start_time = perf_counter()
        pmap = self.grab()
        try:
            for x in range(0, ZONE * 2):
                for y in range(0, ZONE * 2):
                    r, g, b = pmap.getpixel((x, y))
                    if self.color_check(r, g, b):
                        raise FoundEnemy
        except FoundEnemy:
            self.last_reaction = int((perf_counter() - start_time) * 1000)
            if is_key_pressed('shift') or is_mouse_pressed():
                return
            click()
            sleep(MODES[self.mode][1])
            self.print_state()

    def print_state(self) -> None:
        status = 'Active' if self.is_running else 'Inactive'
        status_color = Fore.GREEN if self.is_running else Fore.RED
        state = (
            f"{Style.BRIGHT}{Fore.BLUE}Vigilance {__version__} | By {__author__}{Style.RESET_ALL}\n\n"
            f"{Style.BRIGHT}{Fore.GREEN}=== Controls{Style.RESET_ALL}\n"
            f"Trigger Key           : {Fore.CYAN}{self.config['toggle_key']}{Style.RESET_ALL}\n"
            f"Switch Mode Key       : {Fore.CYAN}{SWITCH_MODS_KEY}{Style.RESET_ALL}\n\n"
            f"{Style.BRIGHT}{Fore.GREEN}=== Status{Style.RESET_ALL}\n"
            f"Mode                  : {Fore.MAGENTA}{MODES[self.mode][0]}{Style.RESET_ALL}\n"
            f"Grab Zone             : {Fore.MAGENTA}{ZONE}x{ZONE}{Style.RESET_ALL}\n"
            f"Is Running            : {status_color}{status}{Style.RESET_ALL}\n"
            f"Last Reaction         : {Fore.MAGENTA}{self.last_reaction} ms"
            f"({self.last_reaction / (ZONE * ZONE):.2f} ms/pix){Style.RESET_ALL}\n"
        )
        system('cls')
        print(state)

    def run(self) -> None:
        while True:
            if self.is_running:
                self.scan()
            sleep(0.01)
