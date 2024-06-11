import winsound
import keyboard
import mouse
import mss
from typing import List
from ctypes import WinDLL
from PIL import ImageGrab
from time import perf_counter, sleep
from os import system
from colorama import Fore, Style
from version import __author__, __version__

# Constants
S_HEIGHT, S_WIDTH = ImageGrab.grab().size
user32 = WinDLL("user32", use_last_error=True)


class FoundEnemy(Exception):
    pass


class TriggerBot:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.is_running: bool = True
        self.mode: int = 0
        self.last_reaction: int = 0
        self.zone: int = config['zone_size']
        self.modes = [(mode['name'], mode['delay']) for mode in config['modes']]
        self.setup_keys()
        self.print_state()
        winsound.Beep(500, 100)

    def setup_keys(self) -> None:
        keyboard.add_hotkey(self.config['toggle_key'], self.toggle_state)
        keyboard.add_hotkey(self.config['switch_mode_key'], self.switch_mods, suppress=True)
        keyboard.add_hotkey(self.config['increase_zone_key'], self.increase_zone, suppress=True)
        keyboard.add_hotkey(self.config['decrease_zone_key'], self.decrease_zone, suppress=True)

    def toggle_state(self) -> None:
        self.is_running = not self.is_running
        if self.is_running:
            winsound.Beep(1000, 100)
            winsound.Beep(1000, 100)
        else:
            winsound.Beep(750, 100)
        self.print_state()
        
    def switch_mods(self) -> None:
        self.mode = (self.mode + 1) % len(self.modes)
        winsound.Beep(1000, 100)
        self.print_state()
        
    def increase_zone(self) -> None:
        self.zone = min(self.zone + 1, 10)  # Arbitrary upper limit to avoid excessive zone size
        winsound.Beep(1500, 100)
        self.print_state()

    def decrease_zone(self) -> None:
        self.zone = max(self.zone - 1, 1)  # Lower limit to ensure zone is always positive
        winsound.Beep(1000, 100)
        self.print_state()

    def color_check(self, r: int, g: int, b: int) -> bool:
        if g >= 0xAA:
            return False
        if g >= 0x78:
            return (abs(r - b) <= 0x8 and (r - g) >= 0x32 and (b - g) >= 0x32 and r >= 0x69 and b >= 0x69)
        return (abs(r - b) <= 0xD and (r - g) >= 0x3C and (b - g) >= 0x3C and r >= 0x6E and b >= 0x64)

    def grab(self) -> List[int]:
        with mss.mss() as sct:
            monitor = (S_HEIGHT // 2 - self.zone,
                       S_WIDTH // 2 - self.zone,
                       S_HEIGHT // 2 + self.zone,
                       S_WIDTH // 2 + self.zone)
            sct_img = sct.grab(monitor)
            return sct_img.rgb

    def scan(self) -> None:
        start_time: float = perf_counter()
        rgb_pixels = self.grab()
        try:
            for i in range(0, len(rgb_pixels), 3):
                r, g, b = rgb_pixels[i], rgb_pixels[i + 1], rgb_pixels[i + 2]
                if self.color_check(r, g, b):
                    raise FoundEnemy
        except FoundEnemy:
            self.last_reaction = int((perf_counter() - start_time) * 1000)
            if keyboard.is_pressed(self.config['hold_key']) or mouse.is_pressed():
                return
            mouse.click()
            sleep(self.modes[self.mode][1])
            self.print_state()

    def print_state(self) -> None:
        status: str = 'Active' if self.is_running else 'Inactive'
        status_color: str = Fore.GREEN if self.is_running else Fore.RED
        state: str = (
            f"{Style.BRIGHT}{Fore.BLUE}Vigilance {__version__} | By {__author__}{Style.RESET_ALL}\n\n"
            f"{Style.BRIGHT}{Fore.GREEN}=== Controls{Style.RESET_ALL}\n"
            f"Trigger Key           : {Fore.CYAN}{self.config['toggle_key']}{Style.RESET_ALL}\n"
            f"Switch Mode Key       : {Fore.CYAN}{self.config['switch_mode_key']}{Style.RESET_ALL}\n"
            f"Increase Zone Key     : {Fore.CYAN}{self.config['increase_zone_key']}{Style.RESET_ALL}\n"
            f"Decrease Zone Key     : {Fore.CYAN}{self.config['decrease_zone_key']}{Style.RESET_ALL}\n\n"
            f"{Style.BRIGHT}{Fore.GREEN}=== Status{Style.RESET_ALL}\n"
            f"Mode                  : {Fore.MAGENTA}{self.modes[self.mode][0]}{Style.RESET_ALL}\n"
            f"Grab Zone             : {Fore.MAGENTA}{self.zone}x{self.zone}{Style.RESET_ALL}\n"
            f"Is Running            : {status_color}{status}{Style.RESET_ALL}\n"
            f"Last Reaction         : {Fore.MAGENTA}{self.last_reaction} ms"
            f" ({self.last_reaction / (self.zone * self.zone):.2f} ms/pix){Style.RESET_ALL}\n"
        )
        system('cls')
        print(state)

    def run(self) -> None:
        while True:
            if self.is_running:
                self.scan()
            sleep(0.01)
