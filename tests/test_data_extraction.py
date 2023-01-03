import unittest
from src.html_extraction import ExtractHtml
from src.data_fields import DataFields



class TestDataFields(unittest.TestCase):

	@classmethod
	def setUpClass(cls) -> None:
		eh = ExtractHtml(
			'https://www.inghams.co.uk/destinations/italy/neapolitan-riviera/amalfi-coast/hotel-aurora-amalfi#0')
		html_obj = eh.parse_html()
		cls.df = DataFields(html_obj)

	def test_get_name(self):
		name = self.df.get_name()
		self.assertEqual(name, 'Hotel Aurora, Amalfi', 'Hotel name incorrect')

	def test_get_description(self):
		desc = self.df.get_description()
		self.assertEqual(
			desc,
			'Hotel Aurora has a fantastic location in Amalfi. It’s just a few minutes’ walk from the centre and '
			'overlooks a gorgeous bay. We love relaxing on the terraces where you can lose yourself in the incredible '
			'sea views. There’s a beach just beneath the hotel that’s well equipped with sunbeds and umbrellas '
			'(payable locally).'
			'The hotel’s got a traditional style with charming and comfortable guest rooms finished with light blue '
			'vierti floor tiles that are typical of the area. A lovely buffet breakfast is served every morning on the '
			'terrace so you can enjoy a coffee and a fresh pastry with your sea views. With the centre of Amalfi close '
			'by you’ll be spoilt for choice with where to eat or what to see. Speak to the friendly staff before you'
			' head out. They\'re more than happy to share their advice.'
			'Transfer time: approx. 1 hour 30 mins by private car from Naples Airport.'
		)


if __name__ == '__main__':
	unittest.main()
