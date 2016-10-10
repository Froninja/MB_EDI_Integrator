import yaml

def read_config(config_file):
    with open(config_file) as file:
        settings = yaml.load(file)
    return settings
