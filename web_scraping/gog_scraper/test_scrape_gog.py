# pylint: skip-file

import pytest

from scrape_gog_game import format_os, format_price


@pytest.mark.parametrize("os_string,os",
                         [("windows, MAC, linux", ["Windows", "Mac", "Linux"]),
                          ("windows(10,11)", ["Windows"]),
                          ("LINUX", ["Linux"]),
                          ("Linux (Ubuntu 20.04, Ubuntu 22.04)", ["Linux"]),
                          ("MAC OS X (10.12+)", ["Mac"]),
                          ("Windows (10, 11), Linux (Ubuntu 20.04, Ubuntu 22.04), Mac OS X (10.12+)", ["Windows", "Mac", "Linux"])])
def test_format_os(os_string, os):

    assert format_os(os_string) == os


@pytest.mark.parametrize("price_str,price",
                         [("49.99", 4999),
                          ("FREE", 0),
                          ("00.00", 0),
                          ("frEe", 0),
                          ("1.00", 100)])
def test_format_price(price_str, price):

    assert format_price(price_str) == price
