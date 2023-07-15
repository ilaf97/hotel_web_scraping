import logging
import os
from typing import Union

import timeout_decorator
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.cms.cms_listing_mapper import CmsListingMapper
from src.models.hotel_model import Hotel


class CmsOperations:

	def __init__(self, web_driver: WebDriver, company_name: str):
		self.driver = web_driver
		self.cms_listing_mapper = CmsListingMapper(self.driver, company_name)

	def instantiate_cms_add_page(self):
		"""Log in and navigate to the Add Accommodation page"""
		self.__log_in()
		self.navigate_to_add_page()

	def navigate_to_add_page(self):
		"""Navigate to the Add Accommodation page.
		If this is not possible, a NoSuchElementException will be raised"""
		try:
			self.driver.get("https://igetaway.co.uk/admin/pages/accommodationpage/add/")
		except NoSuchElementException as e:
			message = f'Cannot navigate to "Add Accommodation Page".\n{e}'
			logging.exception(message)
			raise NoSuchElementException(message)

	@timeout_decorator.timeout(300)
	def populate_new_listing(self, source: str, hotel: Hotel):
		self.cms_listing_mapper.add_hotel_name(hotel.name, hotel.slug)
		self.cms_listing_mapper.set_holiday_id()
		self.cms_listing_mapper.set_resort(hotel.resort)
		self.cms_listing_mapper.add_text_description_field(
			hotel.description,
			facility_descriptions=hotel.facilities_descriptions,
			description_type='description'
		)
		self.cms_listing_mapper.add_text_description_field(
			hotel.rooms,
			description_type='rooms'
		)
		self.cms_listing_mapper.add_text_description_field(
			hotel.facilities_descriptions['MEALS'],
			description_type='meals'
		)
		self.cms_listing_mapper.add_best_for(hotel.best_for)
		self.cms_listing_mapper.select_individual_facilities(hotel.individual_facilities)
		self.cms_listing_mapper.add_map_location(hotel.location)
		self.cms_listing_mapper.remove_airport_info()
		self.cms_listing_mapper.add_images(
			source_company=source,
			images=hotel.images
		)

	def save_listing(self, failed_run=False) -> Union[None, list[str]]:
		"""Save the listing and check that the save process is successful and the driver returns to a
		new add Accommodation page.
		If the listing cannot be saved or the user is not returned to the Add Accommodation page, a NoSuchElement
		exception will be raised"""
		if failed_run:
			self.navigate_to_add_page()
			return

		try:
			self.driver.find_element(By.XPATH, '//*[@id="accommodationpage_form"]/div/div[5]/input[2]').click()
		except NoSuchElementException as e:
			message = f'Cannot find/select "Save and Add Another" button\n{e}'
			logging.exception(message)
			raise NoSuchElementException(message)

		self.__check_listing_saved_successfully()

	def __check_listing_saved_successfully(self):
		try:
			WebDriverWait(self.driver, 2).until_not(
				EC.visibility_of_element_located(
					(By.XPATH, '//*[@id="accommodationpage_form"]/div/p')
				))
		except TimeoutException:
			errors = ''
			error_list = self.driver.find_element(By.CLASS_NAME, 'errorlist')
			error_list_items = error_list.find_elements(By.TAG_NAME, 'li')
			for error in error_list_items:
				errors = errors + error.text.strip() + '\n'
			raise Exception(errors)

	def __log_in(self):
		"""Log in to the CMS using username and password environment variables.
		If login fails due to not being to select components or enter text, a NoSuchElementException will be raised.
		Note: exceptions resulting from invalid credentials are not handled"""
		try:
			cms_username_field = self.driver.find_element(By.ID, 'id_username')
			cms_password_field = self.driver.find_element(By.ID, 'id_password')

			cms_username_field.send_keys(os.getenv('username'))
			cms_password_field.send_keys(os.getenv('password'))
			cms_password_field.send_keys(Keys.ENTER)
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot log in to the site.\n{e}')

