"""
Provide all file handling functions
"""

from json import load, decoder
import os
from typing import Union
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


def read_policy(policy_name: os.path) -> None:
    """
    Read Rules File and returns its contents

    :param os.path policy_name: file path containing rules
    """
    try:
        with open(policy_name, "r", encoding="utf-8") as file:
            try:
                data = load(file)
                return data
            except decoder.JSONDecodeError as error:
                logger.error("Invalid json in %s} file.\n %s", policy_name, error)
                sys.exit(1)
    except FileNotFoundError:
        logger.error(
            "File %s does not exist. Please set another rules file.",
            policy_name,
        )
        sys.exit(1)


def validate_out_dir(directory: str, tgt_dir: os.path) -> None:
    """
    Validate if Target Directory exists

    :param str directory: Directory to save files
    :param os.path tgt_dir: target directory from config file
    """
    case_dir = os.path.join(tgt_dir, directory)
    logger.debug("Target Directory: %s, Case Directory: %s", tgt_dir, case_dir)
    if os.path.isdir(case_dir):
        logger.warning(
            "The target directory %s exists. Removing it before running the script.",
            case_dir,
        )
        try:
            rmtree(case_dir)
        except Exception:  # pylint: disable=broad-except
            logger.error(
                "Unable to remove %s, Please remove before rerunning.", case_dir
            )
            sys.exit(1)


def expand_sosreport(tarball: list, case: str, tgt_dir: os.path) -> None:
    """
    Untar sosreport

    :param list tarball: List of files to untar
    :param str case: case number to store file
    :param os.path tgt_dir: target directory from config file
    """
    final_dir = os.path.join(tgt_dir, case)
    logger.debug("Untarring provided sosreport %s", tarball)
    for tar in tarball:
        if os.path.isfile(tar):
            try:
                with zipfile.ZipFile(tar, "r") as zip_file:
                    zip_file.extractall(path=final_dir)
            except zipfile.BadZipFile:
                try:
                    with tarfile.open(tar, "r") as tar_file:
                        tar_file.extractall(path=final_dir)
                except Exception as err:  # pylint: disable=broad-except
                    logger.error("%s is not a valid archive.\n%s", tar, err)
                    continue
        else:
            logger.error("Invalid sosreport file. Please retry.")
            sys.exit(1)


def create_case_dir(case_choice: os.path, hostname: str, tgt_dir: os.path) -> os.path:
    """
    Create a directory

    :param os.path case_choice: case number
    :param str hostname: hostname collected from reports
    :param os.path tgt_dir: target directory from config file
    :return os.path final_directory
    """
    case_dir = os.path.join(tgt_dir, case_choice)
    try:
        if not os.path.isdir(case_dir):
            os.mkdir(case_dir)
    except FileNotFoundError:
        logger.error("Missing parent directory resulting in failure.")
        sys.exit(1)
    final_directory = os.path.join(case_dir, hostname)
    if not os.path.isdir(final_directory):
        os.mkdir(final_directory)
    return final_directory


def create_output(final_directory: os.path, rules: str, data: dict) -> None:
    """
    Create the output data for each rule processed

    :param os.path final_directory: Directory to save content
    :param str rules: filename based on rules being processed
    :param str data: Multiline string content to be written
    """
    out_file = rules.replace(" ", "_")
    logger.warning("Populating file %s/%s", final_directory, out_file)
    with open(f"{final_directory}/{out_file}", "a", encoding="utf-8") as file:
        for lines in data:
            file.write(lines)


def process_rule(
    hostname: str,
    case_choice: os.path,
    rules: str,
    file_name: str,
    query: str,
    tgt_dir: os.path,
) -> str:
    """
    Process each Rule and gather matching data from sosreport files.

    :param str hostname: Hostname extract from report
    :param os.path case_choice: Directory where files will be stored
    :param str rules: rule name being processed
    :param str file_name: File to be searched based for this query
    :param str query: words to be searched inside file
    :param os.path tgt_dir:
    :return str match_count
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
        final_directory = create_case_dir(case_choice, hostname, tgt_dir)
        create_output(final_directory, rules, data)
    return match_count


def data_input(
    sos_directory: os.path, rules_file: os.path, user_choice: str
) -> Union[dict, dict]:
    """
    Load the external sosreport and policy rules

    :param os.path sos_directory: Directory containing sosreports
    :param os.path rules_file: File path containing rules file
    :param str user_choice: Case number selected
    :return: node_data, curr_policy
    :rtype: Union[dict, dict]
    """
    logger.info("Validating sosreports at the source directory: %s", sos_directory)
    report_data = LocateReports()
    node_data = report_data.run(sos_directory, user_choice)
    logger.info("Validating rules in place: %s", rules_file)
    curr_policy = read_policy(rules_file)
    return node_data, curr_policy


def rules_processing(
    node_data: dict, curr_policy: dict, user_choice: str, debug: str, tgt_dir: os.path
) -> None:
    """
    Read the rules.json file and load it on the file_handling modules for processing.
    :param dict node_data: Keypair values containing hostname, path, controller
    :param dict curr_policy: Nested dic containing Rule and its parameters
    :param str user_choice: Case number string
    :param str debug: Variable if debug
    """
    div = "\n--------\n"
    for hosts in node_data:
        hostname = hosts["hostname"]
        path = hosts["path"]
        analysis_summary = (
            f"Summary:\n\n{hostname}:{div}Controller Node: {hosts['controller']}{div}"
        )
        logger.info("Processing node %s:", hostname)
        for rules in curr_policy:
            match_count = int()
            iterator = curr_policy[rules]
            for files in iterator["files"]:
                to_read = f"{path}/{iterator['path']}/{files}"
                query = iterator["query"].replace(", ", "|")
                match_count += process_rule(
                    hostname, user_choice, rules, to_read, query, tgt_dir
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
        logger.info(analysis_summary)
