import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests import HTTPError


class ExtractHtml:

	def __init__(self, url: str):
		self.url = url
		try:
			self.__page = requests.get(self.url)
		except HTTPError as e:
			raise HTTPError(f'The URL requested cannot be retrieved!\n{e}')
		except ConnectionError as e:
			raise ConnectionError(f'Cannot connect to server: there is a network problem!\n{e}')

	def get_html_text(self) -> str:
		return self.__page.text

	def parse_html_bs(self) -> BeautifulSoup:
		return BeautifulSoup(
			self.__page.content,
			'html.parser'
		)

	def parse_html_selenium(self, web_driver_path):
		opts = webdriver.ChromeOptions()
		opts.add_argument('--incognito')
		driver = webdriver.Chrome(executable_path=web_driver_path, options=opts)
		driver.get(self.url)
		return driver

