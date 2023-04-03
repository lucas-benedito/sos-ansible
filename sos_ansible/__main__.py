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
def get_user_input(sos_directory):
    """Select work directory"""
    if os.path.isdir(sos_directory):
        choice = os.listdir(sos_directory)
        try:
            questions = [
                inquirer.List(
                    "case", message="Choose the sos directory", choices=choice
                ),
            ]

        except TypeError:
            logger.critical("Cancelled by user.")
            sys.exit()
    else:
        logger.critical(
            "The SOS directory provided could not be found. Select another path and try again"
        )
        raise SystemExit
    if questions:
        case = inquirer.prompt(questions)["case"]
    return case


def main():
    """
    Main function from sos_ansible. This will process all steps for sosreports reading
    """

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
        expand_sosreport(params.tarball, params.case)
    # In order to allow both container and standard command line usage must check for env
    try:
        if os.environ["IS_CONTAINER"] and not params.case:
            logger.critical("A case number must be used if running from a container")
            raise SystemExit
    except KeyError:
        pass

    # if case number is not provided prompt if provided just use it
    if params.case:
        user_choice = params.case
    else:
        user_choice = get_user_input(sos_directory)

    node_data, curr_policy = data_input(sos_directory, rules_file, user_choice)
    logger.debug("Node Data: %s, Current Policy: %s", node_data, curr_policy)

    try:
        if node_data or curr_policy:
            logger.debug("Node data: %s", node_data)
            logger.debug("Current policy: %s", curr_policy)
            tgt_dir = os.path.expanduser(config.config_handler.get("files", "target"))
            validate_out_dir(user_choice, tgt_dir)
            rules_processing(node_data, curr_policy, user_choice, params.debug)
            logger.critical(
                "Read the matches at %s/%s",
                config.config_handler.get("files", "target"),
                user_choice,
            )
    except UnboundLocalError:
        node_data = []
        curr_policy = {}
        if not node_data:
            logger.critical(
                "No sosreports found, please review the directory %s", sos_directory
            )
        if not curr_policy:
            logger.critical(
                "No rules file found, please review the directory %s", rules_file
            )

    print("")
    logger.critical("SOS_ANSIBLE - END")


if __name__ == "__main__":
    main()
