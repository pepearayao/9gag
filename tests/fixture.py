import pytest
from selenium import webdriver
import json
import os


@pytest.fixture()
def chrome_browser():
    '''
    Return a chrome driver object instance
    '''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture()
def json_output():
    '''
    Returns json output from scraping if available. Else returns an empy list.
    '''
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(CURRENT_PATH, '..','output')

    try:
        with open(os.path.join(DATA_PATH, 'output.json'), 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    return data
