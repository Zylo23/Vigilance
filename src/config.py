from yaml import safe_load, dump


class Config:
    CONFIG_FILE = 'config.yaml'
    DEFAULT_CONFIG = {
        'hold_key': 'shift',
        'toggle_key': 'insert',
        'switch_mode_key': 'ctrl + tab',
        'increase_zone_key': 'ctrl + up',
        'decrease_zone_key': 'ctrl + down',
        'zone_size': 5,
        'modes': [
            {'name': '0.3s Delayer', 'delay': 0.3},
            {'name': '0.25s Delayer', 'delay': 0.25},
            {'name': '0.2s Delayer', 'delay': 0.2},
            {'name': '0.15s Delayer', 'delay': 0.15},
            {'name': '0.1s Delayer', 'delay': 0.1},
            {'name': 'No Delay Full-Auto', 'delay': 0},
        ]
    }

    @staticmethod
    def load_config() -> dict:
        try:
            with open(Config.CONFIG_FILE, 'r') as file:
                return safe_load(file)
        except FileNotFoundError:
            return Config.create_config()
        except Exception as e:
            print(f"Error loading config file: {e}")
            return Config.DEFAULT_CONFIG

    @staticmethod
    def create_config() -> dict:
        try:
            with open(Config.CONFIG_FILE, 'w') as file:
                dump(Config.DEFAULT_CONFIG, file)
            return Config.DEFAULT_CONFIG
        except Exception as e:
            print(f"Error creating config file: {e}")
            return Config.DEFAULT_CONFIG
