import json
from pathlib import Path


class SaveData:
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

	def create_json_file(self):
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/{self.filename}.json', 'w') as f:
			json.dump([], f)

	def add_data(self, hotel_data: dict[any]):
		"""Add data to the CSV file associated with the class attribute data"""
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/{self.filename}.json', 'r+') as f:
			data_list = json.load(f)
			data_list.append(hotel_data)
			f.seek(0)
			json.dump(data_list, f)
