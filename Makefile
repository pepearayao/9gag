clean_folders:
	rm -rf scraper/__pycache__ tests/__pycache__


install_package:
	pip install -e .

test:
	pytest -vv

run:
	curl x
