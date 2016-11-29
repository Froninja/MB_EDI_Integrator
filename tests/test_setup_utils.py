import os
import pytest
from src.helpers.config import SettingsException, check_config, write_config

class TestEmptyConfig(object):
    def test_empty_config(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "Could not locate the MAPDATA path. Please select a valid directory."
        )

    def teardown(self):
        os.remove("Config.yml")

class TestNoMapData(object):
    def setup(self):
        settings = {
            "File Paths": {
                "PO Database File": "test.sqlite"
            }
        }
        write_config(settings, "Config.yml")

    def test_no_mapdata(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.type) == "MAPDATA Path"

    def teardown(self):
        os.remove("Config.yml")

class TestInvalidMapData(object):
    def setup(self):
        settings = {
            "File Paths": {
                "PO Database File": "test.sqlite",
                "MAPDATA Path": "/bananas/"
            }
        }
        write_config(settings, "Config.yml")

    def test_invalid_mapdata(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "/bananas/ is not a valid directory. Please select a valid directory."
        )

    def teardown(self):
        os.remove("Config.yml")

class TestNoShipLog(object):
    def setup(self):
        settings = {
            "File Paths": {
                "PO Database File": "test.sqlite",
                "MAPDATA Path": "tests/"
            }
        }
        write_config(settings, "Config.yml")

    def test_no_ship_log(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "Could not locate the shipping information file. Please select a valid CSV file."
        )

    def teardown(self):
        os.remove("Config.yml")

class TestInvalidShipLog(object):
    def setup(self):
        settings = {
            "File Paths": {
                "PO Database File": "test.sqlite",
                "MAPDATA Path": "tests/",
                "Shipping Log": "test_ship_log.csv"
            }
        }
        write_config(settings, "Config.yml")

    def test_invalid_ship_log_path(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "test_ship_log.csv is not a valid file. Please select a valid CSV file."
        )

    def teardown(self):
        os.remove("Config.yml")

class TestShipLogBadFormat(object):
    def setup(self):
        write_invalid_ship_log()
        settings = {
            "File Paths": {
                "PO Database File": "test.sqlite",
                "MAPDATA Path": "tests/",
                "Shipping Log": "test_ship_log.csv"
            }
        }
        write_config(settings, "Config.yml")

    def test_invalid_ship_log_format(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "test_ship_log.csv is not in the expected format. Please select a valid file."
        )

    def teardown(self):
        os.remove("Config.yml")
        delete_ship_log()

class TestNoUpcLog(object):
    def setup(self):
        settings = {
            "File Paths": {
                "PO Database File": "test.sqlite",
                "MAPDATA Path": "tests/",
                "Shipping Log": "test_ship_log.csv"
            }
        }
        write_config(settings, "Config.yml")
        write_valid_ship_log()

    def test_no_upc_log(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "Could not locate the UPC exception file. Please select a valid CSV file."
        )

    def teardown(self):
        os.remove("Config.yml")
        delete_ship_log()

class TestInvalidUpcLog(object):
    def setup(self):
        settings = {
            "File Paths": {
                "PO Database File": "test.sqlite",
                "MAPDATA Path": "tests/",
                "Shipping Log": "test_ship_log.csv",
                "UPC Exception Log": "test_upc_log.csv"
            }
        }
        write_config(settings, "Config.yml")
        write_valid_ship_log()

    def test_invalid_upc_log_path(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "test_upc_log.csv is not a valid file. Please select a valid CSV file."
        )

    def teardown(self):
        os.remove("Config.yml")
        delete_ship_log()

class TestUpcLogBadFormat(object):
    def setup(self):
        write_valid_ship_log()
        write_invalid_upc_log()
        settings = {
            "File Paths": {
                "PO Database File": "test.sqlite",
                "MAPDATA Path": "tests/",
                "Shipping Log": "test_ship_log.csv",
                "UPC Exception Log": "test_upc_log.csv"
            }
        }
        write_config(settings, "Config.yml")

    def test_invalid_upc_log_format(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "test_upc_log.csv is not in the expected format. Please select a valid file."
        )

    def teardown(self):
        os.remove("Config.yml")
        delete_ship_log()
        delete_upc_log()

class TestNoDestLog(object):
    def setup(self):
        settings = {
            "File Paths": {
                "PO Database File": "test.sqlite",
                "MAPDATA Path": "tests/",
                "Shipping Log": "test_ship_log.csv",
                "UPC Exception Log": "test_upc_log.csv"
            }
        }
        write_config(settings, "Config.yml")
        write_valid_ship_log()
        write_valid_upc_log()

    def test_no_dest_log(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "Could not locate the destination and store file. Please select a valid txt file."
        )

    def teardown(self):
        os.remove("Config.yml")
        delete_ship_log()
        delete_upc_log()

class TestInvalidDestLog(object):
    def setup(self):
        settings = {
            "File Paths": {
                "PO Database File": "test.sqlite",
                "MAPDATA Path": "tests/",
                "Shipping Log": "test_ship_log.csv",
                "UPC Exception Log": "test_upc_log.csv",
                "Destination Log": "test_dest_log.txt"
            }
        }
        write_config(settings, "Config.yml")
        write_valid_ship_log()
        write_valid_upc_log()

    def test_invalid_dest_log_path(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "test_dest_log.txt is not a valid file. Please select a valid txt file."
        )

    def teardown(self):
        os.remove("Config.yml")
        delete_ship_log()
        delete_upc_log()

