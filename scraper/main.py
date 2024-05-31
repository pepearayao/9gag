from selenium import webdriver
from params import POSTS_TO_FETCH, COMMENTS, ENVIRONMENT
import time

def get_posts(n:int = POSTS_TO_FETCH) -> bool:
    '''
    Function to retrieve N amount of posts from 9 gag.

    :n: Number of posts to retrieve. Default number defined in config file.
    :return: True when scraped correctly. False when not scraped correctly.
    '''
#   Instantiate webdriver and make it headless in production environments.
    options = webdriver.ChromeOptions()
    if ENVIRONMENT == 'PROD': options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

#   Opens website and waits for it to load.
    driver.get("https://9gag.com/")
    driver.implicitly_wait(5)

#   If website doesn't load correctly, raise an error.
    if driver.title != '9GAG - Best Funny Memes and Breaking News':
        #Should raise an error. Will come back later. For now returns False.
        return False

#   Accepts cookies
    driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
    time.sleep(5)

#   Will scroll down the site and on each scroll, will capture new items and process them.

#   Last pixel and scroll size control how much scrolls down per iteration.
    last_pixels = 0
    scroll_size = 1000

#

if __name__ == "__main__":
    get_posts(1)
