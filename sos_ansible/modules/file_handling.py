"""
Provide all file handling functions
"""

from json import load, decoder
import os
import sys
import re
import tarfile
import zipfile
from logging import getLogger
from shutil import rmtree
from sos_ansible.modules.config_manager import ConfigParser
from sos_ansible.modules.locating_sos import LocateReports

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
                logger.error("Invalid json in %s} file.\n %s", policy_name, error)
                sys.exit(1)
    except FileNotFoundError as error:
        logger.error(
            "File %s does not exist. Please set another rules file.\n %s",
            policy_name,
            error,
        )
        sys.exit(1)


def validate_out_dir(directory):
    """Validate if Target Directory exists"""
    tgt_dir = os.path.expanduser(config.config_handler.get("files", "target"))
    case_dir = os.path.join(tgt_dir, directory)
    logger.debug("Target Directory: %s, Case Directory: %s", tgt_dir, case_dir)
    if os.path.isdir(case_dir):
        logger.info(
            "The target directory %s exists. Removing it before running the script.",
            case_dir,
        )
        try:
            rmtree(case_dir)
        except Exception as error:  # pylint: disable=broad-except
            logger.error("Failure while creating %s : %s", case_dir, error)
            sys.exit(1)

def expand_sosreport(tarball,case):
    """Untar sosreport""" 
    tgt_dir = os.path.join(os.path.expanduser(config.config_handler.get("files", 'source')),case)
    logger.debug("Untarring provided sosreport %s", tarball)
    try:
        for tar in tarball:
            with zipfile.ZipFile(tar, 'r') as zip_file:
                zip_file.extractall(path=tgt_dir)
    except zipfile.BadZipFile:
        try:
            for tar in tarball:
                with tarfile.open(tar, 'r') as tar_file:
                    tar_file.extractall(path=tgt_dir)
        except Exception:
            logger.error("%s is not a valid archive", tarball)

def create_dir(directory, hostname):
    """Create a directory"""
    tgt_dir = os.path.abspath(
        os.path.expanduser(config.config_handler.get("files", "target"))
    )
    case_dir = os.path.join(tgt_dir, directory)
    try:
        if not os.path.isdir(case_dir):
            os.mkdir(case_dir)
    except OSError as error:
        logger.error("Failure while creating %s : %s", case_dir, error)
        sys.exit(1)
    final_directory = os.path.join(tgt_dir, directory, hostname)
    try:
        if not os.path.isdir(final_directory):
            os.mkdir(final_directory)
    except OSError as error:
        logger.error("Failure while creating %s : %s", final_directory, error)
        sys.exit(1)
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
        logger.info("Skipping %s. Path does not exist.", file_name)

    if data:
        final_directory = create_dir(tgt_dir, hostname)
        create_output(final_directory, rules, data)
    return match_count


def data_input(sos_directory, rules_file, user_choice):
    """
    Load the external sosreport and policy rules
    """
    logger.critical("Validating sosreports at the source directory: %s", sos_directory)
    report_data = LocateReports()
    node_data = report_data.run(sos_directory, user_choice)
    logger.critical("Validating rules in place: %s", rules_file)
    curr_policy = read_policy(rules_file)
    return node_data, curr_policy


def rules_processing(node_data, curr_policy, user_choice, debug):
    """
    Read the rules.json file and load it on the file_handling modules for processing.
    """
    div = "\n--------\n"
    for hosts in node_data:
        hostname = hosts["hostname"]
        path = hosts["path"]
        analysis_summary = (
            f"Summary:\n\n{hostname}:{div}Controller Node: {hosts['controller']}{div}"
        )
        logger.critical("Processing node %s:", hostname)
        for rules in curr_policy:
            match_count = int()
            iterator = curr_policy[rules]
            for files in iterator["files"]:
                to_read = f"{path}/{iterator['path']}/{files}"
                query = iterator["query"].replace(", ", "|")
                match_count += process_rule(
                    hostname, user_choice, rules, to_read, query
                )
                if debug:
                    logger.debug(
                        "Rule: %s, Result: %s, Query: %s, Source: %s",
                        rules,
                        match_count,
                        query,
                        to_read,
                    )
            analysis_summary += f"{rules}: {match_count}\n"
        logger.critical(analysis_summary)
