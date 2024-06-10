from main import __version__, __author__

from winsound import Beep
from mss import mss
from PIL import ImageGrab, Image
from ctypes import WinDLL
from time import perf_counter, sleep
from os import system
from keyboard import add_hotkey, is_pressed as is_key_pressed
from mouse import click, is_pressed as is_mouse_pressed
from colorama import Fore, Style

S_HEIGHT, S_WIDTH = ImageGrab.grab().size
ZONE = 5
SWITCH_MODS_KEY = 'ctrl + tab'
MODES = ('0.3s Delayer', '0.25s Delayer', '0.2s Delayer', '0.15s Delayer', '0.1s Delayer', 'No Delay Full-Auto')

user32 = WinDLL("user32", use_last_error=True)

class TriggerBot:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.is_running = True
        self.mode = 1
        self.last_reaction = 0
        self.setup_keys()
        self.print_state()
        Beep(750, 100)

    def setup_keys(self) -> None:
        add_hotkey(self.config['toggle_key'], self.toggle_state)
        add_hotkey(SWITCH_MODS_KEY, self.switch_mods, suppress=True)

    def toggle_state(self) -> None:
        self.is_running = not self.is_running
        if self.is_running:
            Beep(1000, 100)
            Beep(1000, 100)
        else:
            Beep(500, 100)
        self.print_state()            

    def switch_mods(self) -> None:
        self.mode = (self.mode + 1) % len(MODES)
        Beep(1000, 100)
        self.print_state()

    def color_check(self, red: int, green: int, blue: int) -> bool:
        if green >= 0xAA: return False
        if green >= 0x78: return abs(red - blue) <= 0x8 and red - green >= 0x32 and blue - green >= 0x32 and red >= 0x69 and blue >= 0x69
        
        return abs(red - blue) <= 0xD and red - green >= 0x3C and blue - green >= 0x3C and red >= 0x6E and blue >= 0x64

    def grab(self) -> Image:
        with mss() as sct:
            bbox = (int(S_HEIGHT / 2 - ZONE), int(S_WIDTH / 2 - ZONE), int(S_HEIGHT / 2 + ZONE), int(S_WIDTH / 2 + ZONE))
            sct_img = sct.grab(bbox)
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

    def scan(self) -> None:
        start_time = perf_counter()
        pmap = self.grab()

        for x in range(0, ZONE * 2):
            for y in range(0, ZONE * 2):
                r, g, b = pmap.getpixel((x, y))
                if self.color_check(r, g, b):
                    self.last_reaction = int((perf_counter() - start_time) * 1000)
                    if is_key_pressed('shift') or is_mouse_pressed():
                        return
                    click()
                    if self.mode < len(MODES) - 1:
                        sleep(float(MODES[self.mode].split('s')[0]))
                    self.print_state()
                    break

    def print_state(self) -> None:
        s = f"{Style.BRIGHT}{Fore.BLUE}Vigilance {__version__} | By {__author__}{Style.RESET_ALL}\n"
        s += f"{Style.BRIGHT}{Fore.GREEN}=== Controls{Style.RESET_ALL}\n"
        s += f"Trigger Key           : {Fore.CYAN}{self.config['toggle_key']}{Style.RESET_ALL}\n"
        s += f"Switch Mode Key       : {Fore.CYAN}{SWITCH_MODS_KEY}{Style.RESET_ALL}\n\n"
        s += f"{Style.BRIGHT}{Fore.GREEN}=== Status{Style.RESET_ALL}\n"
        s += f"Mode                  : {Fore.MAGENTA}{MODES[self.mode]}{Style.RESET_ALL}\n"
        s += f"Grab Zone             : {Fore.MAGENTA}{ZONE}x{ZONE}{Style.RESET_ALL}\n"
        s += f"Is Running            : {Fore.GREEN if self.is_running else Fore.RED}{'Active' if self.is_running else 'Inactive'}{Style.RESET_ALL}\n"
        s += f"Last Reaction         : {Fore.MAGENTA}{self.last_reaction} ms ({self.last_reaction / (ZONE * ZONE):.2f} ms/pix){Style.RESET_ALL}\n"
        system('cls')
        print(s)
        
    def run(self) -> None:
        while True:
            if self.is_running:
                self.scan()
            sleep(0.01)