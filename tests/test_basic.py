import pytest
from sample.modules import additional

def test_addtional():
    assert additional.mycoolfunction(2, 2) == 4