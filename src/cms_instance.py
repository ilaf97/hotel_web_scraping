import os
from typing import Union, Generator
import requests
from pathlib import Path
from selenium.webdriver.support.wait import WebDriverWait
from src.html_extraction import ExtractHtml
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC



class CmsInstance:

	def __init__(self):
		self.__admin_url = 'http://35.178.65.128:8001/admin/'
		self.__username = os.getenv('username')
		self.__password = os.getenv('password')
		self.__driver = self.__instantiate_site_driver()
		self.__log_in()
		self.__navigate_to_add_page()

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
			if description_type in ['rooms', 'meals']:
				description_field.send_keys(description_type.capitalize() + '\n\n' + text)
			else:
				description_field.send_keys(text)
		except NoSuchElementException as e:
			raise NoSuchElementException(f'Cannot find description field/add description\n{e}')

	def select_facilities(self, facilities: list[str]):

		def add_option_obj(option_no: str):
			options_to_select.append(
				self.__driver.find_element(By.XPATH, f'//*[@id="id_features_from"]/option[{option_no}]'))

		action = ActionChains(self.__driver)
		options_selected = ''
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
			# 'outdoor pool': '16', -> omitted to prevent duplication with 3rd dict entry
			'swimming pool': '17',
			'restaurant': '18',
			'bar': '19',
			'dishwasher': '20',
			'coffee': '21',
			'oven': '22',
			'fridge': '23',
			'refrigerator': '24',
			'microwave': '25'
		}
		for facility in facilities:
			for key in available_facilities_to_select.keys():
				if key in facility:
					add_option_obj(available_facilities_to_select[key])
					options_selected = options_selected + key + '\n'

		for option in options_to_select:
			action.double_click(option).perform()

		options_chosen = self.__driver.find_element(By.ID, 'id_features_to').text.lower()
		if options_chosen != options_selected:
			raise AssertionError('Not all selected facilities have been successfully recorded!')

	def add_map_iframe(self, location: dict[str: Union[str, list[int]]]):
		lat = location['long_lat'][0]
		lon = location['long_lat'][1]
		map_iframe = f'<iframe ' \
					 	f'src="https://www.google.com/maps?q={lat},{lon}&hl=es&z=14&amp;output=embed' \
					 	f'width="600" ' \
					 	f'height="450" ' \
					 	f'style="border:0;" ' \
					 	f'allowfullscreen="" ' \
					 	f'loading="lazy" ' \
					 	f'referrerpolicy="no-referrer-when-downgrade">' \
					 f'</iframe>'
		map_iframe_field = self.__driver.find_element(By.ID, 'id_map_iframe')
		map_iframe_field.send_keys(map_iframe)

	def add_images(self, source: str):#, images: Union[dict[str: str], list[str]], ):
		if source == 'inghams':
			self.__add_inghams_images()#images)

	def instantiate_cms_add_page(self):
		self.__log_in()
		self.__navigate_to_add_page()

	def __add_inghams_images(self): #, image_dict: dict[str: str]):
		# for image, attributes in image_dict:
		# 	self.__save_image(
		# 		image_name=image,
		# 		image_url=attributes['src'],
		# 		source_site='inghams'
		# 	)
		# add_another_image_slider_button = self.__driver.find_element(
		# 	By.XPATH,
		# 	'//*[@id="gallery_set-group"]/div/fieldset/table/tbody/tr[5]/td/a'
		# )
		main_window = self.__driver.current_window_handle
		image_paths = self.__get_all_images_in_directory('inghams')
		self.__upload_and_select_images(image_paths)

	def __upload_and_select_images(self, image_paths: Generator[Path, None, None]):

		def locate_upload_pop_up(timeout: int):
			WebDriverWait(self.__driver, timeout).until_not(
				EC.visibility_of_element_located(
					(By.XPATH, '//*[@id="content-main"]/div/form/section/div[1]')
				))

		timeouts = [1, 2, 3, 5, 10]  # total timeout of 20s
		for counter, image in enumerate(image_paths):
			# Open image selector in new tab
			self.__driver.find_element(
				By.ID,
				f'id_gallery_set-{counter}-gallery_image_video_lookup'
			).click()
			# Switch to open window
			self.__driver.switch_to.window(self.__driver.window_handles[1])
			# Now will be in new image selector tab
			self.__driver.find_element(By.XPATH, '//*[@id="result_list"]/tbody/tr[1]/td[3]/div/a').click()
			# Upload image with increasing timeout wait times
			self.__driver.find_element(By.CSS_SELECTOR, 'input[type=file]').send_keys(str(image))
			for index, time in enumerate(timeouts):
				try:
					locate_upload_pop_up(time)
					break
				except TimeoutException:
					if index != len(timeouts) - 1:
						continue
					else:
						raise TimeoutException(f'Image could not be uploaded within 20 seconds.')

			# Click on required uploaded image
			self.__driver.find_element(By.LINK_TEXT, str(image).split('/')[-1]).click()
			# Switch back to original window
			self.__driver.switch_to.window(self.__driver.window_handles[0])

	def __get_all_images_in_directory(self, source_site: str) -> Generator[Path, None, None]:
		abspath = os.path.abspath(f'../data/inghams/images')
		pathlist = Path(abspath).rglob('*.jpg')
		return pathlist

	def __save_image(
			self,
			image_name: str,
			image_url: str,
			source_site: str
	):
		image_data = requests.get(image_url).content
		with open(f'../data/{source_site}/images/{image_name}.jpg', 'wb') as img:
			img.write(image_data)

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


cms = CmsInstance()
cms.add_images('inghams')