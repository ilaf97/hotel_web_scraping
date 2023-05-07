import os
import logging
from typing import Union

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import NoSuchElementException
from src.cms.html_extraction import WebDriverFactory


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
		self.__username = os.getenv('username')
		self.__password = os.getenv('password')
		self.__admin_url = 'https://admin:letmeaccessplease!@igetaway.co.uk/admin/'
		self.driver = self.__instantiate_site_driver()

	def __instantiate_site_driver(self) -> WebDriver:
		"""Returns the Seleium site driver for the CMS"""
		extract_html = WebDriverFactory(self.__admin_url)
		driver = extract_html.parse_html_selenium()
		return driver

	def log_in(self):
		"""Log in to the CMS using username and password environment variables.
		If login fails due to not being to select components or enter text, a NoSuchElementException will be raised.
		Note: exceptions resulting from invalid credentials are not handled"""
		try:
			cms_username_field = self.driver.find_element(By.ID, 'id_username')
			cms_password_field = self.driver.find_element(By.ID, 'id_password')

			cms_username_field.send_keys(self.__username)
			cms_password_field.send_keys(self.__password)
			cms_password_field.send_keys(Keys.ENTER)
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot log in to the site.\n{e}')
