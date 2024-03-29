import unittest

from src.cms.html_extraction import WebDriverFactory
from src.tui.data_fields import TuiSiteData


class TestTuiDataFields(unittest.TestCase):

	@classmethod
	def setUpClass(cls) -> None:
		eh = WebDriverFactory(
			'https://www.tui.co.uk/destinations/italy/lake-garda/garda/hotels/hotel-la-perla.html')
		driver = eh.parse_html_selenium()
		cls.df = TuiSiteData(driver)

	def test_get_name(self):
		name = self.df.get_name()
		self.assertEqual(name, 'Hotel La Perla', 'Hotel name incorrect')

	def test_get_description(self):
		desc = self.df.get_description()
		self.assertIn(
			'La Perla’s a family fave packed with perks to make your stay extra special.',
			desc,
			'Description intro differs from expected value'
		)
		self.assertIn(
			'Items marked with * incur extra charges which are payable locally',
			desc,
			'Disclaimer has not been appended to description'
		)

	def test_get_rooms(self):
		rooms = self.df.get_rooms()
		self.assertNotIn(
			'The rooms are decorated with contemporary colours and all come with a TV',
			rooms,
			'Intro should not be at start of string'
		)
		self.assertIn(
			'Twin Room with Pool View and Balcony',
			rooms,
			'First room type description omitted or incorrect'
		)
		self.assertIn(
			'Twin rooms come with either twin beds or a double bed, plus a balcony for soaking up the Italian sun.',
			rooms,
			'4th room type description omitted or incorrect'
		)

	def test_get_location(self):
		location = self.df.get_location()
		self.assertEqual(
			[45.574652559, 10.710902962],
			location['lat_long'],
			'latitude or longitude values omitted or incorrect'
		)
		self.assertIn(
			'GETTING TO HOTEL',
			location['description'],
			'Second subheading omitted or incorrect'
		)

	def test_get_facilities(self):
		facilities = self.df.get_individual_facilities()
		self.assertIn(
			'Two outdoor pools',
			facilities,
			'Two outdoor pools info omitted or incorrect'
		)
		self.assertIn(
			'E-bikes to hire*',
			facilities,
			'E-bike info omitted or incorrect'
		)

	def test_get_meals(self):
		meals = self.df.get_meals()
		self.assertIn(
			'Half Board',
			meals,
			'Header/title omitted or incorrect'
		)
		self.assertIn(
			'Hot and cold buffet breakfast. 4-course evening meal.',
			meals,
			'Board description omitted or incorrect'
		)
		self.assertNotIn(
			'BreakfastLunchEvening MealDrinksSnacks',
			meals,
			'Summary indicator text included when should have been omitted'
		)

	def test_get_z_images(self):
		images_list = self.df.get_images()
		self.assertEqual(
			images_list[4],
			'https://content.tui.co.uk/adamtui/2018_4/16_8/63863ba1-4d07-4ef5-b509-a8c4008c028a/ITA_GAR_018_45WebOriginalCompressed.jpg',
			'Image URL omitted or incorrect'
		)


if __name__ == '__main__':
	unittest.main()
