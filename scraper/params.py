import os
import yaml

# Define Abs Paths to work with.
PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(PACKAGE_PATH, '..'))
OUTPUT_PATH = os.path.join(ROOT_PATH, 'output')

CONFIG_FILE_PATH = os.path.join(PACKAGE_PATH, 'config.yaml')

# Function to retrieve YAML config values.
def get_config_values():
    with open(CONFIG_FILE_PATH, 'r') as file:
        config = yaml.safe_load(file)
    return config

configs = get_config_values()

# Define variables to work with during the rest of the scraper
OUTPUT_FORMAT = configs['output_format']
POSTS_TO_FETCH = configs['posts_to_fetch']
COMMENTS = configs['comments']
COMMENTS_TO_FETCH = configs['comments_to_fetch']


# Define variable from Environemtn

ENVIRONMENT = os.environ['ENVIRONMENT']
