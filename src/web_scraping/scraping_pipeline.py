from typing import Union

from tqdm import tqdm

from src.controller.crystal_controller import CrystalController
from src.controller.inghams_controller import InghamsController
from src.controller.tui_controller import TuiController


class ScrapingPipeline:

	def __init__(
			self,
			company_name,
			filename,
	):
		self.company_name = company_name
		self.filename = filename

	def scrape_and_save_data(self):
		if self.company_name == 'inghams':
			self.controller = InghamsController(self.filename)

		elif self.company_name == "tui":
			self.controller = TuiController(self.filename)

		elif self.company_name == "crystal_ski":
			self.controller = CrystalController(self.filename)

		else:
			raise ValueError(f"Company name is invalid ({self.company_name})")

		self.__scrape_data_from_urls(
			url_list=self.controller.get_url_list(),
			company_controller=self.controller
		)

	@staticmethod
	def __scrape_data_from_urls(
			url_list: list[str],
			company_controller: Union[InghamsController, TuiController]
	):
		company_controller.create_json_file()
		for url in tqdm(url_list):
			url_web_driver = company_controller.get_driver_obj(url.strip())
			hotel = company_controller.get_hotel_obj(url_web_driver)
			company_controller.save_data.add_data(hotel)
			del hotel

