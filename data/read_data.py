import json
from pathlib import Path


class ReadData:
	"""
	Class for reading data from JSON or CSV format into Python variables.

	Params:
	- filename (str): the : the name of the company from which the data originates

	Attributes:
	- filename (str)
	- source_company (str)
	- __ROOT_DIR (_P) (Private)

	Methods:
	- read_url_list()
	- read_data()
	"""

	def __init__(self, filename: str, source_company: str):
		self.filename = filename
		self.source_company = source_company
		self.__ROOT_DIR = Path(__file__).parent.parent

	def read_url_list(self) -> list[str]:
		"""Returns complete list of URLs contained in CSV as located by class attributes"""
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/urls.csv', 'r') as f:
			return f.readlines()

	def read_data(self) -> tuple[any, list]:
		"""Returns headers and row iterator object from web scraping results CSV"""
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/{self.filename}.json', 'r') as f:
			return json.load(f)

