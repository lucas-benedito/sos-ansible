"""
Provide all file handling functions
"""

import json
import os
import logging
import sys
import re
from shutil import rmtree

logger = logging.getLogger(__name__)


def read_policy(policy_name):
    """Read Rules File and returns its contents"""
    with open(policy_name, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def validate_tgt_dir(directory):
    """ Validate if Target Directory exists"""
    case_dir = os.path.join('/tmp/', directory)
    if os.path.isdir(case_dir):
        logging.info("The target directory %s exists. "
             "Removing it before running the script.", case_dir)
        try:
            rmtree(case_dir)
        except Exception as error: # pylint: disable=broad-except
            logger.error(error)
            sys.exit(1)


def create_dir(directory, hostname):
    """ Create a directory"""
    case_dir = os.path.join('/tmp/', directory)
    try:
        if not os.path.isdir(case_dir):
            os.mkdir(case_dir)
    except OSError as error:
        logging.error(error)
        sys.exit(1)
    final_directory = os.path.join('/tmp/', directory, hostname)
    try:
        if not os.path.isdir(final_directory):
            os.mkdir(final_directory)
    except OSError as error:
        logging.error(error)
        sys.exit(1)
    return final_directory


def create_output(final_directory, rules, data):
    """Create the output data for each rule processed"""
    out_file = rules.replace(" ", "_")
    with open(f"{final_directory}/{out_file}", "a", encoding="utf-8") as file:
        for lines in data:
            file.write(lines)


def process_rule(hostname, tgt_dir, rules, file_name, query):
    """
    Process each Rule and gather matching data from sosreport files.
    Returns str
    """
    data = ""
    match_count = 0

    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            if not query:
                for lines in file.readlines():
                    data += str(lines)
                    match_count += 1
            else:
                try:
                    for lines in file.readlines():
                        reg_rule = re.compile(query, re.IGNORECASE)
                        if reg_rule.findall(lines):
                            data += str(lines)
                            match_count += 1
                except Exception as error: # pylint: disable=broad-except
                        logger.error(error)
    else:
        logging.warning("Skipping %s. Path does not exist.", file_name)

    if data:
        final_directory = create_dir(tgt_dir, hostname)
        create_output(final_directory, rules, data)
    return match_count
