from fixture import chrome_browser, json_output
from scraper.main import get_posts

def test_basic_web_load(chrome_browser):
    '''
    Tests that 9gag is accessible. Uses webdrive from Fixture.
    '''

    chrome_browser.get('https://9gag.com')
    assert chrome_browser.title == '9GAG - Best Funny Memes and Breaking News'

def test_posts_retrieval(chrome_browser):
    '''
    Tests that the main function retrieves the posts requested.
    '''
    chrome_browser.get("https://9gag.com/")
    post = get_posts(1)
    assert post

def test_output_format(json_output):
    '''
    Tests that output file generated has the format requiered.
    '''

    assert sorted(json_output.keys()) == sorted([
        'title',
        'interest_category',
        'tags',
        'upvotes',
        'comments',
        'awards',
        'media_type',
        'media_url',
        'post_url'
    ])
