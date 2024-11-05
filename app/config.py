import os
import yaml
from dotenv import load_dotenv


class Config:
    def __init__(self, config_file=None, debug=False):
        current_dir = os.path.dirname(__file__)
        if debug:
            default_config_file = os.path.join(current_dir, "config_debug.yaml")
        else:
            default_config_file = os.path.join(current_dir, "config.yaml")
        load_dotenv()
        self.config_file = config_file if config_file else default_config_file
        self.config = self.load_config()
        self.interpolate_config()

    def load_config(self):
        with open(self.config_file, "r") as file:
            return yaml.safe_load(file)

    def interpolate_config(self):
        for section, settings in self.config.items():
            for key, value in settings.items():
                if (
                    isinstance(value, str)
                    and value.startswith("${")
                    and value.endswith("}")
                ):
                    env_var = value[2:-1]
                    self.config[section][key] = os.getenv(env_var)

    def get(self, section, key):
        return self.config.get(section, {}).get(key)
