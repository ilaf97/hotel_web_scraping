import os

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import NoSuchElementException

from src.html_extraction import ExtractHtml


class CmsInstance:
	"""
	Class to initialise and manage behaviour of CMS instances.

	Attributes:
	- driver (WebDriver)
	- __admin_url (str) = 'https://igetaway.co.uk/admin/': url of CMS (Private)
	- __username (str): login username (Private)
	- __password (str): login password (Private)

	Methods:
	- instantiate_cms_add_page()
	- navigate_to_add_page()
	- save_listing()
	- __instantiate_site_driver() (Private)
	- __log_in() (Private)
	"""

	def __init__(self):
		self.__admin_url = 'https://igetaway.co.uk/admin/'
		self.__username = os.getenv('username')
		self.__password = os.getenv('password')
		self.driver = self.__instantiate_site_driver()

	def instantiate_cms_add_page(self):
		"""Log in and navigate to the Add Accommodation page"""
		self.__log_in()
		self.navigate_to_add_page()

	def navigate_to_add_page(self):
		"""Navigate to the Add Accommodation page.
		If this is not possible, a NoSuchElementException will be raised"""
		try:
			self.driver.find_element(By.XPATH, '//*[@id="content-main"]/div[3]/table/tbody/tr[5]/th/a').click()
			self.driver.find_element(By.XPATH, '//*[@id="content-main"]/ul/li/a').click()
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot navigate to "Add Accommodation Page".\n{e}')

	def save_listing(self):
		"""Save the listing and check that the save process is successful and the driver returns to a
		new add Accomodation page.
		If the listing cannot be saved or the user is not returned to the Add Accommodation page, a NoSuchElement
		exception will be raised"""
		try:
			self.driver.find_element(By.XPATH, '//*[@id="accommodationpage_form"]/div/div[4]/input[2]').click()
			# Assert that the error banner is not shown
			try:
				self.driver.find_element(By.XPATH, '//*[@id="accommodationpage_form"]/div/p')
			except NoSuchElementException:
				pass

			assert self.driver.find_element(By.XPATH, '//*[@id="main"]/div/ul/li').is_displayed()
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot find/select "Save and Add Another" button\n{e}')
		except AssertionError as e:
			raise AssertionError(f'Data is missing and listing cannot be saved\n{e}')

	def __instantiate_site_driver(self) -> WebDriver:
		"""Returns the Seleium site driver for the CMS"""
		extract_html = ExtractHtml(self.__admin_url)
		driver = extract_html.parse_html_selenium()
		return driver

	def __log_in(self):
		"""Log in to the CMS using username and password environment variables.
		If login fails due to not being to select components or enter text, a NoSuchElementException will be raised.
		Note: exceptions resulting from invalid credentials are not handled"""
		try:
			username_field = self.driver.find_element(By.ID, 'id_username')
			password_field = self.driver.find_element(By.ID, 'id_password')
			username_field.send_keys(self.__username)
			password_field.send_keys(self.__password)
			password_field.send_keys(Keys.ENTER)
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot log in to the site.\n{e}')
