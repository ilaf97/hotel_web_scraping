import logging
from typing import Union, Optional
import random
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from src.image_handler import ImageHandler


class CmsListingMapper():
	"""
	Class handling input into CMS data fields.

	Attributes:
	- __inghams_image_handler (ImageHandler) (Private)
	- __tui_image_handler (ImageHandler) (Private)

	Methods:
	- add_hotel_name()
	- set_category_to_hotel()
	- add_text_description_field()
	- select_facilities()
	- add_map_location()
	- add_images()
	- __add_inghams_images() (Private)
	- __add_tui_inmages() (Private)
	- __click_correct_option_obj() (Private)
	"""

	def __init__(self, cms_driver: WebDriver):
		self.driver = cms_driver
		self.__inghams_image_handler = \
			ImageHandler(driver=self.driver, source_company='inghams')
		self.__crystal_ski_image_handler = \
			ImageHandler(driver=self.driver, source_company='crystal_ski')
		self.__tui_image_handler = \
			ImageHandler(driver=self.driver, source_company='tui')

	def add_hotel_name(self, name: str):
		"""Add hotel name to accommodation title and slug fields"""
		try:
			self.driver.find_element(By.ID, 'id_title').send_keys(name)
			# self.driver.find_element(By.ID, 'id_slug').send_keys(
			# 	name.lower().replace(' ', '-').replace(',', '').replace("'", ''))
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot find/edit "Title" field\n{e}')
		self.set_category_to_hotel()

	def set_holiday_id(self):
		holiday_id = str(random.randint(1, 999999)).zfill(6)
		self.driver.find_element(By.ID, 'id_holiday_id').send_keys(holiday_id)

	def set_resort(self, resort_name: Optional[str]):
		if resort_name:
			"""Set resort name field"""
			try:
				self.driver.find_element(By.XPATH, f'//*[@id="id_resort"]/option[text()={resort_name}]').click()
			except NoSuchElementException as e:
				raise NoSuchElementException(f'Cannot find resort {resort_name}\n{e}')

	def set_category_to_hotel(self):
		"""Set accomodation category field to hotel"""
		try:
			self.driver.find_element(By.ID, 'id_category').click()
			self.driver.find_element(By.XPATH, '//*[@id="id_category"]/option[3]').click()
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot find category field/change category\n{e}')

	def add_text_description_field(self, text: str, description_type: str):
		"""Add description fields for general description, rooms and meals.
		Params:
		- text (str): string to input as description body
		- description_type (str): string selector to determine the content type"""
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
				text_area.send_keys(text)
			self.driver.switch_to.default_content()
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot find description field/add description\n{e}')

	def add_best_for(self, best_for_dict: dict[str]):
		best_for_str = ''

		if not best_for_dict:
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

	def select_facilities(self, facilities: str):
		"""Select facilities from options field and validate correct selection has been made"""
		facilities_list = facilities
		options_selected = []
		options_to_select = []
		available_facilities_to_select = {
			'bowling': '1',
			'spa': '2',
			'heated outdoor pool': '3',
			'skidoo': '4',
			'walking': '5',
			'gym': '6',
			'parapenting': '7',
			'snowshoeing': '8',
			'snow sure': '9',
			'high altitude skiing': '10',
			'high-altitude skiing': '10',
			'village resort': '11',
			'family friendly': '12',
			'tv': '13',
			'television': '13',
			'sauna': '14',
			'balcony': '15',
			'outdoor pool': '16',
			'outdoor pools': '16',
			'swimming pool': '17',
			'swimming pools': '17',
			'restaurant': '18',
			'bar': '19',
			'dishwasher': '20',
			'coffee': '21',
			'oven': '22',
			'fridge': '23',
			'refrigerator': '24',
			'microwave': '25'
		}
		for facility in facilities_list:
			for key in available_facilities_to_select.keys():
				#TODO: reverse order such that options chosen from bottom up
				if key in facility.lower():
					options_to_select.append(int(available_facilities_to_select[key]))
					options_selected.append(key)

		options_to_select.sort(reverse=True)
		for option in options_to_select:
			self.__click_correct_option_obj(option)
		# options_recorded = (self.driver.find_element(By.ID, 'id_features_to').text.lower() + '\n').strip().split('\n')
		# # Check options selected match with facilities input
		# if not len([record for record in options_recorded if any(item in record for item in options_selected)]):
		# 	raise AssertionError('Not all selected facilities have been successfully recorded!')

	def add_map_location(self, location: str):
		"""Add the location in the form of a iframe_map object"""
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
		"""Add iomages to the CMS image client and select them for use in the listing"""
		if source_company == 'inghams':
			self.__add_inghams_images(images)
		else:
			self.__add_tui_images(images)

	def __add_inghams_images(self, images: dict[str, dict[str]]):
		"""Add images from Inghams listings, including titles and alt text"""
		for image, attributes in images.items():
			self.__inghams_image_handler.save_image(image_name=image + '.jpg', image_url=attributes['src'])
		image_paths = self.__inghams_image_handler.get_all_images_in_directory()
		image_order = self.__inghams_image_handler.upload_and_select_images(image_paths)
		# Add image title and alt text
		self.__inghams_image_handler.add_title_and_alt_text(image_order, images)
		self.__inghams_image_handler.delete_images()

	def __add_tui_images(self, images: list[str]):
		"""Add images from TUI listings"""
		for image_url in images:
			image_name = str(image_url).split('/')[-1]
			self.__tui_image_handler.save_image(image_name, image_url)
		pathlist = self.__tui_image_handler.get_all_images_in_directory()
		self.__tui_image_handler.upload_and_select_images(pathlist)
		self.__tui_image_handler.delete_images()

	def __click_correct_option_obj(self, option_no: int):
		"""Click the correct DOM object corresponding to a given facility value"""
		try:
			action = ActionChains(self.driver)
			selector = self.driver.find_element(
					By.XPATH,
					f'//*[@id="id_features_from"]/option[{option_no}]'
				)
			action.double_click(selector).perform()
		except NoSuchElementException as e:
			logging.exception(f'Cannot find facility in available input options.\n{e}')
