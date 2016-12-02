"""Module for functions relating to app settings reading, writing, and validation"""
from os import path
import csv
import yaml
from src.db.db import get_engine

def read_config(config_file):
    """Reads a config file in YAML format and returns a settings dictionary"""
    with open(config_file) as file:
        settings = yaml.load(file)
    return settings

def write_config(settings, config_file):
    """Writes a settings dictionary in YAML format to file"""
    with open(config_file, 'w') as file:
        yaml.dump(settings, file, default_flow_style=False)

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
    settings = dict()
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
    if not "MAPDATA Path" in file_settings:
        raise SettingsException(file_settings, "MAPDATA Path", "Could not locate the MAPDATA path."
                                + " Please select a valid directory.")
    validate_mapdata_path(file_settings)

    if not "Shipping Log" in file_settings:
        raise SettingsException(file_settings, "Shipping Log", "Could not locate the shipping"
                                + " information file. Please select a valid CSV file.")
    validate_shipping_log(file_settings)

    if not "UPC Exception Log" in file_settings:
        raise SettingsException(file_settings, "UPC Exception Log", "Could not locate the UPC"
                                + " exception file. Please select a valid CSV file.")
    validate_upc_log(file_settings)

    if not "Destination Log" in file_settings:
        raise SettingsException(file_settings, "Destination Log", "Could not locate the"
                                + " destination and store file. Please select a valid txt file.")
    validate_destination_log(file_settings)

    if not "PO Database File" in file_settings:
        raise SettingsException(file_settings, "PO Database File", "Could not locate the order"
                                + " database file. Please select a valid Sqlite file.")
    validate_po_db(file_settings)

def validate_po_db(file_settings):
    """Confirms that the path is a valid Sqlite database and has the required tables (or
    creates them)"""
    if not path.isfile(file_settings["PO Database File"]):
        raise SettingsException(file_settings, "PO Database File",
                                str(file_settings["PO Database File"]) + " is not a valid file."
                                + " Please select a valid Sqlite file")
    eng = get_engine(file_settings["PO Database File"])

    #Raise an error if specified databse lacks any needed table
    if not (eng.has_table("Orders") and
            eng.has_table("Stores") and
            eng.has_table("Items") and
            eng.has_table("Invoices")):
        raise SettingsException(file_settings, "PO Database File",
                                str(file_settings["PO Database File"]) + " is missing one or more"
                                + " required tables. Create them now? (Warning: will overwrite"
                                + " existing data)")

def validate_mapdata_path(file_settings):
    """Confirms that the path is a valid directory"""
    if not path.isdir(file_settings["MAPDATA Path"]):
        raise SettingsException(file_settings, "MAPDATA Path", str(file_settings["MAPDATA Path"])
                                + " is not a valid directory. Please select a valid directory.")

def validate_shipping_log(file_settings):
    """Confirms that the path is a valid CSV file with the expected format"""
    if not path.isfile(file_settings["Shipping Log"]):
        raise SettingsException(file_settings, "Shipping Log", str(file_settings["Shipping Log"])
                                + " is not a valid file. Please select a valid CSV file.")
    else:
        with open(file_settings["Shipping Log"]) as shipping_log:
            reader = csv.reader(shipping_log)
            for line in reader:
                last = line
            if not len(last) >= 10:
                raise SettingsException(file_settings, "Shipping Log",
                                        str(file_settings["Shipping Log"]) + " is not in the"
                                        + " expected format. Please select a valid file.")

def validate_upc_log(file_settings):
    """Confirms that the path is a valid CSV file with the expected format"""
    if not path.isfile(file_settings["UPC Exception Log"]):
        raise SettingsException(file_settings, "UPC Exception Log",
                                str(file_settings["UPC Exception Log"]) + " is not a valid file."
                                + " Please select a valid CSV file.")
    else:
        with open(file_settings["UPC Exception Log"]) as upc_log:
            reader = csv.reader(upc_log)
            for line in reader:
                last = line
            if not len(last) >= 3:
                raise SettingsException(file_settings, "UPC Exception Log",
                                        str(file_settings["UPC Exception Log"]) + " is not in the"
                                        + " expected format. Please select a valid file.")

def validate_destination_log(file_settings):
    """Confirms that the path is a valid TXT file with the expected format"""
    if not path.isfile(file_settings["Destination Log"]):
        raise SettingsException(file_settings, "Destination Log",
                                str(file_settings["Destination Log"]) + " is not a valid file."
                                + " Please select a valid txt file.")
    else:
        with open(file_settings["Destination Log"]) as dest_log:
            reader = csv.reader(dest_log, delimiter=';')
            for line in reader:
                last = line
            if not len(last) >= 5:
                raise SettingsException(file_settings, "Destination Log",
                                        str(file_settings["Destination Log"]) + " is not in the"
                                        + " expected format. Please select a valid file.")

class SettingsException(Exception):
    """For use when a setting is invalid or missing"""
    def __init__(self, settings, settings_type, message):
        Exception.__init__(self)
        self.settings = settings
        self.type = settings_type
        self.message = message
