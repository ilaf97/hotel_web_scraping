from bs4 import BeautifulSoup
from src.inghams.data_fields import InghamsSiteData

from src.controller.controller import BaseController
from src.models.hotel_model import Hotel
from src.web_driver_factory import WebDriverFactory


class InghamsController(BaseController):
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

	def __init__(self, filename: str):
		BaseController.__init__(
			self,
			filename=filename,
			company_name="inghams"
		)

	@staticmethod
	def get_driver_obj(page_url: str) -> BeautifulSoup:
		"""Returns a newly instantiated BeautifulSoup HTML object"""
		ex_html = WebDriverFactory(page_url)
		return ex_html.parse_html_bs()

	def get_hotel_obj(self, html_obj: BeautifulSoup) -> Hotel:
		"""Returns raw data scraped from a given Ingham's listing"""
		inghams_site_data = InghamsSiteData(html_obj)
		inghams_hotel = self._create_hotel(inghams_site_data)
		inghams_hotel['excursions'] = inghams_site_data.get_excursions()
		return inghams_hotel

