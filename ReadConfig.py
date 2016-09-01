from CustomerSettings import CustomerSettings
import yaml

def read_config(config_file):
    with open(config_file) as f:
        settings = yaml.load(f)
    return settings