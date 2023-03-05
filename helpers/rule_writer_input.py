""" Helper utility to create an ad-hoc rules file"""

import json
import os

FILE_PATH = "rules/rules.json"


def get_user_inputs():
    """Gather info from the user to build json file"""
    rule_name = input("Rule name? ")
    files = input(
        """
Which files would you like to include?
example: foo.log, bar.log, new.log
"""
    ).split(",")
    path = input("What is the path to search? ")
    query = input("What are the queries? ")
    rule_data = {
        rule_name: {"files": list(files), "path": path, "query": query},
    }
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            data.update(rule_data)
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4))
    else:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            file.write(json.dumps(rule_data, indent=4))
    go_again = input("Add another entry(True or False)? ")
    if go_again.lower() == "true":
        get_user_inputs()


if __name__ == "__main__":
    get_user_inputs()
