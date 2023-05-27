import json
from dataclasses import asdict
from pathlib import Path

from src.models.hotel_model import Hotel


class SaveWebScrapingData:
	"""Class for saving data into JSON format"""

	def __init__(self, filename: str, source_company: str):
		self.filename = filename
		self.source_company = source_company
		self.__ROOT_DIR = Path(__file__).parent.parent.parent

	def create_json_file(self, failed_runs: bool = False):
		filename = self.__fail_check(failed_runs)
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/json_data/{filename}.json', 'w') as f:
			json.dump([], f)

	def add_data(self, hotel: Hotel, failed_runs: bool = False):
		filename = self.__fail_check(failed_runs)
		if failed_runs:
			hotel = {
				"name": hotel.name,
				"failed reason": hotel.failed_reason
			}
		"""Add data to the CSV file associated with the class attribute data"""
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/json_data/{filename}.json', 'r+') as f:
			data_list = json.load(f)
			data_list.append(asdict(hotel) if not failed_runs else hotel)
			f.seek(0)
			json.dump(data_list, f)

	def __fail_check(self, failed_bool: bool) -> str:
		return self.filename + "-FAILS" if failed_bool else self.filename
