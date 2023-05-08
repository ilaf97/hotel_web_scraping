from collections import Iterator
import time

from selenium.webdriver.chrome.webdriver import WebDriver

from src.controller.controller import BaseController
from src.models.hotel_model import Hotel
from src.tui.data_fields import TuiSiteData
from src.web_driver_factory import WebDriverFactory
from src.web_scraping.read_data import ReadData
from src.web_scraping.save_data import SaveWebScrapingData


class TuiController(BaseController):
	"""
	Class to handle TUI's data flows within the application.

	Params:
	- filename (str): name of file to save/read

	Attributes:
	- save_data (SaveData)
	- read_data (ReadData)
	- __filename (str) (Private)

	Methods:
	- read_scraped_data()
	- get_url_list()
	- get_inghams_data_fields()
	- enter_inghams_data()
	"""

	def __init__(self, filename: str, tui_site: str):
		BaseController.__init__(
			self,
			filename=filename,
			company_name=tui_site
		)
		self.__filename = filename
		self.save_data = SaveWebScrapingData(self.__filename, tui_site)
		self.read_data = ReadData(self.__filename, tui_site)
		self.company_name = tui_site

	@staticmethod
	def get_driver_obj(page_url: str) -> WebDriver:
		"""Returns a newly instantiated Selenium WebDriver object"""
		ex_html = WebDriverFactory(page_url)
		return ex_html.parse_html_selenium()

	def get_hotel_obj(self, driver: WebDriver) -> Hotel:
		"""Returns raw data scraped from a given TUI listing"""
		tui_site_data = TuiSiteData(driver)
		time.sleep(1)
		return self._create_hotel(tui_site_data)


