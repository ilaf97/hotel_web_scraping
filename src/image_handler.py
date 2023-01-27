import os
import shutil
from pathlib import Path
from typing import Generator

import requests
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


class ImageHandler:
	"""
	Class to handle the uploading of images into the CMS image client.
	First, images are saved locally, then they are uploaded, then deleted from local storage to conserve runtime memory.

	Params:
	- driver (WebDriver): the driver instance for the CMS site
	- source_company (str): the company from which the images are taken

	Attributes:
	- source_company (str)
	- __driver (WebDriver) (Private)

	Methods:
	- save_image()
	- get_all_images_in_directory()
	- upload_and_select_images()
	- delete_images()
	- add_title_and_alt_text()
	"""

	def __init__(self, driver: WebDriver, source_company: str):
		self.__driver = driver
		self.source_company = source_company
		self.__ROOT_DIR = Path(__file__).parent.parent

	def save_image(self, image_name: str, image_url: str):
		"""Save image from URL in directory"""
		headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
			'From': 'isaac.frewin@gmail.com'
		}
		image_data = requests.get(image_url, headers=headers).content
		image_name = image_name
		with open(f'{self.__ROOT_DIR}/data/{self.source_company}/images/{image_name}', 'wb') as img:
			img.write(image_data)

	def get_all_images_in_directory(self) -> Generator[Path, None, None]:
		"""Return iterator object of paths to all images in given directory"""
		abspath = os.path.abspath(f'{self.__ROOT_DIR}/data/{self.source_company}/images')
		pathlist = Path(abspath).rglob('*.jpg')
		return pathlist

	def upload_and_select_images(self, image_paths: Generator[Path, None, None]) -> list[str]:
		"""Upload images to CMS client and select them for use in the accommodation listing"""

		def locate_upload_pop_up(timeout: int):
			WebDriverWait(self.__driver, timeout).until_not(
				EC.visibility_of_element_located(
					(By.XPATH, '//*[@id="content-main"]/div/form/section/div[1]')
				))

		timeouts = [1, 2, 3, 5, 10]  # total timeout of 20s
		images_names_order = []
		for counter, image in enumerate(image_paths):
			if counter == 15:
				break
			if 2 < counter < 15:
				# Add another image slider
				self.__driver.find_element(
						By.LINK_TEXT,
						'Add another IMAGE SLIDER'
					).click()
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
			image_name = str(image).split('/')[-1]
			self.__driver.find_element(By.LINK_TEXT, image_name).click()
			images_names_order.append(image_name.replace('.jpg', ''))
			# Switch back to original window
			self.__driver.switch_to.window(self.__driver.window_handles[0])
		return images_names_order

	def delete_images(self):
		"""Delete all images in directory"""
		abspath = os.path.abspath(f'{self.__ROOT_DIR}/data/{self.source_company}/images')
		for file in os.listdir(abspath):
			file_path = os.path.join(abspath, file)
			try:
				if os.path.isfile(file_path) or os.path.islink(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception as e:
				raise OSError(f'Failed to delete {file_path}. Reason: {e}')

	def add_title_and_alt_text(self, image_order: list[str], image_dict: dict[str: dict[str: str]]):
		"""Add title and alt text for all images in accommodation listing"""
		for counter, image_name in enumerate(image_order):
			self.__driver.find_element(
				By.ID,
				f'id_gallery_set-{counter}-title'
			).send_keys(image_name)
			self.__driver.find_element(
				By.ID,
				f'id_gallery_set-{counter}-alt'
			).send_keys(image_dict[image_name]['alt'])


