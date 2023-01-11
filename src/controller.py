from typing import AnyStr, Iterator

from bs4 import BeautifulSoup
import datetime
from selenium.webdriver.chrome.webdriver import WebDriver
from tqdm import tqdm

from src.html_extraction import ExtractHtml
from src.inghams.data_fields import InghamsDataFields
from data.save_data import SaveData
from data.read_data import ReadData
from src.tui.data_fields import TuiDataFields
from src.cms_input import CmsInput


class Controller:

	def __init__(self):
		self.cms_input = CmsInput()

	def navigate_to_add_page(self):
		self.cms_input.instantiate_cms_add_page()

	def _save_listing(self):
		self.cms_input.save_listing()

	def _enter_data_into_cms(self, source: str, row_dict: dict[str, any]):
		self.cms_input.add_hotel_name(row_dict['Name'])
		self.cms_input.add_text_description_field(row_dict['Description'])
		self.cms_input.add_text_description_field(row_dict['Rooms'])
		self.cms_input.add_text_description_field(row_dict['Food & Drink'])
		self.cms_input.select_facilities(row_dict['Facilities'])
		self.cms_input.add_map_location(row_dict['Location'])
		self.cms_input.add_images(source=source, images=row_dict['Images'])


class InghamsController(Controller):

	def __init__(self, filename: str):
		super().__init__()
		self.__filename = filename
		self.save_data = SaveData(self.__filename, 'inghams')
		self.read_data = ReadData(self.__filename, 'inghams')

	def read_scraped_data(self) -> list[str] and Iterator[any]:
		return self.read_data.read_scraped_data()

	def get_url_list(self) -> list[str]:
		return self.read_data.read_url_list()

	@staticmethod
	def get_html_obj(page_url: str) -> BeautifulSoup:
		ex_html = ExtractHtml(page_url)
		return ex_html.parse_html_bs()

	@staticmethod
	def get_inghams_data_fields(html_obj: BeautifulSoup) -> list[str]:
		data_fields = InghamsDataFields(html_obj)
		data_fields_list = [
			data_fields.get_name(),
			data_fields.get_description(),
			data_fields.get_rooms(),
			data_fields.get_location(),
			data_fields.get_facilities(),
			data_fields.get_food_and_drink(),
			data_fields.get_images(),
			data_fields.get_excursions()
		]
		return data_fields_list

	def enter_inghams_data(self, row_dict: dict[str, any]):
		self._enter_data_into_cms('inghams', row_dict)
		self._save_listing()


class TuiController(Controller):

	def __init__(self, filename: str):
		super().__init__()
		self.__filename = filename
		self.save_data = SaveData(self.__filename, 'tui')
		self.read_data = ReadData(self.__filename, 'tui')

	def read_scraped_data(self) -> list[str] and Iterator[any]:
		return self.read_data.read_scraped_data()

	def get_url_list(self) -> list[str]:
		return self.read_data.read_url_list()

	@staticmethod
	def get_driver_obj(page_url: str) -> WebDriver:
		ex_html = ExtractHtml(page_url)
		return ex_html.parse_html_selenium()

	@staticmethod
	def get_tui_data_fields(driver: WebDriver) -> list[str]:
		data_fields = TuiDataFields(driver)
		data_fields_list = [
			data_fields.get_name(),
			data_fields.get_description(),
			data_fields.get_rooms(),
			data_fields.get_location(),
			data_fields.get_facilities(),
			data_fields.get_food_and_drink(),
			data_fields.get_images()
		]
		return data_fields_list

	def enter_tui_data(self, row_dict: dict[str, any]):
		self._enter_data_into_cms('tui', row_dict)
		self._save_listing()





