import time

from selenium.webdriver.chrome.webdriver import WebDriver

from src.controller.controller import BaseController
from src.models.hotel_model import Hotel
from src.tui.tui_data_fields import TuiSiteData
from src.web_driver_factory import WebDriverFactory
from src.web_scraping.read_data import ReadWebScrapingData
from src.web_scraping.save_data import SaveWebScrapingData

company_name = "Tui"


class TuiController(BaseController):

	def __init__(self, filename: str):
		BaseController.__init__(
			self,
			filename=filename,
			company_name=company_name
		)
		self.__filename = filename
		self.save_data = SaveWebScrapingData(self.__filename, company_name)
		self.read_data = ReadWebScrapingData(self.__filename, company_name)

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


