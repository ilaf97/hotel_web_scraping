import os
from selenium.webdriver.chrome.webdriver import WebDriver


class InghamsCmsImput:

	def input_name(self, driver: WebDriver):
		self.__driver = driver




icmsin = InghamsCmsImput()
icmsin.input_name(name)