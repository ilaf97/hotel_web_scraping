import json
from typing import Union
import html
import re
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TuiDataFields:

	"""
	Class allowing data from required fields to be scraped from hotel page's JS driver object.

	Params:
	- driver (WebDriver): the hotel's web page JavaScript driver object as found by Selenium

	Attributes:
	- __driver (WebDriver) (Private)
	- __page_source (str) (Private)

	Methods:
	- get_name()
	- get_description()
	- get_rooms()
	- get_location()
	- get_facilities()
	- get_meals()
	- __dismiss_cookies_banner() (Private)
	"""

	def __init__(self, driver: WebDriver):
		self.__driver = driver
		self.__dismiss_cookies_banner()
		self.__page_source = driver.page_source

	def get_name(self) -> str:
		"""Returns hotel name"""
		hotel_name_html_obj = self.__driver.find_element(By.TAG_NAME, 'h1')
		return hotel_name_html_obj.text.strip().capitalize()

	def get_description(self) -> str:
		"""Returns description of hotel"""
		gallery_data = json.loads(self.__page_source.split('galleryData = ')[1].split('};')[0] + '}')
		description = html.unescape(gallery_data['featureCodesAndValues']['introduction'][0])
		description = re.sub(r'\([^<>]*\)', '', description)
		return description

	def get_best_for(self):

		def get_empty_rating_rectangles(div: WebElement):
			return div.find_elements(By.CLASS_NAME, 'SkiResortInfo__rectEmpty')

		best_for_dict = {}
		experience_levels = ['beginners', 'intermediates', 'advanced', 'boarders']
		for level in experience_levels:
			level_div = self.__driver.find_element(By.CLASS_NAME, f'SkiResortInfo__{level}')
			best_for_dict[level] = (5 - len(get_empty_rating_rectangles(level_div))) * '★'

		return best_for_dict

	def get_rooms(self) -> str:
		"""Returns rooms available at hotel"""
		self.__driver.find_element(By.XPATH, '//*[@id="rooms"]/a').click()
		rooms = html.unescape(self.__driver.find_element(By.CLASS_NAME, 'SkiRoomInfo__roomInfoBlock').text.strip())
		return rooms

	def get_location(self) -> dict[str: Union[str, list[int]]]:
		"""Returns hotel's location"""
		location_dict = {}
		self.__driver.find_element(By.XPATH, '//*[@id="location"]/a').click()
		WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.ID, 'sights__component')))
		location_dict['description'] = \
			html.unescape(self.__driver.find_element(
				By.XPATH,
				'//*[@id="locationEditorial__component"]/div/div'
			).text.strip())
		feature_codes_and_values = json.loads(
			self.__page_source.split('galleryData = ')[1].split('};')[0] + '}'
		)['featureCodesAndValues']
		latitude = float(feature_codes_and_values['latitude'][0])
		longitude = float(feature_codes_and_values['longitude'][0])
		location_dict['lat_long'] = [latitude, longitude]
		return location_dict

	def get_facilities(self) -> list[str]:
		"""Returns facilities available at hotel"""
		facilities_string = json.loads(
			self.__page_source.split('accommodationFacilities  = ')[1].split('};')[0] + '}'
		)['featureCodesAndValues']['AF0047'][0]
		facilities_string = facilities_string.replace('· ', '\n')
		return facilities_string

	def get_meals(self) -> str:
		"""Returns meal options"""
		board_type = self.__driver.find_element(By.TAG_NAME, 'h4').text.strip()
		board_description = self.__driver.find_element(
			By.XPATH,
			'//*[@id="browseBoardBasis__component"]/div/div/div/div[2]/div[2]/p[1]'
		).text.strip()
		return board_type + '\n' + board_description

	def get_images(self):
		"""Returns all images URLS for hotel"""
		hotel_images = []
		gallery_data = json.loads(self.__page_source.split('galleryData = ')[1].split('};')[0] + '}')
		gallery_images = gallery_data['galleryImages']
		for image in gallery_images:
			src = image['mainSrc'].split('?')[0]
			if src not in hotel_images:
				# Get image source, removing resize params whilst doing so
				hotel_images.append(src)
			else:
				break
		return hotel_images

	def __dismiss_cookies_banner(self):
		"""Close the cookies dialog that is present at the launch of new browser instance.
		Returns:
		- None

		Exceptions:
		- Exception (custom): thrown when no cookie dialog present or found
		"""
		try:
			self.__driver.find_element(By.ID, 'cmNotifyBanner')
		except NoSuchElementException:
			return
		try:
			self.__driver.find_element(By.ID, 'cmDecline').click()
			return
		except NoSuchElementException:
			try:
				self.__driver.find_element(By.ID, 'cmCloseBanner').click()
				return
			except NoSuchElementException as e:
				raise Exception(f'Cannot close the cookies dialog! {e}')
