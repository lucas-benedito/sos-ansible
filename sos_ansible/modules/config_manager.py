"""
Allowing for an external configuration file
"""

from pathlib import Path
import configparser

home_dir = Path.home()
config_handler = configparser.ConfigParser()
config_file = Path.joinpath(home_dir, ".sos_ansible.ini")


def load_config():
    """Load config file from current user"""
    if Path.is_file(config_file):
        config_handler.read(config_file)
    else:
        config_handler.add_section("files")
        config_handler.set("files", "source", "/tmp/sosreports/")
        config_handler.set("files", "target", "/tmp")
        config_handler.set("files", "rules", "/tmp/rules.json")
        with open(config_file, "w", encoding="utf-8") as file:
            config_handler.write(file)
    return config_handler
