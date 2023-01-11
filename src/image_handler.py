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

	def __init__(self, driver: WebDriver, source_site: str):
		self.__driver = driver
		self.source_site = source_site

	def upload_and_select_images(self, image_paths: Generator[Path, None, None]):

		def locate_upload_pop_up(timeout: int):
			WebDriverWait(self.__driver, timeout).until_not(
				EC.visibility_of_element_located(
					(By.XPATH, '//*[@id="content-main"]/div/form/section/div[1]')
				))

		timeouts = [1, 2, 3, 5, 10]  # total timeout of 20s
		for counter, image in enumerate(image_paths):
			if counter > 2:
				# Add another image slider
				self.__driver.find_element(
						By.XPATH,
						'//*[@id="gallery_set-group"]/div/fieldset/table/tbody/tr[5]/td/a'
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
			self.__driver.find_element(By.LINK_TEXT, str(image).split('/')[-1]).click()
			# Switch back to original window
			self.__driver.switch_to.window(self.__driver.window_handles[0])

	def get_all_images_in_directory(self) -> Generator[Path, None, None]:
		abspath = os.path.abspath(f'../data/{self.source_site}/images')
		pathlist = Path(abspath).rglob('*.jpg')
		return pathlist

	def save_image(self, image_name: str, image_url: str):
		image_data = requests.get(image_url).content
		with open(f'../data/{self.source_site}/images/{image_name}.jpg', 'wb') as img:
			img.write(image_data)

	def delete_images(self):
		abspath = os.path.abspath(f'../data/{self.source_site}/images')
		for file in os.listdir(abspath):
			file_path = os.path.join(abspath, file)
			try:
				if os.path.isfile(file_path) or os.path.islink(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception as e:
				raise OSError(f'Failed to delete {file_path}. Reason: {e}')

	def add_title_and_alt_text(self, image_dict: dict[str: dict[str: str]]):
		for counter, image_name in enumerate(image_dict.keys()):
			self.__driver.find_element(
				By.ID,
				f'id_gallery_set-{counter}-title'
			).send_keys(image_name)
			self.__driver.find_element(
				By.ID,
				f'id_gallery_set-{counter}-alt'
			).send_keys(image_dict[image_name]['alt'])


