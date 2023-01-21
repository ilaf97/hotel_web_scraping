import unittest
from src.html_extraction import ExtractHtml
from src.inghams.data_fields import InghamsDataFields


class TestInghamsDataFields(unittest.TestCase):

	@classmethod
	def setUpClass(cls) -> None:
		eh = ExtractHtml(
			'https://www.inghams.co.uk/destinations/italy/neapolitan-riviera/amalfi-coast/hotel-aurora-amalfi#0')
		html_obj = eh.parse_html_bs()
		cls.df = InghamsDataFields(html_obj)

	def test_get_name(self):
		name = self.df.get_name()
		self.assertEqual(name, 'Hotel Aurora, Amalfi', 'Hotel name incorrect')

	def test_get_description(self):
		desc = self.df.get_description()
		self.assertIn(
			'Hotel Aurora has a fantastic location in Amalfi.',
			desc,
			'Description intro differs from expected value'
		)
		self.assertIn(
			'A lovely buffet breakfast is served every morning on the terrace so you can enjoy a coffee and a fresh',
			desc,
			'Paragraph two of description differs from expected value '
		)

	def test_get_rooms(self):
		rooms = self.df.get_rooms()
		self.assertNotEqual('Rooms', rooms[:6], '"Rooms" header should not be at start of string')
		self.assertIn(
			'Standard Sea View Rooms are located on the second floor and have a balcony with sea views.',
			rooms,
			'First room type description omitted or incorrect'
		)
		self.assertIn(
			'Superior Rooms are located on the top floors of the hotel at the back of the property.',
			rooms,
			'Second room type description omitted or incorrect'
		)

	def test_get_location(self):
		location = self.df.get_location()
		self.assertEqual(
			[40.6320567, 14.5947055],
			location['lat_long'],
			'Latitude and longitude values omitted or incorrect'
		)
		self.assertIn(
			'900 metres to Valle delle Ferriere Nature Reserve',
			location['description'],
			'Distance to Valle delle Ferriere Nature Reserve omitted or incorrect'
		)

	def test_get_facilities(self):
		facilities = self.df.get_facilities()
		self.assertIn(
			'Private beach with sun loungers and parasols',
			facilities,
			'Private beach info omitted or incorrect'
		)
		self.assertIn(
			'Free Wi-Fi\nGarage (payable locally)',
			facilities,
			'Wi-fi and/or garage info omitted or incorrect'
		)

	def test_get_meals(self):
		meals = self.df.get_meals()
		self.assertIn(
			'Breakfast here is buffet style and includes delicious homemade cakes, pastries, fruit juices',
			meals,
			'Breakfast description omitted or incorrect'
		)
		self.assertIn(
			'The hotel has a nice lounge bar and the large terrace here is the best place for an aperitif',
			meals,
			'Lounge bar description omitted or incorrect'
		)
		self.assertIn(
			'Bed & Breakfast',
			meals,
			'Bed and breakfast option omitted or incorrect'
		)

	def test_get_excursions(self):
		excursions = self.df.get_excursions()
		self.assertIn(
			'Pre-book your excursions online or give us a call',
			excursions,
			'Intro omitted or incorrect'
		)
		self.assertIn(
			'Departs: Sundays from May to October\n'
			'Price departing from: Amalfi, Maiori or Minori from £57pp, Positano from £74pp or Ravello from £67pp',
			excursions,
			'Pompeii & Herculaneum trip info omitted or incorrect'
		)
		self.assertIn(
			'We act at all times as a selling agent for the suppliers.',
			excursions,
			'Disclaimer intro omitted or incorrect')

	def test_get_images(self):
		images_dict = self.df.get_images()
		self.assertEqual(
			images_dict['Superior Room'],
			'https://res.cloudinary.com/dqc68ksfw/image/upload/v1/Inghams/media/13072047/aurora03.jpg',
			'Image URL omitted or incorrect'
		)


if __name__ == '__main__':
	unittest.main()
