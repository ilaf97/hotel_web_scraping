from typing import Iterator, Union
from selenium.webdriver.chrome.webdriver import WebDriver

from src.inghams.data_fields import InghamsDataFields
from src.web_scraping.save_data import SaveWebScrapingData
from src.web_scraping.read_data import ReadData
from src.tui.data_fields import TuiDataFields
from src.cms.cms_listing_mapper import CmsListingMapper


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
			web_driver: WebDriver,
			filename: str,
			company_name: str
	):
		self.cms_listing_mapper = CmsListingMapper(web_driver)
		self.filename = filename
		self.company_name = company_name
		self.save_data = SaveWebScrapingData(self.filename, company_name)
		self.read_data = ReadData(self.filename, company_name)

	@staticmethod
	def _create_data_fields_dict(data_fields: Union[InghamsDataFields, TuiDataFields]) -> dict[any]:
		data_fields_dict = {
			"hotel_name": data_fields.get_name(),
			"description": data_fields.get_description(),
			'best_for': data_fields.get_best_for(),
			"rooms": data_fields.get_rooms(),
			"location": data_fields.get_location(),
			"facilities": data_fields.get_facilities(),
			"meals": data_fields.get_meals(),
			"images": data_fields.get_images(),
		}
		return data_fields_dict

	def _enter_data_into_cms(self, source: str, hotel_attributes: dict[str, any]):
		self.cms_listing_mapper.add_hotel_name(hotel_attributes['hotel_name'])
		self.cms_listing_mapper.set_holiday_id()
		self.cms_listing_mapper.set_resort(hotel_attributes.get('resort'))
		self.cms_listing_mapper.add_text_description_field(hotel_attributes['description'], 'description')
		self.cms_listing_mapper.add_text_description_field(hotel_attributes['rooms'], 'rooms')
		self.cms_listing_mapper.add_text_description_field(hotel_attributes['meals'], 'meals')
		self.cms_listing_mapper.add_best_for(hotel_attributes['best_for'])
		self.cms_listing_mapper.select_facilities(hotel_attributes['facilities'])
		self.cms_listing_mapper.add_map_location(hotel_attributes['location'])
		self.cms_listing_mapper.add_images(source_company=source, images=hotel_attributes['images'])

	def create_json_file(self):
		"""Create file into which scraped data can be saved"""
		self.save_data.create_json_file()

	def read_scraped_data(self) -> list[str] and Iterator[any]:
		"""Returns column headers and a row iterator object"""
		return self.read_data.read_data()

	def get_url_list(self) -> list[str]:
		"""Returns all URLs of listings to scrape"""
		return self.read_data.read_url_list()

	def enter_data(self, hotel_attributes: dict[str, any]):
		"""Enter and save accommodation data into the CMS"""
		self._enter_data_into_cms(self.company_name, hotel_attributes)




