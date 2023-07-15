from typing import Union

from bs4 import BeautifulSoup, ResultSet


class InghamsSiteData:

	def __str__(self):
		return "inghams"

	def __init__(self, html_object: BeautifulSoup):
		self.html_object = html_object

	def get_name(self) -> str:
		hotel_name_html_obj = self.html_object.find_all('h1', class_='c-heading-h1')[0]
		return hotel_name_html_obj.text.strip()

	def get_description(self) -> str:
		description_html_objs = self.html_object.find(id='descriptionAccTop')
		p_tags = description_html_objs.find_all('p')
		return self.__format_text(p_tags)

	@staticmethod
	def get_best_for() -> dict[str]:
		return dict()

	def get_rooms(self) -> str:
		accommodation_tab_objs = self.html_object.find(id='tabpanel0')
		p_tags = accommodation_tab_objs.find_all('p')
		for index, p in enumerate(p_tags):
			if p.text.strip() == 'Rooms':
				room_description = p_tags[index + 1:]
				break
		return self.__format_text(room_description)

	def get_location(self) -> dict[str: Union[str, list[int]]]:
		location_dict = {}
		location_tab_objs = self.html_object.find(id='tabpanel5')
		li_tags = location_tab_objs.find_all('li')
		latitude = float(li_tags[1].text.split(': ')[1])
		longitude = float(li_tags[0].text.split(': ')[1])
		try:
			location_dict['description'] = li_tags[2].text.strip()
		except IndexError:
			location_dict['description'] = ''
		location_dict['lat_long'] = [latitude, longitude]
		return location_dict

	def get_facilities(self) -> list[str]:
		facilities_list = []
		facilities_tab_objs = self.html_object.find(id='tabpanel3')
		ul_tags = facilities_tab_objs.find_all('ul')
		for item in ul_tags:
			facilities_list = facilities_list + (item.text.strip().split('\n'))
		return facilities_list

	def get_meals(self) -> str:
		return self.__get_all_tab_div_content('6')

	def get_excursions(self) -> str:
		return self.__get_all_tab_div_content('2')

	def get_images(self):
		image_objs = self.html_object.find_all('div', class_='c-slider__list')[0]
		img_tags = image_objs.find_all('img')
		img_name = image_objs.find_all('div', class_='c-slider__item')
		image_data = {}
		for index, image in enumerate(img_tags):
			if index > 15:
				break
			else:
				if img_name[index].text is None:
					continue
				image_data[img_name[index].text.replace('\n', '').strip().lstrip()] = {
				'src': image['data-cloudinarymainslider'],
				'alt': image['alt'].capitalize()
			}
		return image_data

	def __get_all_tab_div_content(self, panel_no: str) -> str:
		"""Retrieve all div content from given tab.
		Params:
		- panel_no (str): HTML panel no. for desired tab
		"""

		try:
			tab_objs = self.html_object.find(id='tabpanel' + panel_no)
			div = tab_objs.find_all('div', class_='c-accordion__content')
			return self.__format_text(div)
		except AttributeError:
			return ''

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

