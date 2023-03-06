"""
Allowing for an external configuration file
"""

import sys
import logging
from pathlib import Path
import configparser
from shutil import rmtree

logger = logging.getLogger(__name__)


class ConfigParser:
    """config_parser class for initialization and validation"""

    def __init__(self):
        """Initializing required values"""
        self.home_dir = Path.home()
        self.config_handler = configparser.ConfigParser()
        self.config_file = Path.joinpath(self.home_dir, ".sos_ansible.ini")

    def load_config(self):
        """Load config file from current user"""
        if Path.is_file(self.config_file):
            self.config_handler.read(self.config_file)
        else:
            self.config_handler.add_section("files")
            self.config_handler.set("files", "source", "/tmp/sosreports/")
            self.config_handler.set("files", "target", "/tmp")
            self.config_handler.set("files", "rules", "/tmp/rules.json")
            with open(self.config_file, "w", encoding="utf-8") as file:
                self.config_handler.write(file)
        return self.config_handler

    def clear_config(self):
        """Delete config file from current user"""
        try:
            rmtree(self.config_file)
        except Exception as error:  # pylint: disable=broad-except
            logger.error(error)
            sys.exit(f"Failure while deleting {self.config_file}: {error}")


def validator(config):
    """Validating basic fields"""
    if "files" not in config:
        logger.error("Invalid config file.")
        sys.exit("Invalid config file.")

    base_config = ["source", "target", "rules"]
    for items in base_config:
        try:
            config.get("files", items)
        except Exception as error:  # pylint: disable=broad-except
            logger.error("Invalid config file.\n %s", error)
