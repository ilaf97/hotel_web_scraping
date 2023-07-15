import traceback
from typing import Union

from selenium.common import NoSuchElementException

from src.crystal_ski.crystal_data_fields import CrystalSiteData
from src.inghams.inghams_data_fields import InghamsSiteData
from src.models.hotel_model import Hotel, ScrapeFailHotel
from src.tui.tui_data_fields import TuiSiteData
from src.web_scraping.exception_handler import exception_handler
from src.web_scraping.read_data import ReadWebScrapingData
from src.web_scraping.save_data import SaveWebScrapingData


class BaseController:
	"""
	Class to handle data flows within the application.

	Attributes:
	- cms_input (CmsInput)

	Methods:
	- naviagte_to_add_page()
	- _save_listing() (Protected)
	- _enter_data_into_cms() (Protected)
	"""

	def __init__(
			self,
			filename: str,
			company_name: str
	):
		self.filename = filename
		self.company_name = company_name
		self.save_data = SaveWebScrapingData(self.filename, company_name)
		self.read_data = ReadWebScrapingData(self.filename, company_name)

	@staticmethod
	def _create_hotel(site_data: Union[InghamsSiteData, TuiSiteData, CrystalSiteData]) -> Union[Hotel, ScrapeFailHotel]:
		hotel_name = site_data.get_name()
		try:
			return Hotel(
				name=hotel_name,
				slug=site_data.generate_slug(hotel_name),
				description=site_data.get_description(),
				resort=site_data.get_resort(),
				best_for=site_data.get_best_for(),
				rooms=site_data.get_rooms(),
				location=site_data.get_location(),
				individual_facilities=site_data.get_individual_facilities(),
				facilities_descriptions=site_data.get_facilities_descriptions(),
				images=site_data.get_images(),
			)
		except Exception as e:
			traceback.print_exc(limit=1)
			exception_handler(str(site_data))
			return ScrapeFailHotel(
				name=hotel_name,
				url=(site_data.html_object.namespace
					 if isinstance(site_data, InghamsSiteData)
					 else site_data.driver.current_url),
				failed_reason=str(e.msg if isinstance(e, NoSuchElementException) else str(e))
			)

	def create_json_file(self):
		"""Create file into which scraped data can be saved"""
		self.save_data.create_json_file()

	def get_url_list(self) -> list[str]:
		"""Returns all URLs of listings to scrape"""
		return self.read_data.read_url_list()
