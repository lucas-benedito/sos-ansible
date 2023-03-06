"""
Common functions for helpers
"""

import os
import json

def create_json(file_path, rule_data):
    """File handling"""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            data.update(rule_data)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4))
    else:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(rule_data, indent=4))