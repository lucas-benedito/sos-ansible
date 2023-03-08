"""
Provide all file handling functions
"""

from json import load, decoder
import os
import sys
import re
from logging import getLogger
from shutil import rmtree
from modules.config_manager import ConfigParser

config = ConfigParser()
config.setup()

logger = getLogger("root")


def read_policy(policy_name):
    """Read Rules File and returns its contents"""
    try:
        with open(policy_name, "r", encoding="utf-8") as file:
            try:
                data = load(file)
                return data
            except decoder.JSONDecodeError as error:
                logger.error(error)
                sys.exit(f"Invalid json in {policy_name} file")
    except FileNotFoundError as error:
        logger.error(error)
        sys.exit(f"File {policy_name} does not exist. Please set another rules file.")


def validate_tgt_dir(directory):
    """Validate if Target Directory exists"""
    tgt_dir = os.path.expanduser(config.config_handler.get("files", "target"))
    case_dir = os.path.join(tgt_dir, directory)
    logger.debug("Target Directory: %s, Case Directory: %s", tgt_dir, case_dir)
    if os.path.isdir(case_dir):
        logger.warning(
            "The target directory %s exists. Removing it before running the script.",
            case_dir,
        )
        try:
            rmtree(case_dir)
        except Exception as error:  # pylint: disable=broad-except
            logger.error(error)
            sys.exit(f"Failure while creating {case_dir}: {error}")


def create_dir(directory, hostname):
    """Create a directory"""
    tgt_dir = os.path.expanduser(config.config_handler.get("files", "target"))
    case_dir = os.path.join(tgt_dir, directory)
    try:
        if not os.path.isdir(case_dir):
            os.mkdir(case_dir)
    except OSError as error:
        logger.error(error)
        sys.exit(f"Failure while creating {case_dir}: {error}")
    final_directory = os.path.join(tgt_dir, directory, hostname)
    try:
        if not os.path.isdir(final_directory):
            os.mkdir(final_directory)
    except OSError as error:
        logger.error(error)
        sys.exit(f"Failure while creating {final_directory}: {error}")
    return final_directory


def create_output(final_directory, rules, data):
    """Create the output data for each rule processed"""
    out_file = rules.replace(" ", "_")
    logger.info("Populating file %s/%s", final_directory, out_file)
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
        with open(file_name, "r", encoding="utf-8", errors="replace") as file:
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
                except Exception as error:  # pylint: disable=broad-except
                    logger.error(error)
    else:
        logger.warning("Skipping %s. Path does not exist.", file_name)

    if data:
        final_directory = create_dir(tgt_dir, hostname)
        create_output(final_directory, rules, data)
    return match_count
