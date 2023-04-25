#!/usr/bin/env python
"""
sos_ansible, main program
"""
import os
import sys
from logging import getLogger
import inquirer
from sos_ansible.modules.file_handling import (
    validate_out_dir,
    data_input,
    rules_processing,
    expand_sosreport,
)
from sos_ansible.modules.parsing import Parser
from sos_ansible.modules.config_manager import ConfigParser

# Setting up local settings
config = ConfigParser()
config.setup()

# Setting up Logger
logger = getLogger("root")


# Processing user input for directory choice
def get_user_input(sos_directory: os.path) -> str:
    """
    Select work directory

    :params os.path sos_directory: Directory containing the sosreports
    :return str
    """
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
    tgt_dir = os.path.join(
        os.path.expanduser(config.config_handler.get("files", "target"))
    )

    params = Parser.get_args()
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
    if params.tarball:
        expand_sosreport(params.tarball, params.case, sos_directory)
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
        logger.critical(
            "The selected directory %s doesn't exist."
            " Select a new directory and try again.",
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

    validate_out_dir(user_choice, tgt_dir)

    rules_processing(node_data, curr_policy, user_choice, params.debug, tgt_dir)

    logger.critical(
        "Read the matches at %s/%s",
        config.config_handler.get("files", "target"),
        user_choice,
    )
    logger.critical("SOS_ANSIBLE - END")


if __name__ == "__main__":
    main()
