import json
from dataclasses import asdict
from pathlib import Path
from typing import Union

from src.models.hotel_model import Hotel, ScrapeFailHotel


class SaveWebScrapingData:
	"""Class for saving data into JSON format"""

	def __init__(self, filename: str, source_company: str):
		self.filename = filename
		self.source_company = source_company.lower()
		self.__ROOT_DIR = Path(__file__).parent.parent.parent

	def create_json_file(self, failed_cms_runs: bool = False, failed_scrape_runs: bool = False):
		assert not all([failed_scrape_runs, failed_cms_runs])
		filename = self.__fail_check(failed_cms_runs, failed_scrape_runs)
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/json_data/{filename}.json', 'w') as f:
			json.dump([], f)

	def add_data(self, hotel: Union[Hotel, ScrapeFailHotel], failed_cms_runs: bool = False,
				 failed_scrape_runs: bool = False):
		assert not all([failed_scrape_runs, failed_cms_runs])
		filename = self.__fail_check(failed_cms_runs, failed_scrape_runs)
		if failed_cms_runs or failed_scrape_runs:
			hotel = {
				"name": hotel.name,
				"failed reason": hotel.failed_reason,
				"url": hotel.url if isinstance(hotel, ScrapeFailHotel) else ""
			}
		"""Add data to the CSV file associated with the class attribute data"""
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/json_data/{filename}.json', 'r+') as f:
			data_list = json.load(f)
			data_list.append(asdict(hotel) if not any([failed_cms_runs, failed_scrape_runs]) else hotel)
			f.seek(0)
			json.dump(data_list, f)

	def __fail_check(self, failed_cms_bool: bool, failed_scrape_bool: bool) -> str:
		if failed_cms_bool:
			return self.filename + "-CMS-FAILS"
		elif failed_scrape_bool:
			return self.filename + "-SCRAPE-FAILS"
		else:
			return self.filename
