from yaml import safe_load, dump


class Config:
    @staticmethod
    def load_config() -> dict:
        try:
            with open('config.yaml', 'r') as file:
                return safe_load(file)
        except FileNotFoundError:
            return Config().create_config()
        
    @staticmethod
    def create_config() -> dict:
        with open('config.yaml', 'w') as file:
            config = {
                'hold_key': 'shift',
                'toggle_key': 'insert'
            }
            dump(config, file)
        return Config.load_config()
