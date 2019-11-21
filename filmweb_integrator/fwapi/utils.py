# coding=utf-8
import requests

from bs4 import BeautifulSoup


def make_request(url, params=None):
    """
    Makes a request to the given URL and returns the response's
    content in the form of a BeautifulSoup object.
    """
    r = requests.get(url, params)
    soup = BeautifulSoup(r.text, "lxml")
    
    return soup
