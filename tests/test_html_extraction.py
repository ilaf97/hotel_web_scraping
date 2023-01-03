import unittest
from src.html_extraction import ExtractHtml


class TestHtmlExtraction(unittest.TestCase):

	# TODO: Remove or refactor these tests

	test_url = 'https://www.inghams.co.uk/destinations/italy/neapolitan-riviera/amalfi-coast/hotel-aurora-amalfi#0'
	ex_html = ExtractHtml(test_url)

	def test_get_html_text(self):
		with open('test_html/test_html_text', 'r') as f:
			test_html_text = f.read()
		live_html_text = self.ex_html.get_html_text()
		self.assertEqual(test_html_text, live_html_text, "Page content different")

	def test_html_parsing(self):
		with open('test_html/test_parsed_html', 'r') as f:
			test_html_parsed = f.read()
		live_parsed_html = self.ex_html.parse_html()
		self.assertIn(test_html_parsed, live_parsed_html, 'Page content different')


if __name__ == '__main__':
	unittest.main()
