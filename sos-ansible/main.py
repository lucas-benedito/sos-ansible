#!/usr/bin/env python
"""
sos_ansible, main program
"""

import argparse
import logging
import os
from modules import file_handling
from modules import locating_sos

SOS_DIRECTORY = os.path.abspath("/tmp/test_sosreport/")
RULES_FILE = os.path.abspath("/home/lbenedit/labs/ansible/policy_template/rules.json")


def data_input(sos_directory, rules_file):
    """
    Load the external sosreport and policy rules
    """
    logging.info("Validating sosreports on target directory: %s", sos_directory)
    test = locating_sos.LocateReports()
    node_data = test.run({sos_directory})
    logging.info("Validating rules in place:")
    curr_policy = file_handling.read_policy(rules_file)
    return node_data, curr_policy


def rules_processing(node_data, curr_policy):
    """
    Read the rules.json file and load it on the file_handling modules for processing.
    """
    for hosts in node_data:
        hostname = hosts['hostname']
        path = hosts['path']
        logging.info("Checking node %s:", hostname)
        for rules in curr_policy:
            iterator = curr_policy[rules]
            for files in iterator['files']:
                to_read = f"{path}/{iterator['path']}/{files}"
                file_handling.process_rule(files, rules, to_read, iterator['query'])


def main():
    """
    Main function from sos_ansible. This will process all steps for sosreports reading
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-d', '--directory', type=str,
        help='Directory containing sosreports',
        required=False, default=''
    )
    parser.add_argument(
        '-r', '--rules', type=str, 
        help='Rules file with full path',
        required=False, default=''
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

    logging.basicConfig(
        filename='sos-ansible.log',
        format='%(levelname)s:%(message)s',
        level=logging.DEBUG
    )

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    logging.getLogger('').addHandler(console)

    node_data, curr_policy = data_input(sos_directory, rules_file)
    logging.info(node_data)
    rules_processing(node_data, curr_policy)


if __name__ == "__main__":
    main()
