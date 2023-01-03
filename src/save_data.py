import csv
from pathlib import Path


class SaveData:

	def __init__(self, filename: str):
		self.filename = filename
		self.__ROOT_DIR = Path(__file__).parent.parent


	def create_file(self):
		with open(f'{self.__ROOT_DIR}/data/{self.filename}.csv', 'w') as f:
			writer = csv.DictWriter(
				f,
				fieldnames=
				['Name',
				 'Description',
				 'Rooms',
				 'Location',
				 'Facilities',
				 'Food & Drink',
				 'Excursions',
				 'Images']
			)
			writer.writeheader()

	def add_data(self, hotel_data: list[str]):
		with open(f'{self.__ROOT_DIR}/data/{self.filename}.csv', 'a') as f:
			writer = csv.writer(f)
			writer.writerow([
				hotel_data[0],
				hotel_data[1],
				hotel_data[2],
				hotel_data[3],
				hotel_data[4],
				hotel_data[5],
				hotel_data[6],
				hotel_data[7]
			])
