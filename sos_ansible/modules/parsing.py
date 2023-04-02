
"""Custom parser to evaluate conditions"""
import argparse

class CheckDependsAction(argparse.Action):
    """custom action to evaluate dependency on case number"""
    def __call__(self, parser, namespace, values, option_string=None):
        if len(namespace.case) < len(namespace.tarball):
            parser.error('Missing case number')
        else:
            namespace.tarball.append(values)


class Parser(): # pylint: disable=too-few-public-methods
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
            type=str,
            action=CheckDependsAction,
            help="Tarball to expand",
            required=False,
            default=""

        )

        return parser.parse_args()
