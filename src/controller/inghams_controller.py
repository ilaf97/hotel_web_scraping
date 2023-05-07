from collections import Iterator

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver

from src.controller.abstract_controller import AbstractCompanyController
from src.controller.controller import BaseController
from src.inghams.data_fields import InghamsDataFields
from src.web_driver_factory import WebDriverFactory
from src.web_scraping.read_data import ReadData
from src.web_scraping.save_data import SaveWebScrapingData


class InghamsController(BaseController, AbstractCompanyController):
	"""
	Class to handle Ingham's data flows within the application.

	Params:
	- filename (str): name of file to save/read

	Attributes:
	- save_data (SaveData)
	- read_data (ReadData)
	- __filename (str) (Private)

	Methods:
	- read_scraped_data()
	- get_url_list()
	- get_inghams_data_fields()
	- enter_inghams_data()
	"""

	def __init__(self, filename: str, web_driver: WebDriver):
		BaseController.__init__(
			self,
			web_driver=web_driver,
			filename=filename,
			company_name='inghams')

	@staticmethod
	def get_driver_obj(page_url: str) -> BeautifulSoup:
		"""Returns a newly instantiated BeautifulSoup HTML object"""
		ex_html = WebDriverFactory(page_url)
		return ex_html.parse_html_bs()

	def get_data_fields_json(self, html_obj: BeautifulSoup) -> dict[any]:
		"""Returns raw data scraped from a given Ingham's listing"""
		data_fields = InghamsDataFields(html_obj)
		data_fields_dict = self._create_data_fields_dict(data_fields)
		data_fields_dict['excursions'] = data_fields.get_excursions()
		return data_fields_dict

