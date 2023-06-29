import os
import time

from selenium.webdriver.chrome.webdriver import WebDriver

from src.web_driver_factory import WebDriverFactory


class CmsInstance:
	"""
	Class to initialise CMS instances.

	Attributes:
	- driver (WebDriver)
	- __admin_url (str) = 'https://igetaway.co.uk/admin/': url of CMS (Private)
	- __username (str): login username (Private)
	- __password (str): login password (Private)

	Methods:
	- __instantiate_site_driver() (Private)
	- __log_in() (Private)
	"""

	def __init__(self):
		self.__browser_username = os.getenv('browser_username')
		self.__browser_password = os.getenv('browser_password')
		self.__admin_url = f'https://{self.__browser_username}:{self.__browser_password}@igetaway.co.uk/admin/'
		time.sleep(2)
		self.driver = self.__instantiate_site_driver()

	def __instantiate_site_driver(self) -> WebDriver:
		"""Returns the Selenium site driver for the CMS"""
		extract_html = WebDriverFactory(self.__admin_url)
		driver = extract_html.parse_html_selenium()
		return driver

