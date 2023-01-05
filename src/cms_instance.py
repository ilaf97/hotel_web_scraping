import os
from src.html_extraction import ExtractHtml
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import NoSuchElementException


class CmsInstance:

	def __init__(self):
		self.__admin_url = 'http://35.178.65.128:8001/admin/'
		self.__username = os.getenv('username')
		self.__password = os.getenv('password')
		self.__driver = self.__instantiate_site_driver()

	def add_hotel_name(self, name: str):
		try:
			self.__driver.find_element(By.ID, 'id_title').send_keys(name)
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot find/edit "Title" field\n{e}')

	def set_category_to_hotel(self):
		try:
			self.__driver.find_element(By.ID, 'id_category').click()
			self.__driver.find_element(By.XPATH, '//*[@id="id_category"]/option[3]').click()
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot find category field/change category\n{e}')

	def add_text_description_field(self, text: str, description_type: str):
		if description_type == 'description':
			desc_field_no = 'one'
		elif description_type == 'rooms':
			desc_field_no = 'two'
		elif description_type == 'meals':
			desc_field_no = 'three'
		else:
			raise ValueError(f'description_type can only have values "description", "rooms" or "meals": '
							 f'invalid value passed ({description_type})')

		try:
			description_field = self.__driver.find_element(By.ID, f'id_description_section_{desc_field_no}_ifr')
			description_field.send_keys(text)
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot find description field/add description\n{e}')

	def instantiate_cms_add_page(self):
		self.__log_in()
		self.__navigate_to_add_page()

	def __log_in(self):
		try:
			username_field = self.__driver.find_element(By.ID, 'id_username')
			password_field = self.__driver.find_element(By.ID, 'id_password')
			username_field.send_keys(self.__username)
			password_field.send_keys(self.__password)
			password_field.send_keys(Keys.ENTER)
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot log in to the site.\n{e}')

	def __navigate_to_add_page(self):
		try:
			self.__driver.find_element(By.XPATH, '//*[@id="content-main"]/div[3]/table/tbody/tr[5]/th/a').click()
			self.__driver.find_element(By.XPATH, '//*[@id="content-main"]/ul/li/a').click()
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot navigate to "Add Accomodation Page".\n{e}')

	def __instantiate_site_driver(self):
		extract_html = ExtractHtml(self.__admin_url)
		driver = extract_html.parse_html_selenium()
		return driver
