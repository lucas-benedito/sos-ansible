"""Custom parser to evaluate conditions"""
import argparse
import re


class CheckDependsAction(argparse.Action):  # pylint: disable=too-few-public-methods
    """custom action to evaluate dependency on case number"""

    def __call__(self, parser, namespace, values, option_string=None):
        casenum = re.search(r"-(\d{8})\-", values)
        if casenum:
            namespace.case = casenum.group().replace("-", "")

        if namespace.case:
            namespace.tarball = [value.strip() for value in values.split(",")]
        else:
            parser.error("Missing case number")


class Parser:  # pylint: disable=too-few-public-methods
    """custom parser to evaluate special conditions"""

    @staticmethod
    def get_args():
        """method to create and augment Argparse"""
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
            "-c",
            "--case",
            type=str,
            help="Directory number to which the sosreport was extracted",
            required=False,
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Enable debug message logging",
            required=False,
            default=False,
        )
        parser.add_argument(
            "-t",
            "--tarball",
            action=CheckDependsAction,
            help="Path to tarball to expand",
            required=False,
            default=[],
        )

        return parser.parse_args()
