from yaml import safe_load, dump


class Config:
    CONFIG_FILE = 'config.yaml'
    DEFAULT_CONFIG = {
        'hold_key': 'shift',
        'toggle_key': 'insert'
    }
    
    @staticmethod
    def load_config() -> dict:
        try:
            with open(Config.CONFIG_FILE, 'r') as file:
                return safe_load(file) or Config.create_config()
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
