import json
from pathlib import Path


class ReadWebScrapingData:
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
		self.__ROOT_DIR = Path(__file__).parent.parent.parent

	def read_url_list(self) -> list[str]:
		"""Returns complete list of URLs contained in CSV as located by class attributes"""
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/urls.csv', 'r') as f:
			return f.readlines()

	def read_data(self, failed_cms_runs: bool = False, failed_scrape_runs: bool = False) -> tuple[any, list]:
		if failed_cms_runs:
			filename = self.filename + "-CMS-FAILS"
		elif failed_scrape_runs:
			filename = self.filename + "-SCRAPE-FAILS"
		else:
			filename = self.filename
		"""Returns headers and row iterator object from web scraping results CSV"""
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/json_data/{filename}.json', 'r') as f:
			return json.load(f)
