import os

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import NoSuchElementException

from src.html_extraction import ExtractHtml


class CmsInstance:

	def __init__(self):
		self.__admin_url = 'http://35.178.65.128:8001/admin/'
		self.__username = os.getenv('username')
		self.__password = os.getenv('password')
		self.driver = self.__instantiate_site_driver()
		self.__log_in()
		self.navigate_to_add_page()

	def instantiate_cms_add_page(self):
		self.__log_in()
		self.navigate_to_add_page()

	def navigate_to_add_page(self):
		try:
			self.driver.find_element(By.XPATH, '//*[@id="content-main"]/div[3]/table/tbody/tr[5]/th/a').click()
			self.driver.find_element(By.XPATH, '//*[@id="content-main"]/ul/li/a').click()
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot navigate to "Add Accommodation Page".\n{e}')

	def save_listing(self):
		try:
			self.driver.find_element(By.XPATH, '//*[@id="accommodationpage_form"]/div/div[4]/input[2]').click()
			assert not self.driver.find_element(By.XPATH, '//*[@id="accommodationpage_form"]/div/p').is_displayed()
			assert self.driver.find_element(By.XPATH, '//*[@id="main"]/div/ul/li').is_displayed()
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot find/select "Save and Add Another" button\n{e}')
		except AssertionError as e:
			raise AssertionError(f'Data is missing and listing cannot be saved\n{e}')

	def __instantiate_site_driver(self) -> WebDriver:
		extract_html = ExtractHtml(self.__admin_url)
		driver = extract_html.parse_html_selenium()
		return driver

	def __log_in(self):
		try:
			username_field = self.driver.find_element(By.ID, 'id_username')
			password_field = self.driver.find_element(By.ID, 'id_password')
			username_field.send_keys(self.__username)
			password_field.send_keys(self.__password)
			password_field.send_keys(Keys.ENTER)
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot log in to the site.\n{e}')
