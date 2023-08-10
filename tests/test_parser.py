"""test parsing"""
from unittest.mock import patch
import pytest
from sos_ansible.modules.parsing import Parser


def test_parser(capsys):
    """test missing case number"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with patch("sys.argv", ["sos_ansible", "--tarball", "test.tar.gz"]):
            Parser.get_args()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
    with patch(
        "sys.argv", ["sos_ansible", "--case", "999999", "--tarball", "test.tar.gz"]
    ):
        Parser.get_args()
        captured = capsys.readouterr()
        assert captured.out == ""
