import json

config_path = "/home/pi/Hexi/hexi/config/config.json"

def load():
    with open(config_path, "r") as config_file:
        config_data = json.load(config_file)

    return config_data


def save(new_config):
    with open(config_path, "w") as config_file:
        json.dump(new_config, config_file)

