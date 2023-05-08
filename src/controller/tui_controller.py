from collections import Iterator
import time

from selenium.webdriver.chrome.webdriver import WebDriver

from src.controller.controller import BaseController
from src.tui.data_fields import TuiDataFields
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

	def __init__(self, filename: str, web_driver: WebDriver, tui_site: str):
		BaseController.__init__(
			self,
			web_driver=web_driver,
			filename=filename,
			company_name=tui_site
		)
		self.__filename = filename
		self.save_data = SaveWebScrapingData(self.__filename, tui_site)
		self.read_data = ReadData(self.__filename, tui_site)

	@staticmethod
	def get_driver_obj(page_url: str) -> WebDriver:
		"""Returns a newly instantiated Selenium WebDriver object"""
		ex_html = WebDriverFactory(page_url)
		return ex_html.parse_html_selenium()

	def get_data_fields_json(self, driver: WebDriver) -> dict[any]:
		"""Returns raw data scraped from a given TUI listing"""
		data_fields = TuiDataFields(driver)
		time.sleep(1)
		return self._create_data_fields_dict(data_fields)