class TestDestLogBadFormat(object):
    def setup(self):
        write_valid_ship_log()
        write_valid_upc_log()
        write_invalid_dest_log()
        settings = {
            "File Paths": {
                "PO Database File": "test.sqlite",
                "MAPDATA Path": "tests/",
                "Shipping Log": "test_ship_log.csv",
                "UPC Exception Log": "test_upc_log.csv",
                "Destination Log": "test_dest_log.txt"
            }
        }
        write_config(settings, "Config.yml")

    def test_invalid_dest_log_format(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "test_dest_log.txt is not in the expected format. Please select a valid file."
        )

    def teardown(self):
        os.remove("Config.yml")
        delete_ship_log()
        delete_upc_log()
        delete_dest_log()

class TestValidConfig(object):
    def setup(self):
        write_valid_ship_log()
        write_valid_dest_log()
        write_valid_upc_log()
        settings = {
            "File Paths": {
                "PO Database File": "test.sqlite",
                "MAPDATA Path": "tests/",
                "Shipping Log": "test_ship_log.csv",
                "UPC Exception Log": "test_upc_log.csv",
                "Destination Log": "test_dest_log.txt"
            },
            "SQL Settings": {

            },
            "Customer Settings": {

            }
        }
        write_config(settings, "Config.yml")

    def test_valid_config(self):
        check_config("Config.yml")

    def teardown(self):
        os.remove("Config.yml")
        delete_ship_log()
        delete_upc_log()
        delete_dest_log()

class TestPoDbNoPath(object):
    def setup(self):
        settings = {
            "File Paths": {
                "MAPDATA Path": "tests/",
                "Shipping Log": "test_ship_log.csv",
                "UPC Exception Log": "test_upc_log.csv",
                "Destination Log": "test_dest_log.txt"
            },
            "SQL Settings": {

            },
            "Customer Settings": {

            }
        }
        write_config(settings, "Config.yml")
        write_valid_upc_log()
        write_valid_dest_log()
        write_valid_ship_log()

    def test_po_db_not_specified(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "Could not locate the order database file. Please select a valid Sqlite file."
        )

    def teardown(self):
        os.remove("Config.yml")
        delete_upc_log()
        delete_ship_log()
        delete_dest_log()

class TestPoDbInvalidPath(object):
    def setup(self):
        settings = {
            "File Paths": {
                "MAPDATA Path": "tests/",
                "Shipping Log": "test_ship_log.csv",
                "UPC Exception Log": "test_upc_log.csv",
                "Destination Log": "test_dest_log.txt",
                "PO Database File": "test.sqlite"
            },
            "SQL Settings": {

            },
            "Customer Settings": {

            }
        }
        write_config(settings, "Config.yml")
        write_valid_upc_log()
        write_valid_dest_log()
        write_valid_ship_log()

    def test_po_db_invalid_path(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "test.sqlite is not a valid file. Please select a valid Sqlite file"
        )

    def teardown(self):
        os.remove("Config.yml")
        delete_upc_log()
        delete_ship_log()
        delete_dest_log()

class TestPoDbNoTables(object):
    def setup(self):
        settings = {
            "File Paths": {
                "MAPDATA Path": "tests/",
                "Shipping Log": "test_ship_log.csv",
                "UPC Exception Log": "test_upc_log.csv",
                "Destination Log": "test_dest_log.txt",
                "PO Database File": "test.sqlite"
            },
            "SQL Settings": {

            },
            "Customer Settings": {

            }
        }
        write_config(settings, "Config.yml")
        write_valid_upc_log()
        write_valid_dest_log()
        write_valid_ship_log()
        write_invalid_po_db()

    def test_po_db_no_tables(self):
        with pytest.raises(SettingsException) as excinfo:
            check_config("Config.yml")
        assert str(excinfo.value.message) == (
            "test.sqlite is missing one or more"
            + " required tables. Create them now? (Warning: will overwrite"
            + " existing data)"
        )

    def teardown(self):
        os.remove("Config.yml")
        delete_upc_log()
        delete_ship_log()
        delete_dest_log()
        #delete_po_db()

def write_valid_ship_log():
    with open("test_ship_log.csv", 'w') as ship_log:
        ship_log.write("a, b, c, d, e, f, g, h, i, j")

def write_invalid_ship_log():
    with open("test_ship_log.csv", 'w') as ship_log:
        ship_log.write("a,b,c")

def write_valid_upc_log():
    with open("test_upc_log.csv", 'w') as upc_log:
        upc_log.write("cust, style, upc")

def write_invalid_upc_log():
    with open("test_upc_log.csv", 'w') as upc_log:
        upc_log.write("cust,style")

def write_valid_dest_log():
    with open("test_dest_log.txt", 'w') as dest_log:
        dest_log.write("cust;dest;store;dc;name")

def write_invalid_dest_log():
    with open("test_dest_log.txt", 'w') as dest_log:
        dest_log.write("cust;dest")

def write_invalid_po_db():
    with open("test.sqlite", 'w') as po_db:
        po_db.write("Oinkers")

def delete_ship_log():
    os.remove("test_ship_log.csv")

def delete_upc_log():
    os.remove("test_upc_log.csv")

def delete_dest_log():
    os.remove("test_dest_log.txt")

def delete_po_db():
    os.remove("test.sqlite")
