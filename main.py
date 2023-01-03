from bs4 import BeautifulSoup
import datetime
from tqdm import tqdm
from src.html_extraction import ExtractHtml
from src.data_fields import DataFields
from src.save_data import SaveData


def get_html_obj(url: str) -> BeautifulSoup:
	ex_html = ExtractHtml(url)
	return ex_html.parse_html()


def get_all_data_fields(html_obj: BeautifulSoup) -> list[str]:
	data_fields = DataFields(html_obj)
	data_fields_list = [
		data_fields.get_name(),
		data_fields.get_description(),
		data_fields.get_rooms(),
		data_fields.get_location(),
		data_fields.get_facilities(),
		data_fields.get_food_and_drink(),
		data_fields.get_excursions(),
		data_fields.get_images()
	]
	return data_fields_list


if __name__ == '__main__':
	url_list = ['https://www.inghams.co.uk/destinations/italy/neapolitan-riviera/amalfi-coast/hotel-aurora-amalfi#0',
				'https://www.inghams.co.uk/destinations/france/chamonix/hotel-la-folie-douce?accommodationNode=32317&programCode=GBINB&tourOpCode=ING&catalogue=010&obArrGateway=FRCH&departurePoint=AIRPORT-LGW&propertyCode=FRCH0126&boardBasis=BB&unitCode=A2&transportType=FLT&departureDate=13/05/2023&duration=7&adults=2&children=0&childages=#0']
	save_data = SaveData(f'iSki–{datetime.datetime.today().strftime("%Y-%m-%d")}')
	save_data.create_file()
	for url in tqdm(url_list):
		url_html_obj = get_html_obj(url)
		hotel_data = get_all_data_fields(url_html_obj)
		save_data.add_data(hotel_data)



