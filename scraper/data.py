import os
import json
from params import OUTPUT_PATH, OUTPUT_FORMAT


class Post:
    '''
    Post class that stores each post's data and stores as Json as well
    '''
    def __init__(self):
        self.post = {
            'title': '',
            'interest_category': '',
            'tags': [],
            'upvotes': '',
            'comments': '',
            'awards': '',
            'media_type': '',
            'media_url': '',
            'post_url': ''

        }

    def set_title(self, title:str):
        '''
        Saves Post Title

        :title: Title of the post
        '''
        self.post['title'] = title

    def set_post_url(self, post_url:str):
        '''
        Saves Post Title

        :post_url: URL of post
        '''
        self.post['post_url'] = post_url

    def save(self):
        '''
        Saves the post scanned to persistent medium.

        For now it appends data and it gets repeated as there is no built in
        mechanism to detect duplicates. Will work on that later.
        '''

        if OUTPUT_FORMAT == 'json':
            try:
                with open(os.path.join(OUTPUT_PATH, 'output.json'), 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = []

            data.append(self.post)

            with open(os.path.join(OUTPUT_PATH, 'output.json'), 'w') as file:
                json.dump(data, file, indent=4)
        elif OUTPUT_FORMAT == 'csv':
            pass
        elif OUTPUT_FORMAT == 'XML':
            pass
        elif OUTPUT_FORMAT == 'postgres':
            pass
