import html
import json
import re
from typing import Union

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.models.data_fields_base_class import DataFieldsBaseClass


class CrystalSiteData(DataFieldsBaseClass):

	def __init__(self, driver: WebDriver):
		self.__driver = driver
		self.__dismiss_cookies_banner()
		self.__page_source = driver.page_source

	def get_name(self) -> str:
		hotel_name_html_obj = self.__driver.find_element(By.TAG_NAME, 'h1')
		return hotel_name_html_obj.text.strip().capitalize()

	@staticmethod
	def generate_slug(hotel_name: str) -> str:
		formatted_hotel_name = hotel_name.lower().replace(" ", "-")
		new_slug = formatted_hotel_name + "-crystal"
		return new_slug

	def get_resort(self) -> str:
		location_description_obj = self.__driver.find_element(
			By.XPATH,
			'//*[@id="headerContainer__component"]/div/div/div/div[1]/div[2]/span[1]/p'
		)
		resort = self.__extract_resort_from_location_description(location_description_obj.text)
		return resort

	def get_description(self) -> str:
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
			try:
				level_div = self.__driver.find_element(By.CLASS_NAME, f'SkiResortInfo__{level}')
			except NoSuchElementException:
				break
			best_for_dict[level] = (5 - len(get_empty_rating_rectangles(level_div))) * '★'

		return best_for_dict

	def get_rooms(self) -> str:
		self.__driver.find_element(By.XPATH, '//*[@id="rooms"]/a').click()
		rooms = html.unescape(self.__driver.find_element(By.CLASS_NAME, 'SkiRoomInfo__roomInfoBlock').text.strip())
		return rooms

	def get_location(self) -> dict[str: Union[str, list[int]]]:
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
		facilities_string = json.loads(
			self.__page_source.split('accommodationFacilities  = ')[1].split('};')[0] + '}'
		)['featureCodesAndValues']['AF0047'][0]
		facilities_string = facilities_string.replace('· ', '\n')
		return facilities_string

	def get_meals(self) -> str:
		board_type = self.__driver.find_element(By.TAG_NAME, 'h4').text.strip()
		board_description = self.__driver.find_element(
			By.XPATH,
			'//*[@id="browseBoardBasis__component"]/div/div/div/div[2]/div[2]/p[1]'
		).text.strip()
		return board_type + '\n' + board_description

	def get_images(self):
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

	@staticmethod
	def __extract_resort_from_location_description(resort: str) -> str:
		resort_and_country = resort.split(",")
		if len(resort_and_country) == 3:
			resort = resort_and_country[1]
		else:
			resort = resort_and_country[0].split(" ")[1]
		return resort.strip().capitalize()

	def __dismiss_cookies_banner(self):
		"""Close the cookies dialog that is present at the launch of new browser instance"""

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
