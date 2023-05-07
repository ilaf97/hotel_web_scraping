import time
from typing import Iterator, Union
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver

from src.controller.abstract_controller import AbstractCompanyController
from src.seleniuim.html_extraction import ExtractHtml
from src.inghams.data_fields import InghamsDataFields
from data.save_data import SaveWebScrapingData
from data.read_data import ReadData
from src.tui.data_fields import TuiDataFields
from src.seleniuim.cms_listing_mapper import CmsListingMapper


class BaseController:
	"""
	Class to handle data flows within the application.

	Attributes:
	- cms_input (CmsInput)

	Methods:
	- naviagte_to_add_page()
	- _save_listing() (Protected)
	- _enter_data_into_cms() (Protected)
	"""

	def __init__(self, cms_driver: WebDriver):
		self.cms_input_mapper = CmsListingMapper(cms_driver)

	@staticmethod
	def _create_data_fields_dict(data_fields: Union[InghamsDataFields, TuiDataFields]) -> dict[any]:
		data_fields_dict = {
			"hotel_name": data_fields.get_name(),
			"description": data_fields.get_description(),
			'best_for': data_fields.get_best_for(),
			"rooms": data_fields.get_rooms(),
			"location": data_fields.get_location(),
			"facilities": data_fields.get_facilities(),
			"meals": data_fields.get_meals(),
			"images": data_fields.get_images(),
		}
		return data_fields_dict

	def _enter_data_into_cms(self, source: str, hotel_attributes: dict[str, any]):
		self.cms_input_mapper.add_hotel_name(hotel_attributes['hotel_name'])
		self.cms_input_mapper.set_holiday_id()
		self.cms_input_mapper.set_resort(hotel_attributes.get('resort'))
		self.cms_input_mapper.add_text_description_field(hotel_attributes['description'], 'description')
		self.cms_input_mapper.add_text_description_field(hotel_attributes['rooms'], 'rooms')
		self.cms_input_mapper.add_text_description_field(hotel_attributes['meals'], 'meals')
		self.cms_input_mapper.add_best_for(hotel_attributes['best_for'])
		self.cms_input_mapper.select_facilities(hotel_attributes['facilities'])
		self.cms_input_mapper.add_map_location(hotel_attributes['location'])
		self.cms_input_mapper.add_images(source_company=source, images=hotel_attributes['images'])


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

	def __init__(self, filename: str, cms_driver: WebDriver):
		BaseController.__init__(self, cms_driver)
		self.__filename = filename
		self.save_data = SaveWebScrapingData(self.__filename, 'inghams')
		self.read_data = ReadData(self.__filename, 'inghams')

	def create_json_file(self):
		"""Create file into which scraped data can be saved"""
		self.save_data.create_json_file()

	def read_scraped_data(self) -> list[str] and Iterator[any]:
		"""Returns column headers and a row iterator object"""
		return self.read_data.read_data()

	def get_url_list(self) -> list[str]:
		"""Returns all URLs of listings to scrape"""
		return self.read_data.read_url_list()

	@staticmethod
	def get_driver_obj(page_url: str) -> BeautifulSoup:
		"""Returns a newly instantiated BeautifulSoup HTML object"""
		ex_html = ExtractHtml(page_url)
		return ex_html.parse_html_bs()

	def get_data_fields_json(self, html_obj: BeautifulSoup) -> dict[any]:
		"""Returns raw data scraped from a given Ingham's listing"""
		data_fields = InghamsDataFields(html_obj)
		data_fields_dict = self._create_data_fields_dict(data_fields)
		data_fields_dict['excursions'] = data_fields.get_excursions()
		return data_fields_dict

	def enter_data(self, hotel_attributes: dict[str, any]):
		"""Enter and save accommodation data into the CMS"""
		self._enter_data_into_cms('inghams', hotel_attributes)


class TuiController(BaseController, AbstractCompanyController):
	"""
	Class to handle TUI's data flows within the application.

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

	def __init__(self, filename: str, cms_driver: WebDriver, tui_site: str):
		BaseController.__init__(self, cms_driver)
		self.__filename = filename
		self.tui_site = tui_site
		self.save_data = SaveWebScrapingData(self.__filename, tui_site)
		self.read_data = ReadData(self.__filename, tui_site)

	def create_json_file(self):
		"""Create file into which scraped data can be saved"""
		self.save_data.create_json_file()

	def read_scraped_data(self) -> list[str] and Iterator[any]:
		"""Returns column headers and a row iterator object"""
		return self.read_data.read_data()

	def get_url_list(self) -> list[str]:
		"""Returns all URLs of listings to scrape"""
		return self.read_data.read_url_list()

	@staticmethod
	def get_driver_obj(page_url: str) -> WebDriver:
		"""Returns a newly instantiated Selenium WebDriver object"""
		ex_html = ExtractHtml(page_url)
		return ex_html.parse_html_selenium()

	def get_data_fields_json(self, driver: WebDriver) -> dict[any]:
		"""Returns raw data scraped from a given TUI listing"""
		data_fields = TuiDataFields(driver)
		time.sleep(1)
		return self._create_data_fields_dict(data_fields)

	def enter_data(self, hotel_attributes: dict[str, any]):
		"""Enter and save accommodation data into the CMS"""
		self._enter_data_into_cms(self.tui_site, hotel_attributes)

