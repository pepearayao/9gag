from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='scraper',
      version="0.0.1",
      description="Scrapper to retrieve posts from 9gag.",
      author="Pepe Araya",
      author_email="pepearayao@gmail.com",
      url="https://github.com/pepearayao/9gag",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      include_package_data=True,
      zip_safe=False)
