from abc import ABC, abstractmethod

from bs4 import BeautifulSoup


class AbstractCompanyController(ABC):

	@abstractmethod
	def create_json_file(self):
		pass

	@abstractmethod
	def read_scraped_data(self):
		pass

	@abstractmethod
	def get_url_list(self):
		pass

	@staticmethod
	@abstractmethod
	def get_driver_obj(page_url: str):
		pass

	@abstractmethod
	def get_data_fields_json(self, html_obj: BeautifulSoup):
		pass

	@abstractmethod
	def enter_data(self, hotel_attributes: dict[str, any]):
		pass
