import json
from typing import Union
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time

from src.html_extraction import ExtractHtml


class TuiDataFields:

	"""
	Class allowing data from required fields to be scraped from hotel page's JS driver object.

	Params:
	- driver (WebDriver): the hotel's web page JavaScript driver object as found by Selenium

	Attributes:
	- driver (WebDriver)

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

	def get_name(self) -> str:
		"""Returns hotel name"""
		hotel_name_html_obj = self.__driver.find_element(By.TAG_NAME, 'h1')
		return hotel_name_html_obj.text.strip()

	def get_description(self) -> str:
		"""Returns description of hotel"""
		about_tab_objs = self.__driver.find_element(By.CLASS_NAME, 'About__content').text.strip()
		disclaimer = self.__driver.find_element(By.XPATH, '//*[@id="disclaimer__component"]/div').text.strip()
		return about_tab_objs + '\n' + disclaimer

	def get_rooms(self) -> str:
		"""Returns rooms available at hotel"""
		room_str = ''
		self.__driver.find_element(By.XPATH, '//*[@id="rooms"]/a').click()
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
		page_source = self.__driver.page_source
		self.__driver.find_element(By.XPATH, '//*[@id="location"]/a').click()
		location_dict['description'] = \
			self.__driver.find_element(
				By.XPATH,
				'//*[@id="locationEditorial__component"]/div/div/div/aside'
			).text.strip()
		lat_long = json.loads(page_source.split('"geo":')[1].split('}')[0] + '}')
		latitude = float(lat_long['latitude'])
		longitude = float(lat_long['longitude'])
		location_dict['lat_long'] = [latitude, longitude]
		return location_dict

	def get_facilities(self) -> str:
		"""Returns facilities available at hotel"""
		facilities = self.__driver.find_element(
			By.XPATH,
			'//*[@id="accomEditorial__component"]/div/div/div/aside/div[1]/div[2]'
		).text.strip()
		return facilities

	def get_food_and_drink(self) -> str:
		"""Returns meal options"""
		board_type = self.__driver.find_element(By.TAG_NAME, 'h4').text.strip()
		board_description = self.__driver.find_element(
			By.XPATH,
			'//*[@id="browseBoardBasis__component"]/div/div/div/div[2]/div/div/p'
		).text.strip()
		return board_type + '\n' + board_description

	def get_images(self):
		"""Returns all images URLS for hotel"""
		hotel_images = []
		self.__driver.find_element(
			By.XPATH,
			'//*[@id="heroBannerV2__component"]/div/div/div[1]/div[2]/ul/li/section/span/a'
		).click()
		time.sleep(1)
		banner_images_container = self.__driver.find_element(By.CLASS_NAME, 'Galleries__thumbNailView')
		banner_images = banner_images_container.find_elements(By.TAG_NAME, 'img')
		for image in banner_images:
			# Get image source, removing resize params whilst doing so
			hotel_images.append(image.get_attribute('src').split('?')[0])
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

eh = ExtractHtml(
			'https://www.tui.co.uk/destinations/italy/lake-garda/garda/hotels/hotel-la-perla.html')
driver = eh.parse_html_selenium()
df = TuiDataFields(driver)
print(df.get_location())