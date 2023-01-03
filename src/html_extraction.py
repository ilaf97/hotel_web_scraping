import requests
from bs4 import BeautifulSoup
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

	def parse_html(self) -> BeautifulSoup:
		return BeautifulSoup(
			self.__page.content,
			'html.parser'
		)


ht = ExtractHtml('https://www.inghams.co.uk/destinations/italy/neapolitan-riviera/amalfi-coast/hotel-aurora-amalfi#0')
#print(ht.parse_html())
