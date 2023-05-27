import time
from typing import Union

from selenium.webdriver.chrome.webdriver import WebDriver

from src.cms.cms_operations import CmsOperations
from src.controller.crystal_controller import CrystalController
from src.controller.inghams_controller import InghamsController
from src.controller.tui_controller import TuiController
from src.models.hotel_model import Hotel
from src.util.hotel_data_helper import convert_json_list_to_hotel_obj_list


class CmsPipeline:

	def __init__(
			self,
			web_driver: WebDriver,
			filename: str,
			company_name: str,
			cms_operations: CmsOperations
	):
		self.driver = web_driver
		self.filename = filename
		self.company_name = company_name
		self.cms_operations = cms_operations

		if company_name == 'inghams':
			self.controller = InghamsController(filename)
		elif company_name == "tui":
			self.controller = TuiController(filename)
		elif company_name == "crystal_ski":
			self.controller = CrystalController(filename)
		else:
			raise ValueError(f"Invalid company name passed ({company_name})")

	def read_data_and_enter_into_cms(self) -> Union[InghamsController, TuiController, CrystalController]:
		self.__iterate_through_hotels(self.controller)
		return self.controller

	@staticmethod
	def check_for_failed_runs(company_controller: Union[InghamsController, TuiController]) -> bool:
		try:
			company_controller.read_data.read_data(failed_runs=True)
			return True
		except FileNotFoundError:
			return False

	def __iterate_through_hotels(
			self, company_controller: Union[InghamsController, TuiController, CrystalController]):
		hotels_json = company_controller.read_data.read_data()
		hotels = convert_json_list_to_hotel_obj_list(hotels_json)
		num_items = len(hotels)

		while num_items:
			hotel = hotels.pop(0)
			try:
				self.cms_operations.populate_new_listing(
					source=self.company_name,
					hotel=hotel)
				time.sleep(1)
				self.cms_operations.save_listing()
			except Exception as e:
				hotel.failed_reason = e.__str__()
				self.__record_failed_run(
					company_controller=company_controller,
					hotel=hotel)
				self.cms_operations.save_listing(failed_run=True)

			num_items -= 1

	@staticmethod
	def __record_failed_run(
			hotel: Hotel,
			company_controller: Union[InghamsController, TuiController, CrystalController]
	):
		try:
			company_controller.read_data.read_data(failed_runs=True)
		except FileNotFoundError:
			company_controller.save_data.create_json_file(failed_runs=True)

		company_controller.save_data.add_data(hotel, failed_runs=True)