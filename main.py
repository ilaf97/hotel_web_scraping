import time
from datetime import datetime
from typing import Union, Any

from tqdm import tqdm

from src.controller import InghamsController, TuiController, Controller
from src.cms_instance import CmsInstance


class Main(CmsInstance):
	"""
	Main class of the web scraping application. This is the user endpoint from which to run the application.

	Params:
	- inghams_filename (str): the filename under which to save scraped Ingham's site data
	- tui_filename (str): the filename under which to save scraped TUI site data

	Attributes:
	- inghams_controller (InghamsController)
	- tui_controller (TuiController)
	- controller (Controller)
	- __tui_items (int) (Private)
	- __inghams_items (int) (Private)

	Methods:
	- scrape_and_save_data()
	- read_data_and_enter_into_cms()
	- navigate_to_add_page()
	- __create_row_dict() (Private)
	- __check_source_company() (Private)
	- __get_inghams_url_list() (Private)
	- __get_tui_url_list() (Private)
	- __get_driver_or_html() (Private)
	"""

	def __init__(self, inghams_filename: str, tui_filename: str):
		super().__init__()
		self.inghams_controller = InghamsController(inghams_filename, self.driver)
		self.tui_controller = TuiController(tui_filename, self.driver)

	def scrape_and_save_data(self, source_company):
		self.__check_source_company(source_company)

		if source_company == 'inghams':
			url_list = self.__get_inghams_url_list()
			self.inghams_controller.create_json_file()
			for url in tqdm(url_list):
				url_html_obj = self.__get_driver_or_html(source_company, url.strip())
				hotel_data = self.inghams_controller.get_inghams_data_fields_json(url_html_obj)
				self.inghams_controller.save_data.add_data(hotel_data)
		else:
			url_list = self.__get_tui_url_list()
			self.tui_controller.create_json_file()
			for url in tqdm(url_list):
				driver_obj = self.__get_driver_or_html(source_company, url.strip())
				hotel_data = self.tui_controller.get_tui_data_fields(driver_obj)
				self.tui_controller.save_data.add_data(hotel_data)
			driver_obj.close()

	def read_data_and_enter_into_cms(self, source_company: str):
		self.__check_source_company(source_company)
		if source_company == 'inghams':
			hotels_json = self.inghams_controller.read_data.read_data()
			num_inghams_items = len(hotels_json)
			while tqdm(len(hotels_json), total=num_inghams_items):
				hotel_dict = hotels_json.pop(0)
				self.inghams_controller.enter_inghams_data(hotel_dict)
				time.sleep(1)
				self.save_listing()

		else:
			hotels_json = self.tui_controller.read_data.read_data()
			num_tui_items = len(hotels_json)
			while tqdm(len(hotels_json), total=num_tui_items):
				hotel_dict = hotels_json.pop(0)
				self.tui_controller.enter_tui_data(hotel_dict)
				time.sleep(1)
				self.save_listing()

	@staticmethod
	def __check_source_company(source_company: str):
		if source_company not in ['inghams', 'tui']:
			raise ValueError(f'source_company must be either "inghams" or "tui" ("{source_company}" passed')

	def __get_inghams_url_list(self) -> list[str]:
		return self.inghams_controller.get_url_list()

	def __get_tui_url_list(self) -> list[str]:
		return self.tui_controller.get_url_list()

	def __get_driver_or_html(self, source_company: str, page_url: str):
		if source_company == 'inghams':
			return self.inghams_controller.get_html_obj(page_url)
		else:
			return self.tui_controller.get_driver_obj(page_url)



if __name__ == '__main__':
	current_date = datetime.today().strftime("%Y-%m-%d")
	tui_filename = f'tui-{current_date}'
	inghams_filename = f'inghams-{current_date}'

	main = Main(inghams_filename=inghams_filename, tui_filename=tui_filename)

	# Scrape and save data for either site
	# main.scrape_and_save_data('tui')
	main.scrape_and_save_data('inghams')

	# Add data to CMS
	# main.instantiate_cms_add_page()
	# main.read_data_and_enter_into_cms('tui')
	main.read_data_and_enter_into_cms('inghams')

	print('Complete! Please check site listings to ensure data is correct')


