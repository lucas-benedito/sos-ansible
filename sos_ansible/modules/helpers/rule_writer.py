"""
Utility to create json rules file
"""

import logging
import inquirer
from sos_ansible.modules.helpers.write_json import create_json

logger = logging.getLogger(__name__)

FILE_PATH = "rules/rules.json"


def get_user_inputs():
    """Prompts for fields to populate rules json file"""
    questions = [
        inquirer.Text("rule_name", message="Rule name?"),
        inquirer.Text(
            "files",
            message='Which files would you like to include? example ["foo.log", "bar.log"]',
        ),
        inquirer.Path("path", message="What is the path to search?"),
        inquirer.Text("query", message="What is the query string?"),
    ]
    prompted_answers = inquirer.prompt(questions)
    rule_data = {
        prompted_answers["rule_name"]: {
            "files": prompted_answers["files"].split(","),
            "path": prompted_answers["path"],
            "query": prompted_answers["query"],
        }
    }
    create_json(FILE_PATH, rule_data)
    question = [inquirer.Text("go_again", message="Add another rule (True or False)? ")]
    go_again = inquirer.prompt(question)
    if go_again["go_again"].lower() == "true":
        get_user_inputs()


if __name__ == "__main__":
    get_user_inputs()
