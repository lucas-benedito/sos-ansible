"""
Allowing for an external configuration file
"""

import sys
import os
import configparser
import logging.config
from shutil import rmtree


class ConfigParser:
    """config_parser class for initialization and validation"""

    def __init__(self, home_dir=os.path.expanduser("~"), tgt_file=".sos_ansible.ini"):
        """Initializing required values"""
        self.home_dir = home_dir
        self.tgt_file = tgt_file
        self.config_file = os.path.join(self.home_dir, self.tgt_file)
        self.config_handler = configparser.ConfigParser()

    def setup(self):
        """Setting up config files"""
        if os.path.isfile(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as file:
                self.config_handler.read_file(file)
        else:
            try:
                self.set_files_config()
            except Exception as err:  # pylint: disable=broad-except
                print(err)
        self.set_logger_config()

    def set_files_config(self):
        """Load config for local files"""
        if "files" not in self.config_handler:
            self.config_handler.add_section("files")
            self.config_handler.set("files", "source", "/tmp/sosreports")
            self.config_handler.set("files", "target", "/tmp")
            self.config_handler.set("files", "rules", "/tmp/rules.json")
        with open(self.config_file, "a", encoding="utf-8") as file:
            self.config_handler.write(file)

    def set_logger_config(self):
        """Load config for the loggers"""
        logging_config = {
            "version": 1,
            "formatters": {
                "sos_ansible": {"format": "%(message)s"},
                "sos_ansible_asctime": {
                    "format": "%(asctime)s %(levelname)s %(message)s"
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "sos_ansible",
                    "level": "CRITICAL",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "formatter": "sos_ansible_asctime",
                    "filename": "sos-ansible.log",
                    "level": "DEBUG",
                    "mode": "a",
                },
            },
            "root": {"level": "DEBUG", "handlers": ["console", "file"]},
        }

        if "logging" in self.config_handler:
            for key in self.config_handler["logging"]:
                logging_config[key] = self.config_handler["logging"][key]

        logging.config.dictConfig(logging_config)

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
        print(config.sections())
        sys.exit("Invalid config file.")

    base_config = ["source", "target", "rules"]
    for items in base_config:
        try:
            config.get("files", items)
        except Exception as error:  # pylint: disable=broad-except
            print(error)
