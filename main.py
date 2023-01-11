from datetime import datetime
from typing import Union

from tqdm import tqdm

from src.controller import InghamsController, TuiController, Controller


class Main:

	def __init__(self, inghams_filename: str, tui_filename: str):
		self.inghams_controller = InghamsController(inghams_filename)
		self.tui_controller = TuiController(tui_filename)
		self.controller = Controller
		self.__tui_items = 0
		self.__inghams_items = 0

	def scrape_and_save_data(self, source_company):
		self.__check_source_company(source_company)

		if source_company == 'inghams':
			url_list = self.__get_inghams_url_list()
			self.__inghams_items = len(url_list)
			for url in tqdm(url_list):
				url_html_obj = self.__get_driver_or_html(source_company, url)
				hotel_data = self.inghams_controller.get_inghams_data_fields(url_html_obj)
				self.inghams_controller.save_data.add_data(hotel_data)
		else:
			url_list = self.__get_tui_url_list()
			self.__tui_items = len(url_list)
			for url in tqdm(url_list):
				driver_obj = self.__get_driver_or_html(source_company, url)
				hotel_data = self.tui_controller.get_tui_data_fields(driver_obj)
				self.tui_controller.save_data.add_data(hotel_data)
			driver_obj.close()

	def read_data_and_enter_into_cms(self, source_company: str):
		self.__check_source_company(source_company)
		if source_company == 'inghams':
			headers, row_generator = self.inghams_controller.read_data.read_scraped_data()
			row = self.inghams_controller.read_data.get_scraped_data_row(row_generator)
			while tqdm(row, total=self.__inghams_items):
				row_dict = self.__create_row_dict(headers, row)
				self.inghams_controller.enter_inghams_data(row_dict)

		else:
			headers, row_generator = self.tui_controller.read_data.read_scraped_data()
			row = self.tui_controller.read_data.get_scraped_data_row(row_generator)
			while tqdm(row, total=self.__tui_items):
				row_dict = self.__create_row_dict(headers, row)
				self.tui_controller.enter_tui_data(row_dict)

	def navigate_to_add_page(self):
		self.controller.navigate_to_add_page()

	@staticmethod
	def __create_row_dict(headers: str, row: list[any]) -> dict[str, Union[str, dict[str, str], list[str]]]:
		row_dict = {header: col for header, col in headers, row}
		return row_dict

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
	main.navigate_to_add_page()

	# Scrape and save data for either site
	main.scrape_and_save_data('tui')
	main.scrape_and_save_data('inghams')

	# Add data to CMS
	main.read_data_and_enter_into_cms('tui')
	main.read_data_and_enter_into_cms('inghams')

	print('Complete! Please check site listings to ensure data is correct')


