import time
from typing import Union

from src.cms.cms_instance import CmsInstance
from src.cms.cms_operations import CmsOperations
from src.controller.crystal_controller import CrystalController
from src.controller.inghams_controller import InghamsController
from src.controller.tui_controller import TuiController
from src.models.hotel_model import Hotel
from src.util.hotel_data_helper import convert_json_list_to_hotel_obj_list


class CmsPipeline:

	def __init__(
			self,
			filename: str,
			company_name: str,
			cms_operations: CmsOperations
	):
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
			start_time = time.time()
			hotel = hotels.pop(0)
			try:
				self.cms_operations.populate_new_listing(
					source=self.company_name,
					hotel=hotel)
				time.sleep(1)
				self.cms_operations.save_listing()
			except Exception as e:
				if e == TimeoutError:
					hotels = hotels.extend([hotel])
					self.__delete_and_reinitialise_web_driver()
				hotel.failed_reason = str(e)
				self.__record_failed_run(
					company_controller=company_controller,
					hotel=hotel)
				self.cms_operations.save_listing(failed_run=True)
			run_time = time.time() - start_time

			num_items -= 1

	@staticmethod
	def __record_failed_run(
			hotel: Hotel,
			company_controller: Union[InghamsController, TuiController, CrystalController]
	):
		try:
			company_controller.read_data.read_data(failed_runs=True)
		except FileNotFoundError:
			company_controller.save_data.create_json_file(failed_cms_runs=True)

		company_controller.save_data.add_data(hotel, failed_cms_runs=True)

	def __delete_and_reinitialise_web_driver(self):
		"""The aim of this is to speed up long-running executions that slow due to the driver instance"""
		self.cms_operations.driver.quit()
		del self.cms_operations
		# TODO: this code is duplicated in main
		cms_instance = CmsInstance()
		web_driver = cms_instance.driver
		self.cms_operations = CmsOperations(
			web_driver=web_driver
		)
		self.cms_operations.instantiate_cms_add_page()
