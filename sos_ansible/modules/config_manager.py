"""
Allowing for an external configuration file
"""

import sys
from pathlib import Path
import configparser
from shutil import rmtree


class ConfigParser:
    """config_parser class for initialization and validation"""

    def __init__(self):
        """Initializing required values"""
        self.home_dir = Path.home()
        self.config_handler = configparser.ConfigParser()
        self.config_file = Path.joinpath(self.home_dir, ".sos_ansible.ini")
        print("Initiated")

    def setup(self):
        """Setting up config files"""
        if Path.is_file(self.config_file):
            self.config_handler.read(self.config_file)
        else:
            self.set_config()
        print("Setup")

    def set_config(self):
        """Load config for the loggers"""
        try:
            self.config_handler.add_section("files")
            self.config_handler.set("files", "source", "/tmp/sosreports/")
            self.config_handler.set("files", "target", "/tmp")
            self.config_handler.set("files", "rules", "/tmp/rules.json")
        except configparser.DuplicateSectionError:
            print("Files section already exists")
        except Exception as error:  # pylint: disable=broad-except
            sys.exit(error)

        try:
            self.config_handler.add_section("loggers")
            self.config_handler.set("loggers", "keys", "root")
            self.config_handler.add_section("handlers")
            self.config_handler.set("handlers", "keys", "console, file")
            self.config_handler.add_section("formatters")
            self.config_handler.set(
                "formatters", "keys", "sos_ansible, sos_ansible_asctime"
            )
            self.config_handler.add_section("logger_root")
            self.config_handler.set("logger_root", "level", "DEBUG")
            self.config_handler.set("logger_root", "handlers", "console,file")
            self.config_handler.add_section("handler_console")
            self.config_handler.set("handler_console", "class", "StreamHandler")
            self.config_handler.set("handler_console", "level", "INFO")
            self.config_handler.set("handler_console", "formatter", "sos_ansible")
            self.config_handler.set("handler_console", "args", "(sys.stdout,)")
            self.config_handler.add_section("handler_file")
            self.config_handler.set("handler_file", "class", "FileHandler")
            self.config_handler.set("handler_file", "level", "DEBUG")
            self.config_handler.set("handler_file", "formatter", "sos_ansible_asctime")
            self.config_handler.set("handler_file", "args", "('sos-ansible.log', 'a')")
            self.config_handler.add_section("formatter_sos_ansible")
            self.config_handler.set(
                "formatter_sos_ansible", "format", "%(levelname)s:%(message)s"
            )
            self.config_handler.set("formatter_sos_ansible", "datefmt", "")
            self.config_handler.set("formatter_sos_ansible", "style", "%%")
            self.config_handler.set("formatter_sos_ansible", "validate", "True")
            self.config_handler.set(
                "formatter_sos_ansible", "class", "logging.Formatter"
            )
            self.config_handler.add_section("formatter_sos_ansible_asctime")
            self.config_handler.set(
                "formatter_sos_ansible_asctime",
                "format",
                "%(asctime)s %(levelname)s %(message)s",
            )
            self.config_handler.set("formatter_sos_ansible_asctime", "datefmt", "")
            self.config_handler.set("formatter_sos_ansible_asctime", "style", "%%")
            self.config_handler.set("formatter_sos_ansible_asctime", "validate", "True")
            self.config_handler.set(
                "formatter_sos_ansible_asctime", "class", "logging.Formatter"
            )
        except configparser.DuplicateSectionError:
            print("Loggers section already exists")
        except Exception as error:  # pylint: disable=broad-except
            sys.exit(error)

        with open(self.config_file, "a", encoding="utf-8") as file:
            self.config_handler.write(file)

    def clear_config(self):
        """Delete config file from current user"""
        try:
            rmtree(self.config_file)
        except Exception as error:  # pylint: disable=broad-except
            # logger.error(error)
            sys.exit(f"Failure while deleting {self.config_file}: {error}")


def validator(config):
    """Validating basic fields"""
    if "files" not in config:
        # logger.error("Invalid config file.")
        sys.exit("Invalid config file.")

    base_config = ["source", "target", "rules"]
    for items in base_config:
        try:
            config.get("files", items)
        except Exception as error:  # pylint: disable=broad-except
            # logger.error("Invalid config file.\n %s", error)
            print(error)
