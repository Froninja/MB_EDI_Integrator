"""Module for functions relating to app settings reading, writing, and validation"""
from os import path
import yaml

def read_config(config_file):
    """Reads a config file in YAML format and returns a settings dictionary"""
    with open(config_file) as file:
        settings = yaml.load(file)
    return settings

def check_config(config_file):
    """Checks for a config file at the given path and creates a new one if not present"""
    if not path.isfile(config_file):
        create_config(config_file)
    else:
        settings = read_config(config_file)
        validate_config(settings)

def create_config(config_file):
    """Creates an empty configuration file and runs the validation to confirm all settings
    are present"""
    open(config_file, 'w')
    settings = read_config(config_file)
    validate_config(settings)

def validate_config(settings):
    """Validates a settings dictionary for required values and makes sure they are in the
    proper format"""
    if not "File Paths" in settings:
        settings["File Paths"] = dict()
    validate_file_paths(settings["File Paths"])

    if not "SQL Settings" in settings:
        raise NotImplementedError()
    if not "Customer Settings" in settings:
        raise NotImplementedError()
    if not "Statuses" in settings:
        settings["Statuses"] = ['']

def validate_file_paths(file_settings):
    """Validates the file paths portion of the settings dictionary"""
    if not "PO Database File" in file_settings:
        raise SettingsException(file_settings, "PO Database File", "Could not locate the order"
                                + " database file. Please select a valid file Sqlite file.")
    elif not "MAPDATA Path" in file_settings:
        raise SettingsException(file_settings, "MAPDATA Path", "Could not locate the MAPDATA path."
                                + " Please select a valid directory.")
    elif not "Shipping Log" in file_settings:
        raise SettingsException(file_settings, "Shipping Log", "Could not locate the shipping"
                                + " information file. Please select a valid CSV file.")
    elif not "UPC Exception Log" in file_settings:
        raise SettingsException(file_settings, "UPC Exception Log", "Could not locate the UPC"
                                + " exception file. Please select a valid CSV file.")
    elif not "Destination Log" in file_settings:
        raise SettingsException(file_settings, "Destination Log", "Could not locate the"
                                + " destination and store file. Please select a valid CSV file.")

class SettingsException(Exception):
    def __init__(self, settings, settings_type, message):
        self.settings = settings
        self.type = settings_type
        self.message = message
