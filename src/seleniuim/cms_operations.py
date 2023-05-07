import logging
from typing import Union

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.seleniuim.cms_instance import CmsInstance


class CmsOperations(CmsInstance):

	def instantiate_cms_add_page(self):
		"""Log in and navigate to the Add Accommodation page"""
		self._log_in()
		self.navigate_to_add_page()

	def navigate_to_add_page(self, from_listing_page=False):
		"""Navigate to the Add Accommodation page.
		If this is not possible, a NoSuchElementException will be raised"""
		if from_listing_page:
			id = "nav-sidebar"
		else:
			id = "content-main"
		try:
			self.driver.find_element(By.XPATH, f'//*[@id="{id}"]/div[3]/table/tbody/tr[5]/th/a').click()
			self.driver.find_element(By.XPATH, '//*[@id="content-main"]/ul/li/a').click()
		except NoSuchElementException as e:
			message = f'Cannot navigate to "Add Accommodation Page".\n{e}'
			logging.exception(message)
			raise NoSuchElementException(message)

	def save_listing(self, failed_run=False) -> Union[None, list[str]]:
		"""Save the listing and check that the save process is successful and the driver returns to a
		new add Accomodation page.
		If the listing cannot be saved or the user is not returned to the Add Accommodation page, a NoSuchElement
		exception will be raised"""
		if failed_run:
			self.navigate_to_add_page(from_listing_page=True)
			return
		try:
			self.driver.find_element(By.XPATH, '//*[@id="accommodationpage_form"]/div/div[4]/input[2]').click()
		except NoSuchElementException as e:
			message = f'Cannot find/select "Save and Add Another" button\n{e}'
			logging.exception(message)
			raise NoSuchElementException(message)

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
		return


