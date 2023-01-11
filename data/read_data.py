import csv
from pathlib import Path
from typing import Iterator


class ReadData:
	"""
	Class for reading data from CSV format into Python variables.

	Params:
	- filename (str)
	- source_company (str)

	Attributes:
	- filename (str)
	- source_company (str)
	- __ROOT_DIR (_P) (Private)

	Methods:
	- read_url_list()
	- read_scraped_data()
	- get_scraped_data_row()
	"""

	def __init__(self, filename: str, source_company: str):
		self.filename = filename
		self.source_company = source_company
		self.__ROOT_DIR = Path(__file__).parent.parent

	def read_url_list(self) -> list[str]:
		"""Returns complete list of URLs contained in CSV as located by class attributes"""
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/urls.csv', 'r') as f:
			return f.readlines()

	def read_scraped_data(self) -> Iterator[any]:
		"""Returns headers and row iterator object from web scraping results CSV"""
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/{self.filename}.csv', 'r') as f:
			csvreader = csv.reader(f)
			headers = next(csvreader)
			return headers, csvreader

	@staticmethod
	def get_scraped_data_row(csv_generator: Iterator[any]):
		"""Returns next row in iterator object or None if iterator is empty"""
		try:
			return next(csv_generator)
		except StopIteration:
			return None

