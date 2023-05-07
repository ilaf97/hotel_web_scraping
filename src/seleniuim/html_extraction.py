import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from requests import HTTPError, ConnectionError


class ExtractHtml:
	"""
	Class to retireve page HTML representation, instantiate BeautifulSoup HTML objects, and instantiate Selenium
	site drivers.

	Params:
	- url (str): the page url from which to retrieve site data

	Attributes:
	- url (str)

	Methods:
	- get_html_text()
	- parse_html_bs()
	- parse_html_selenium()
	"""

	def __init__(self, url: str):
		self.url = url
		try:
			self.__page = requests.get(self.url)
		except HTTPError as e:
			raise HTTPError(f'The URL requested cannot be retrieved!\n{e}')
		except ConnectionError as e:
			raise ConnectionError(f'Cannot connect to server: there is a network problem!\n{e}')

	def get_html_text(self) -> str:
		"""Return page's plain HTML text representation"""
		return self.__page.text

	def parse_html_bs(self) -> BeautifulSoup:
		"""Return BeautifulSoup object from parsing HTML"""
		return BeautifulSoup(
			self.__page.content,
			'html.parser'
		)

	def parse_html_selenium(self):
		"""Return Selenium WebDriver object from parsing HTML"""
		opts = webdriver.ChromeOptions()
		opts.add_argument('--incognito')
		driver = webdriver.Chrome(options=opts)
		driver.get(self.url)
		return driver

