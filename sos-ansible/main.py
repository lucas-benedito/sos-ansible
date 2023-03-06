#!/usr/bin/env python
"""
sos_ansible, main program
"""

import argparse
import json
import os
import sys
import inquirer
from logging import config, getLogger
from modules.file_handling import read_policy, process_rule, validate_tgt_dir
from modules.locating_sos import LocateReports

SOS_DIRECTORY = os.path.abspath("/tmp/test_sosreport/")
RULES_FILE = os.path.abspath("/tmp/rules/rules.json")
LOGGING_CONFIG = os.path.dirname(__file__) + "/config/" + "logging.json"

with open(LOGGING_CONFIG) as f:
    config.dictConfig(json.load(f))
logger = getLogger(__name__)


def get_user_input(sos_directory):
    """Select workdir"""
    choice = os.listdir(sos_directory)
    questions = [
        inquirer.List("case", message="Choose the sos directory", choices=choice),
    ]
    return inquirer.prompt(questions)["case"]


def data_input(sos_directory, rules_file, user_choice):
    """
    Load the external sosreport and policy rules
    """
    logger.info("Validating sosreports on target directory: %s", sos_directory)
    report_data = LocateReports()
    node_data = report_data.run({sos_directory}, user_choice)
    logger.info("Validating rules in place: %s", rules_file)
    curr_policy = read_policy(rules_file)
    return node_data, curr_policy


def rules_processing(node_data, curr_policy, user_choice, debug):
    """
    Read the rules.json file and load it on the file_handling modules for processing.
    """
    for hosts in node_data:
        hostname = hosts["hostname"]
        path = hosts["path"]
        analysis_summary = f"Summary\n{hostname}:\n--------\nController Node: {hosts['controller']}\n--------\n"
        match_count = int()
        logger.info("Processing node %s:", hostname)
        for rules in curr_policy:
            iterator = curr_policy[rules]
            for files in iterator["files"]:
                to_read = f"{path}/{iterator['path']}/{files}"
                query = iterator["query"].replace(", ", "|")
                result_count = process_rule(hostname, user_choice, rules, to_read, query)
                match_count += result_count
                if debug:
                    logger.debug("Rule:\"{}\",Source:\"{}\",Query:\"{}\",Result:\"{}\"".format(
                        rules, to_read, query, result_count))
            analysis_summary += f"{rules}: {match_count}\n"
        logger.info(analysis_summary)


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
        "--debug",
        action="store_true",
        help="Enable debug message logging",
        required=False,
        default=False,
    )
    params = parser.parse_args()
    if params.directory:
        sos_directory = params.directory
    else:
        sos_directory = SOS_DIRECTORY
    if params.rules:
        rules_file = os.path.abspath(params.rules)
    else:
        rules_file = RULES_FILE

    if os.path.isdir(sos_directory):
        user_choice = get_user_input(sos_directory)
    else:
        logger.error(
            "The selected directory %s doesn't exist."
            "Select a new directory and try again.",
            sos_directory,
        )
        sys.exit(1)
    logger.info("sos-ansible started.")
    validate_tgt_dir(user_choice)
    node_data, curr_policy = data_input(sos_directory, rules_file, user_choice)
    if not node_data:
        logger.error(
            "No sosreports found, please review the directory %s", sos_directory
        )
        sys.exit(1)

    logger.info("Node data: {}".format(node_data))
    if params.debug:
        logger.debug("Current policy: {}".format(curr_policy))

    rules_processing(node_data, curr_policy, user_choice, params.debug)
    logger.info("sos-ansible finished.")


if __name__ == "__main__":
    main()
