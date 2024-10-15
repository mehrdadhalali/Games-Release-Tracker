# pylint: skip-file

import pytest
from bs4 import BeautifulSoup
from scrape_gog_game import format_os, format_price, find_price


@pytest.mark.parametrize("html, expected", [
    ('<div><span selenium-id="ProductFinalPrice">59.99</span></div>', 5999),
    ('<div><span class="product-actions-price__final-amount">21.00</span></div>', 2100),
    ('<div><span class="product-actions-price__final-amount">1999.00</span></div>', 199900),
])
def test_find_price(html, expected):
    soup = BeautifulSoup(html, 'html.parser')
    assert find_price(soup) == expected


def test_find_price_raises_error():
    soup = BeautifulSoup(
        '<div><span class="no-price-here"></span></div>', 'html.parser')
    with pytest.raises(ValueError, match="The price is somewhere else!"):
        find_price(soup)


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
