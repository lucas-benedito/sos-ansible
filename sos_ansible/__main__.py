#!/usr/bin/env python
"""
sos_ansible, main program
"""

import argparse
import os
import sys
import logging.config as loggerconf
from logging import getLogger
import inquirer
from sos_ansible.modules.file_handling import (
    validate_out_dir,
    data_input,
    rules_processing,
)
from sos_ansible.modules.config_manager import ConfigParser, validator

# Setting up local settings
config = ConfigParser()
config.setup()
validator(config.config_handler)

# Setting up Logger
loggerconf.fileConfig(config.config_file)
logger = getLogger("root")


# Processing user input for directory choice
def get_user_input(sos_directory):
    """Select work directory"""
    choice = os.listdir(sos_directory)
    try:
        questions = [
            inquirer.List("case", message="Choose the sos directory", choices=choice),
        ]
    except TypeError:
        logger.critical("Cancelled by user.")
        sys.exit(1)
    return inquirer.prompt(questions)["case"]


def main():
    """
    Main function from sos_ansible. This will process all steps for sosreports reading
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        help="Directory containing sosreports",
        required=False,
        default="",
    )
    parser.add_argument(
        "-r",
        "--rules",
        type=str,
        help="Rules file with full path",
        required=False,
        default="",
    )
    parser.add_argument(
        "-c",
        "--case",
        type=str,
        help="Directory number to which the sosreport was extracted",
        required=False,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug message logging",
        required=False,
        default=False,
    )
    params = parser.parse_args()

    if params.directory:
        sos_directory = os.path.abspath(params.directory)
    else:
        sos_directory = os.path.abspath(
            os.path.expanduser(config.config_handler.get("files", "source"))
        )
    if params.rules:
        rules_file = os.path.expanduser(params.rules)
    else:
        rules_file = os.path.expanduser(config.config_handler.get("files", "rules"))

    # In order to allow both container and standard command line usage must check for env
    try:
        if os.environ["IS_CONTAINER"]:
            if not params.case:
                logger.error("A case number must be used if running from a container")
                sys.exit("A case number must be used if running from a container")
    except KeyError:
        pass

    # if case number is not provided prompt if provided just use it
    if os.path.isdir(sos_directory) and not params.case:
        user_choice = get_user_input(sos_directory)
    elif os.path.isdir(sos_directory) and params.case:
        user_choice = params.case
    else:
        logger.error(
            "The selected directory %s doesn't exist."
            "Select a new directory and try again.",
            sos_directory,
        )
        sys.exit(1)

    node_data, curr_policy = data_input(sos_directory, rules_file, user_choice)
    if not node_data:
        logger.critical(
            "No sosreports found, please review the directory %s", sos_directory
        )
        sys.exit(0)
    logger.debug("Node data: %s", node_data)
    logger.debug("Current policy: %s", curr_policy)

    validate_out_dir(user_choice)

    rules_processing(node_data, curr_policy, user_choice, params.debug)

    logger.critical(
        "Read the matches at %s/%s",
        config.config_handler.get("files", "target"),
        user_choice,
    )
    logger.critical("SOS_ANSIBLE - END")


if __name__ == "__main__":
    main()
