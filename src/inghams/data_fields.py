from bs4 import BeautifulSoup, ResultSet


class InghamsDataFields:

	"""
	Class allowing data from required fields to be scraped from hotel page's HTML object.

	Params:
	- html_object (BeautifulSoup): the hotel's HTML page object as parsed by BeautifulSoup

	Attributes:
	- html_object (BeautifulSoup)

	Methods:
	- get_name()
	- get_description()
	- get_rooms()
	- get_location()
	- get_facilities()
	- get_food_and_drink()
	- get_excursions()
	- __get_all_tab_div_content() (Private)
	- __format_text() (Private)
	"""

	def __init__(self, html_object: BeautifulSoup):
		self.html_object = html_object

	def get_name(self) -> str:
		"""Returns hotel name"""
		hotel_name_html_obj = self.html_object.find_all('h1', class_='c-heading-h1')[0]
		return hotel_name_html_obj.text.strip()

	def get_description(self) -> str:
		"""Returns description of hotel"""
		description_html_objs = self.html_object.find(id='descriptionAccTop')
		p_tags = description_html_objs.find_all('p')
		return self.__format_text(p_tags)

	def get_rooms(self) -> str:
		"""Returns rooms available at hotel"""
		accommodation_tab_objs = self.html_object.find(id='tabpanel0')
		p_tags = accommodation_tab_objs.find_all('p')
		for index, p in enumerate(p_tags):
			if p.text.strip() == 'Rooms':
				room_description = p_tags[index+1:]
				break
		return self.__format_text(room_description)

	def get_location(self) -> str:
		"""Returns hotel's location"""
		location_tab_objs = self.html_object.find(id='tabpanel5')
		header = location_tab_objs.find_all('div', class_='panel-ski-title')[0].text.strip()
		ul_tags = location_tab_objs.find_all('ul')[0]
		return header + '\n' + self.__format_text(ul_tags)

	def get_facilities(self) -> str:
		"""Returns facilities available at hotel"""
		facilities_tab_objs = self.html_object.find(id='tabpanel3')
		ul_tags = facilities_tab_objs.find_all('ul')
		return self.__format_text(ul_tags)

	def get_food_and_drink(self) -> str:
		"""Returns meal options"""
		return self.__get_all_tab_div_content('6')

	def get_excursions(self) -> str:
		"""Returns available excursions from the hotel"""
		return self.__get_all_tab_div_content('2')

	def get_images(self):
		"""Returns all images URLS for hotel"""
		image_objs = self.html_object.find_all('div', class_='c-slider__list')[0]
		img_tags = image_objs.find_all('img')
		img_name = image_objs.find_all('div', class_='c-slider__caption')
		image_data = {}
		for index, image in enumerate(img_tags):
			image_data[img_name[index].text] = image['data-cloudinarymainslider']
		return image_data

	def __get_all_tab_div_content(self, panel_no: str) -> str:
		"""Retrieve all div content from given tab.
		Params:
		- panel_no (str): HTML panel no. for desired tab

		Returns:
		Formatted string of div element's text representation"""
		tab_objs = self.html_object.find(id='tabpanel' + panel_no)
		div = tab_objs.find_all('div', class_='c-accordion__content')
		return self.__format_text(div)

	@staticmethod
	def __format_text(html_objs: ResultSet) -> str:
		"""Format text for object in ResultSet of HTML objects,
		Params:
		- html_objs (ResultSet): results from searching HTML container using BeautifulSoup find_all()

		Returns:"
		Formatted string containing all text from parsed HTML objects"""
		output_str = ''
		for obj in html_objs:
			output_str = output_str + obj.text.strip() + '\n'
		return output_str

