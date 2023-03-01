"""
Provide all file handling functions
"""

import json
import os
import logging

DIVISOR = 10 * "-"

logger = logging.getLogger('modules.file_handling')


def read_policy(policy_name):
    """Read Rules File and returns its contents"""
    with open(policy_name, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def process_rule(files, rules, file_name, query):
    """
    Process each Rule and gather matching data from sosreport files.
    Returns str
    """
    data = ""
    if query:
        if not isinstance(query, list):
            query = query.split()

    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            if not query:
                data = file.readlines()
            else:
                for lines in file.readlines():
                    for item in query:
                        if item.lower() in lines or item.upper() in lines:
                            data += str(lines)
    else:
        logging.warning("Skipping %s. Path does not exist.", file_name)
    if not data:
        logging.debug("Criteria %s not met.", query)
    else:
        logging.debug("Rule: %s - %s\n%s\n", rules, files, data)
