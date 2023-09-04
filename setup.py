from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='ScapeCord',
	version='0.0.1',
	description='A simple web scraper for Discord channels',
	long_description=long_description,
	long_description_content_type="text/markdown",
	py_modules=["ScrapeCord"],
	package_dir={'': 'src'}
)