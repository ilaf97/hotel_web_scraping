import json
import logging
import random
from typing import Union, Optional

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from src.util.image_handler import WebImageHandler, LocalImageHandler


class CmsListingMapper:
	"""
	Class handling input into CMS data fields.
	It maps data from the hotel properties to the correct CMS fields.
	"""

	def __init__(self, web_driver: WebDriver, company_name: str):
		self.driver = web_driver
		self.company_name = company_name
		self._web_image_handler = \
			WebImageHandler(driver=self.driver, source_company=company_name)
		self._local_image_handler = LocalImageHandler(source_company=company_name)

	def add_hotel_name(self, name: str, slug: Optional[str]):
		try:
			self.driver.find_element(By.ID, 'id_title').send_keys(name)
			if slug:
				self.driver.find_element(By.ID, 'id_slug').send_keys(slug)
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot find/edit "Title" field\n{e}')
		self.set_category_to_hotel()

	def set_holiday_id(self):
		holiday_id = str(random.randint(1, 999999)).zfill(6)
		self.driver.find_element(By.ID, 'id_holiday_id').send_keys(holiday_id)

	def set_resort(self, resort_name: Optional[str]):
		if resort_name:
			try:
				resort_name_drop_down_format = resort_name.replace(" ", "-").replace("'", "").replace("`", "").lower()
				self.driver.find_element(
					By.XPATH,
					f'//*[@id="id_resort"]'
				).send_keys(resort_name_drop_down_format)

			except NoSuchElementException as e:
				logging.warning(f'Cannot find resort {resort_name} in list\n{e}')

	def set_category_to_hotel(self):
		try:
			self.driver.find_element(By.ID, 'id_category').click()
			self.driver.find_element(By.XPATH, '//*[@id="id_category"]/option[3]').click()
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot find category field/change category\n{e}')

	def add_text_description_field(
			self,
			text: str,
			description_type: str,
			facility_descriptions: Optional[dict[str, str]] = None
	):

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
			description_field = self.driver.find_element(By.ID, f'id_description_section_{desc_field_no}_ifr')
			self.driver.switch_to.frame(description_field)
			text_area = self.driver.find_element(By.ID, 'tinymce')
			text_area.send_keys(Keys.CONTROL + "a")
			text_area.send_keys(Keys.DELETE)
			if description_type in ['rooms', 'meals']:
				text_area.send_keys(description_type.capitalize() + '\n\n' + text)
			else:
				facility_text = ''
				for facility, description in facility_descriptions.items():
					if facility != "MEALS":
						facility_text = facility_text + '\n\n\n' + facility + '\n\n' + description
				text_area.send_keys(text + facility_text)
			self.driver.switch_to.default_content()
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot find description field/add description\n{e}')

	def add_best_for(self, best_for_dict: dict[str]):
		best_for_str = ''

		if best_for_dict is None:
			best_for_str = 'Coming soon!'
		else:
			for key, value in best_for_dict.items():
				best_for_str = best_for_str + f'{key.capitalize()}: {value}\n'

		try:
			description_field = self.driver.find_element(By.ID, 'id_best_for_list_ifr')
			self.driver.switch_to.frame(description_field)
			text_area = self.driver.find_element(By.ID, 'tinymce')
			text_area.send_keys(best_for_str)
			self.driver.switch_to.default_content()
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot find best for field/add best for\n{e}')

	def remove_airport_info(self):
		try:
			self.driver.find_element(
				By.CSS_SELECTOR,
				f'#accommodationdepartingarrival_set-0 > td.delete > div > a'
			).click()
		except NoSuchElementException as e:
			raise NoSuchElementException(f"Cannot find button to delete airport info\n{e}")

	def select_individual_facilities(self, facilities: list[str]):
		options_selected = []
		options_to_select = []

		with open('src/util/facility_mapping.json', 'r') as f:
			hotel_facility_mapping = json.load(f)

		for facility in facilities:
			for key in hotel_facility_mapping.keys():
				if key in facility.lower():
					options_to_select.append(int(hotel_facility_mapping[key]))
					options_selected.append(key)

		options_to_select.sort(reverse=True)
		for option in options_to_select:
			self.__click_correct_facility_option_obj(option)

	def add_map_location(self, location: dict[str: Union[str, list[int]]]):
		lat = location['lat_long'][0]
		lon = location['lat_long'][1]
		map_iframe = f'<iframe ' \
					 	f'src="https://www.google.com/maps?q={lat},{lon}&hl=es&z=14&amp;output=embed" ' \
					 	f'width="600" ' \
					 	f'height="450" ' \
					 	f'style="border:0;" ' \
					 	f'allowfullscreen="" ' \
					 	f'loading="lazy" ' \
					 	f'referrerpolicy="no-referrer-when-downgrade">' \
					 f'</iframe>'
		map_iframe_field = self.driver.find_element(By.ID, 'id_map_iframe')
		map_iframe_field.send_keys(map_iframe)

	def add_images(self, source_company: str, images: Union[dict[str, dict[str, str]], list[str]]):
		if source_company == 'inghams':
			self.__add_inghams_images(images)
		else:
			self.__add_tui_images(images)
		self._web_image_handler.check_images_present_in_final_listing()

	def __add_inghams_images(self, images: dict[str, dict[str]]):
		"""Add images from Inghams listings, including titles and alt text"""
		for image, attributes in images.items():
			self._local_image_handler.save_image(image_name=image + '.jpg', image_url=attributes['src'])
		image_paths = self._local_image_handler.get_all_images_in_directory()
		image_order = self._web_image_handler.upload_and_select_images(image_paths)
		# Add image title and alt text
		self._web_image_handler.add_title_and_alt_text(image_order, images)
		self._local_image_handler.delete_images()

	def __add_tui_images(self, images: list[str]):
		for image_url in images:
			image_name = str(image_url).split('/')[-1]
			self._local_image_handler.save_image(image_name, image_url)
		pathlist = self._local_image_handler.get_all_images_in_directory()
		self._web_image_handler.upload_and_select_images(pathlist)
		self._local_image_handler.delete_images()

	def __click_correct_facility_option_obj(self, option_num: int):
		"""Click the correct DOM object corresponding to a given facility value"""
		try:
			action = ActionChains(self.driver)
			selector = self.driver.find_element(
				By.XPATH,
				f'//*[@id="id_features_from"]/option[{option_num}]'
			)
			action.double_click(selector).perform()
		except NoSuchElementException as e:
			logging.exception(f'Cannot find facility in available input options.\n{e}')
