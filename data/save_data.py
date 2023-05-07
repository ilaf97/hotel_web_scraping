import json
from pathlib import Path


class SaveWebScrapingData:
	"""
	Class for saving data into JSON format.

	Params:
	- filename (str): the name of the file to save
	- company (str): the name of the company from which the data originates

	Attributes:
	- filename (str)
	- source_company (str)
	- ROOT_DIR (_P) (Private)

	Methods:
	- create_file()
	- add_data()
	"""

	def __init__(self, filename: str, source_company: str):
		self.filename = filename
		self.source_company = source_company
		self.__ROOT_DIR = Path(__file__).parent.parent

	def create_json_file(self, failed_runs: bool = False):
		filename = self.__fail_check(failed_runs)
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/json_data/{filename}.json', 'w') as f:
			json.dump([], f)

	def add_data(self, hotel_data: dict[any], failed_runs: bool = False):
		filename = self.__fail_check(failed_runs)
		"""Add data to the CSV file associated with the class attribute data"""
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/json_data/{filename}.json', 'r+') as f:
			data_list = json.load(f)
			data_list.append(hotel_data)
			f.seek(0)
			json.dump(data_list, f)

	def __fail_check(self, failed_bool: bool) -> str:
		return self.filename + "-FAILS" if failed_bool else self.filename
