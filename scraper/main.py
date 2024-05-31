from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from scraper.params import POSTS_TO_FETCH, ENVIRONMENT
from scraper.data import Post
import time


def get_title(post:WebElement) -> str:
    '''
    Retrieves the Title of the post from the item received.

    :post: Selenium WebElement object to parse
    :return: Title as a string
    '''
    return post.find_element(By.TAG_NAME, 'h2').text

def get_post_link(post:WebElement) -> str:
    '''
    Retrieves the Post Link from item received

    :post: Selenium WebElement object to parse
    :return: Link to post (not Media) as a string
    '''
    return post.find_element(By.CLASS_NAME, "badge-track").get_attribute("href")

def get_interest_category(post:WebElement) -> str:
    '''
    Retrieves the Interest Category from item received

    :post: Selenium WebElement object to parse
    :return: Interest Category as a string
    '''
    return post.find_element(By.CLASS_NAME, 'name').text

def get_tags(post:WebElement) -> list[str]:
    '''
    Retrieves the Tags from item received

    :post: Selenium WebElement object to parse
    :return: Tags as a List of strings
    '''
    tags = post.find_element(By.CLASS_NAME, 'post-tags').find_elements(By.TAG_NAME, 'a')
    return [tag.text for tag in tags]


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

#   Retrieves posts in the present DOM. Than it scrolls and retrieves again the posts in the DOM
#   but only analyses the last ones. That is why there is scroll variables and last item index.

    present_scroll = 0
    scroll_size = 1000
    last_itme = 0
    saved_items = 0

#   Iterate over until at least n posts have been retrieved
    while last_itme < n+5:

#   All the posts are considred articles in the DOM. So we look all the instances.
        articles = driver.find_elements(By.TAG_NAME, 'article')

#   Then we retrieve the last posts loaded in DOM and work with those
        current_articles = articles[last_itme:]

#   Iterate though the working posts and save items in JSON. We store only the ones requested, not more.
        if current_articles:
            for article in current_articles:
                post = Post()
                post.set_item('title', get_title(article))
                post.set_item('post_url', get_post_link(article))
                post.set_item('interest_category', get_interest_category(article))
                post.set_item('tags', get_tags(article))
                post.save()
                # saved_items =+ 1
                # if saved_items == n:
                #     break
        time.sleep(5)

#   Scroll down and update pixels and  last_item number
        driver.execute_script(f'window.scrollBy({present_scroll},{present_scroll + scroll_size})')
        present_scroll = present_scroll + scroll_size
        last_itme = len(articles)

    return True

if __name__ == "__main__":
    get_posts(5)
