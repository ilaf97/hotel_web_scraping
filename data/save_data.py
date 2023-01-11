import csv
from pathlib import Path


class SaveData:
	"""
	Class for saving data into CSV format.

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

	def create_file(self):
		"""Create a new empty CSV file with  predetermined headers"""
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/{self.filename}.csv', 'w') as f:
			col_headers = [
				'Name',
				'Description',
				'Rooms',
				'Location',
				'Facilities',
				'Food & Drink',
				'Images'
			]
			if self.source_company == 'inghams':
				col_headers.append('Excursions')
			writer = csv.DictWriter(f, fieldnames=col_headers)
			writer.writeheader()

	def add_data(self, hotel_data: list[str]):
		"""Add data to the CSV file associated with the class attribute data"""
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/{self.filename}.csv', 'a') as f:
			writer = csv.writer(f, delimiter='|')
			writer.writerow([hotel_data[i] for i in range(len(hotel_data))])
