import csv
from pathlib import Path


class SaveData:

	def __init__(self, filename: str, company: str):
		self.filename = filename
		self.company = company
		self.__ROOT_DIR = Path(__file__).parent.parent

	def create_file(self):
		with open(f'{self.__ROOT_DIR}/data/{self.company}/{self.filename}.csv', 'w') as f:
			col_headers = [
				'Name',
				'Description',
				'Rooms',
				'Location',
				'Facilities',
				'Food & Drink',
				'Images'
			]
			if self.company == 'inghams':
				col_headers.append('Excursions')
			writer = csv.DictWriter(f, fieldnames=col_headers)
			writer.writeheader()

	def add_data(self, hotel_data: list[str]):
		with open(f'{self.__ROOT_DIR}/data/{self.company}/{self.filename}.csv', 'a') as f:
			writer = csv.writer(f)
			writer.writerow([hotel_data[i] for i in range(len(hotel_data))])
