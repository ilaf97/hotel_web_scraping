import json
import re
from typing import Union

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from src.tui.facilities import FacilitiesCategories


class TuiSiteData:

	def __str__(self):
		return "tui"

	def __init__(self, driver: WebDriver):
		self.driver = driver
		self.__dismiss_cookies_banner()
		self.__page_source = driver.page_source

	def get_name(self) -> str:
		hotel_name_html_obj = self.driver.find_element(By.TAG_NAME, 'h1')
		return hotel_name_html_obj.text.strip()

	@staticmethod
	def generate_slug(hotel_name: str) -> None:
		return None

	def get_resort(self) -> str:
		try:
			location_description_obj = self.driver.find_element(
				By.XPATH,
				'//*[@id="headerContainer__component"]/div/div/div/div[1]/div[2]/span[1]/p'
			)
		except NoSuchElementException:
			location_description_obj = self.driver.find_element(
				By.XPATH,
				'//*[@id="headerContainer__component"]/div/div[1]/div/div[2]/div[2]/span[1]/p'
			)

		resort = self.__extract_resort_from_location_description(location_description_obj.text)
		return resort

	def get_description(self) -> str:
		about_tab_objs = self.driver.find_element(By.CLASS_NAME, 'About__content').text.strip()
		disclaimer = self.driver.find_element(By.XPATH, '//*[@id="disclaimer__component"]/div').text.strip()
		description = about_tab_objs + '\n' + disclaimer
		description = re.sub(r'\([^<>]*\)', '', description)
		return description

	@staticmethod
	def get_best_for() -> dict[str]:
		return dict()

	def get_individual_facilities(self) -> list[str]:
		facility_list = []
		try:
			facilities_data = json.loads(
				self.__page_source.split('accommFacilitiesJsonData = ')[1].split('};')[0] + '}')
			facilities = facilities_data['facilities']
			for facility in facilities:
				facility_list.append(facility['name'].lower())
			return facility_list
		except IndexError:
			return ['']

	def get_facilities_descriptions(self) -> dict[str, str]:
		facilities_descriptions = {}
		self.driver.find_element(By.XPATH, '//*[@id="facilities"]').click()
		for category in FacilitiesCategories:
			try:
				facilities_descriptions[category.name] = self._get_facility_category(category.value)
			except NoSuchElementException:
				facilities_descriptions[category.name] = ''

		return facilities_descriptions

	def get_rooms(self) -> str:
		room_str = ''
		self.driver.find_element(By.ID, 'rooms').click()
		rooms = self.driver.find_elements(By.CLASS_NAME, 'UI__roomListWrapper')
		for index, room in enumerate(rooms, start=1):
			room_str = room_str + room.find_element(
				By.XPATH,
				f'//*[@id="roomsList__component"]/div/div/div[2]/div[{index}]/div[2]/div[1]'
			).text.strip()
		return room_str

	def get_location(self) -> dict[str: Union[str, list[int]]]:
		location_dict = {}
		self.driver.find_element(By.XPATH, '//*[@id="location"]/a').click()
		location_dict['description'] = \
			self.driver.find_element(
				By.XPATH,
				'//*[@id="locationEditorial__component"]/div/div/div/aside'
			).text.strip()
		lat_long = json.loads(self.__page_source.split('"geo":')[1].split('}')[0] + '}')
		latitude = float(lat_long['latitude'])
		longitude = float(lat_long['longitude'])
		location_dict['lat_long'] = [latitude, longitude]
		return location_dict

	def get_images(self) -> list[str]:
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
		resort = resort_and_country[0].split(" ")[1]
		return resort.strip().upper()

	def _get_facility_category(self, div_num: int) -> str:
		self.driver.find_element(By.XPATH,
								 f'//*[@id="facilitiesV3__component"]/div/div/div[1]/ul/li[{div_num}]/a').click()
		description = self.driver.find_element(
			By.XPATH,
			f'//*[@id="facilitiesV3__component"]/div/div/div[2]/div'
		).text.strip()
		if div_num == FacilitiesCategories.MEALS:
			board_type = self.driver.find_element(By.TAG_NAME, 'h4').text.strip()
			description = board_type + '\n' + description
		# Replace brakets
		description = re.sub(r'\([^<>]*\)', '', description)
		# Add extra newline for formatting
		description = re.sub(r"\n", r"\n\n", description)
		return description

	def __dismiss_cookies_banner(self):
		"""Close the cookies dialog that is present at the launch of new browser instance"""
		try:
			self.driver.find_element(By.ID, 'cmNotifyBanner')
		except NoSuchElementException:
			return
		try:
			self.driver.find_element(By.ID, 'cmDecline').click()
			return
		except NoSuchElementException:
			try:
				self.driver.find_element(By.ID, 'cmCloseBanner').click()
				return
			except NoSuchElementException as e:
				raise Exception(f'Cannot close the cookies dialog! {e}')