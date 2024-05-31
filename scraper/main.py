from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from scraper.params import POSTS_TO_FETCH, ENVIRONMENT
from scraper.data import Post
import time
import re


class PostRetriever:
    '''
    PostRetriever is design to get structured data from 9GAG.
    '''

    def __init__(self, n:int = POSTS_TO_FETCH):
    #   Instantiate webdriver and make it headless in production environments.
        options = webdriver.ChromeOptions()
        if ENVIRONMENT == 'PROD': options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.n = n

    def load_site(self):
    #   Loads 9GAG main page
        self.driver.get("https://9gag.com/")
        self.driver.implicitly_wait(5)
    #   If website doesn't load correctly, raise an error. (Returns False for now)
        if self.driver.title != '9GAG - Best Funny Memes and Breaking News':
            return False

    def scrape_posts(self):
        '''
        Function to retrieve N amount of posts from 9 gag.
        :return: True when scraped correctly. False when not scraped correctly.
        '''

    #   Accepts cookies
        self.driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        time.sleep(5)
    #   Retrieves posts in the present DOM. Than it scrolls and retrieves again the posts in the DOM
    #   but only analyses the last ones. That is why there is scroll variables and last item index.
        present_scroll = 0
        scroll_size = 1000
        last_itme = 0
        saved_items = 0

        #   Iterate over until at least n posts have been retrieved
        while last_itme < self.n + 5:

        #   All the posts are considred articles in the DOM. So we look all the instances.
            articles = self.driver.find_elements(By.TAG_NAME, 'article')

    #   Then we retrieve the last posts loaded in DOM and work with those
            current_articles = articles[last_itme:]

        #   Iterate though the working posts and save items in JSON. We store only the ones requested, not more.
            if current_articles:
                for article in current_articles:
                    post = Post()
                    post.set_item('title', self.get_title(article))
                    post.set_item('post_url', self.get_post_link(article))
                    post.set_item('interest_category', self.get_interest_category(article))
                    post.set_item('tags', self.get_tags(article))

                    media_type, url = self.get_media_data(article)
                    post.set_item('media_type', media_type)
                    post.set_item('media_url', url)

                    upvotes, comments = self.get_metrics(article)
                    post.set_item('upvotes', upvotes)
                    post.set_item('comments', comments)

                    post.save()
                    # saved_items =+ 1
                    # if saved_items == n:
                    #     break
            time.sleep(5)

        #   Scroll down and update pixels and  last_item number
            self.driver.execute_script(f'window.scrollBy({present_scroll},{present_scroll + scroll_size})')
            present_scroll = present_scroll + scroll_size
            last_itme = len(articles)

        return True

    def get_title(self, post:WebElement) -> str:
        '''
        Retrieves the Title of the post from the item received.

        :post: Selenium WebElement object to parse
        :return: Title as a string
        '''
        return post.find_element(By.TAG_NAME, 'h2').text

    def get_post_link(self, post:WebElement) -> str:
        '''
        Retrieves the Post Link from item received

        :post: Selenium WebElement object to parse
        :return: Link to post (not Media) as a string
        '''
        return post.find_element(By.CLASS_NAME, "badge-track").get_attribute("href")

    def get_interest_category(self, post:WebElement) -> str:
        '''
        Retrieves the Interest Category from item received

        :post: Selenium WebElement object to parse
        :return: Interest Category as a string
        '''
        return post.find_element(By.CLASS_NAME, 'name').text

    def get_tags(self, post:WebElement) -> list[str]:
        '''
        Retrieves the Tags from item received

        :post: Selenium WebElement object to parse
        :return: Tags as a List of strings
        '''
        tags = post.find_element(By.CLASS_NAME, 'post-tags').find_elements(By.TAG_NAME, 'a')
        return [tag.text for tag in tags]

    def get_media_data(self, post:WebElement) -> tuple[str]:
        '''
        Retrieves Media Data

        :post: Selenium WebElement object to parse
        :return: Tuple with media type and media url as strings
        '''
    #   Retrived classes names and from there it works out the final media type.
        media_types = post.find_element(By.CLASS_NAME, "post-view").get_attribute("class").split()

    #   Removes the post view class name and the other class name is called either image-post or video-post.
    #   Split with - separatr and gets the first item return which can be image or video.
        media_type = " ".join([part for part in media_types if part != "post-view"]).split("-")[0]

    #   Obtain the video or image link. Its position in DOM changes depending on the media type.
        if media_type == 'image':
            return ('image', post.find_element(By.TAG_NAME, "img").get_attribute("src"))
        elif media_type == 'video':
            return ('video', post.find_element(By.TAG_NAME, "source").get_attribute("src"))

    def get_metrics(self, post:WebElement) -> tuple[str]:
        metrics = post.find_element(By.CLASS_NAME, 'post-afterbar-a')
        upvotes_str = metrics.find_element(By.XPATH, './/span[@class="upvote"]').text
        comments_str = metrics.find_element(By.XPATH, './/a[@class="comment badge-evt"]/*[2]').text

        upvotes = self.find_numbers(upvotes_str)
        comments = self.find_numbers(comments_str)

        return (upvotes, comments)

    def find_numbers(self, item:str) -> float:
        '''
        Finds and returns all numbers in the specified format.

        :item: Input text to search for numbers
        :return: Float number identified
        '''
        pattern = r'\b\d+(\.\d+)?K?\b'
        match = re.search(pattern, item)

        if match:
            number_str = match.group(0)
            if 'K' in number_str:
                return float(number_str.replace('K','')) * 1000
            else:
                return float(number_str)


if __name__ == "__main__":
    retriever = PostRetriever(5)
    retriever.load_site()
    retriever.scrape_posts()
