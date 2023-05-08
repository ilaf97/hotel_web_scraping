import json
import re
import time
from typing import Union

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


class TuiSiteData:

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
	- get_food_and_drink()
	- __dismiss_cookies_banner() (Private)
	"""

	def __init__(self, driver: WebDriver):
		self.__driver = driver
		self.__dismiss_cookies_banner()
		self.__page_source = driver.page_source

	def get_name(self) -> str:
		"""Returns hotel name"""
		hotel_name_html_obj = self.__driver.find_element(By.TAG_NAME, 'h1')
		return hotel_name_html_obj.text.strip()

	def get_description(self) -> str:
		"""Returns description of hotel"""
		about_tab_objs = self.__driver.find_element(By.CLASS_NAME, 'About__content').text.strip()
		disclaimer = self.__driver.find_element(By.XPATH, '//*[@id="disclaimer__component"]/div').text.strip()
		description = about_tab_objs + '\n' + disclaimer
		description = re.sub(r'\([^<>]*\)', '', description)
		return description

	@staticmethod
	def get_best_for() -> dict[str]:
		return dict()

	def get_rooms(self) -> str:
		"""Returns rooms available at hotel"""
		room_str = ''
		self.__driver.find_element(By.ID, 'rooms').click()
		rooms = self.__driver.find_elements(By.CLASS_NAME, 'UI__roomListWrapper')
		for index, room in enumerate(rooms, start=1):
			room_str = room_str + room.find_element(
				By.XPATH,
				f'//*[@id="roomsList__component"]/div/div/div[2]/div[{index}]/div[2]/div[1]'
			).text.strip()
		return room_str

	def get_location(self) -> dict[str: Union[str, list[int]]]:
		"""Returns hotel's location"""
		location_dict = {}
		self.__driver.find_element(By.XPATH, '//*[@id="location"]/a').click()
		location_dict['description'] = \
			self.__driver.find_element(
				By.XPATH,
				'//*[@id="locationEditorial__component"]/div/div/div/aside'
			).text.strip()
		lat_long = json.loads(self.__page_source.split('"geo":')[1].split('}')[0] + '}')
		latitude = float(lat_long['latitude'])
		longitude = float(lat_long['longitude'])
		location_dict['lat_long'] = [latitude, longitude]
		return location_dict

	def get_facilities(self) -> list[str]:
		"""Returns facilities available at hotel"""
		facility_list = []
		try:
			facilities_data = json.loads(self.__page_source.split('accommFacilitiesJsonData = ')[1].split('};')[0] + '}')
			facilities = facilities_data['facilities']
			for facility in facilities:
				facility_list.append(facility['name'].lower())
			return facility_list
		except IndexError:
			return ['']

	def get_meals(self) -> str:
		"""Returns meal options"""
		board_type = self.__driver.find_element(By.TAG_NAME, 'h4').text.strip()
		self.__driver.find_element(By.XPATH, '//*[@id="facilities"]').click()
		try:
			self.__driver.find_element(By.LINK_TEXT, 'FOOD AND DRINK').click()
			board_description = self.__driver.find_element(
				By.CLASS_NAME,
				'Facilities__cardContet'
			).text.strip()
			board_description = re.sub(r'\([^<>]*\)', '', board_description)
			return board_type + '\n' + board_description
		except NoSuchElementException:
			return ' '

	def get_images(self) -> list[str]:
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