import time
from datetime import datetime
from typing import Union

from selenium.webdriver.chrome.webdriver import WebDriver
from tqdm import tqdm

from src.controller.inghams_controller import InghamsController
from src.controller.tui_controller import TuiController
from src.cms.cms_instance import CmsInstance
from src.cms.cms_operations import CmsOperations


class Run:
	# TODO: get rid of this class as it shouldn't exist in it's current form
	# The methods within do not share common objectives
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

	def __init__(
			self,
			web_driver: WebDriver,
			cms_operations: CmsOperations,
			inghams_filename: str,
			tui_filename: str,
			crystal_filename: str):
		self.driver = web_driver
		self.cms_operations = cms_operations
		self.inghams_controller = InghamsController(inghams_filename, self.driver)
		self.tui_controller = TuiController(tui_filename, self.driver, 'tui')
		self.crystal_controller = TuiController(crystal_filename, self.driver, 'crystal_ski')

	def scrape_and_save_data(self, source_company):
		self.__check_source_company(source_company)

		if source_company == 'inghams':
			controller = self.inghams_controller

		elif source_company == 'crystal_ski':
			controller = self.crystal_controller

		else:
			controller = self.tui_controller

		self.__scrape_data_from_urls(
			url_list=controller.get_url_list(),
			company_controller=controller
		)

	def read_data_and_enter_into_cms(self, source_company: str) -> Union[InghamsController, TuiController]:
		self.__check_source_company(source_company)

		if source_company == 'inghams':
			self.__iterate_through_hotel_dict(self.inghams_controller)
			return self.inghams_controller
		elif source_company == 'crystal_ski':
			self.__iterate_through_hotel_dict(self.crystal_controller)
			return self.crystal_controller
		else:
			self.__iterate_through_hotel_dict(self.tui_controller)
			return self.tui_controller

	@staticmethod
	def check_for_failed_runs(company_controller: Union[InghamsController, TuiController]) -> bool:
		try:
			company_controller.read_data.read_data(failed_runs=True)
			return True
		except FileNotFoundError:
			return False

	@staticmethod
	def __check_source_company(source_company: str):
		if source_company not in ['inghams', 'crystal_ski', 'tui']:
			raise ValueError(
				f'source_company must be either "inghams", "tui" or "crystal_ski" ("{source_company}" passed')

	def __get_driver_or_html(self, source_company: str, page_url: str):
		if source_company == 'inghams':
			return self.inghams_controller.get_driver_obj(page_url)
		elif source_company == 'crystal_ski':
			return self.tui_controller.get_driver_obj(page_url)
		else:
			return self.tui_controller.get_driver_obj(page_url)

	def __iterate_through_hotel_dict(
			self, company_controller: Union[InghamsController, TuiController]):
		hotels_json = company_controller.read_data.read_data()
		num_items = len(hotels_json)
		while num_items:
			hotel_dict = hotels_json.pop(0)
			try:
				company_controller.enter_data(hotel_dict)
				time.sleep(1)
				self.cms_operations.save_listing()
			except Exception as e:
				hotel_dict['failed_reason'] = e.__str__()
				self.__record_failed_run(
					company_controller=company_controller,
					hotel_dict=hotel_dict)
				self.cms_operations.save_listing(failed_run=True)
			# If any exception occurs, want to return new hotel json
			num_items -= 1

	@staticmethod
	def __scrape_data_from_urls(
			url_list: list[str],
			company_controller: Union[InghamsController, TuiController]
	):
		company_controller.create_json_file()
		for url in tqdm(url_list):
			url_html_obj = company_controller.get_driver_obj(url.strip())
			hotel_dict = company_controller.get_data_fields_json(url_html_obj)
			company_controller.save_data.add_data(hotel_dict)

	@staticmethod
	def __record_failed_run(
			hotel_dict: any,
			company_controller: Union[InghamsController, TuiController]
	):
		try:
			company_controller.read_data.read_data(failed_runs=True)
		except FileNotFoundError:
			company_controller.save_data.create_json_file(failed_runs=True)

		company_controller.save_data.add_data(hotel_dict, failed_runs=True)


if __name__ == '__main__':
	current_date = datetime.today().strftime("%Y-%m-%d")
	crystal_filename = f'crystal_ski-{current_date}'
	inghams_filename = f'inghams-{current_date}'
	tui_filename = f'tui-{current_date}'

	cms_instance = CmsInstance()
	cms_operations = CmsOperations(cms_instance)
	web_driver = cms_instance.driver

	main = Run(inghams_filename=inghams_filename, tui_filename=tui_filename,
			   crystal_filename='crystal_ski-2023-05-03 (1)')

	# Scrape and save data for either site
	# main.scrape_and_save_data('crystal_ski')
	# main.scrape_and_save_data('inghams')
	# main.scrape_and_save_data('tui')

	# sys.exit()

	# Add data to CMS
	cms_operations.instantiate_cms_add_page()
	crystal_controller_instance = main.read_data_and_enter_into_cms('crystal_ski')
	# tui_controller_instance = main.read_data_and_enter_into_cms('tui')
	# inghams_controller_instance = main.read_data_and_enter_into_cms('inghams')

	if main.check_for_failed_runs(crystal_controller_instance):
		print('Some listings failed to be recorded in Crystal Ski data')

	# if main.check_for_failed_runs(inghams_controller_instance):
	# 	print('Some listings failed to be recorded in Inghams data')

	print('Complete! Please check site listings to ensure data is correct')
