# pylint: skip-file

from os import path


def test_placeholder():
    assert path.exists('README.md')
