from bs4 import BeautifulSoup
import datetime
import os
from selenium.webdriver.chrome.webdriver import WebDriver
from tqdm import tqdm

from src.html_extraction import ExtractHtml
from src.inghams.data_fields import InghamsDataFields
from src.tui.data_fields import TuiDataFields
from src.save_data import SaveData
from src.tui.data_fields import TuiDataFields


def get_html_obj(url: str) -> BeautifulSoup:
	ex_html = ExtractHtml(url)
	return ex_html.parse_html_bs()


def get_driver_obj(url: str) -> WebDriver:
	ex_html = ExtractHtml(url)
	return ex_html.parse_html_selenium()


def get_inghams_data_fields(html_obj: BeautifulSoup) -> list[str]:
	data_fields = InghamsDataFields(html_obj)
	data_fields_list = [
		data_fields.get_name(),
		data_fields.get_description(),
		data_fields.get_rooms(),
		data_fields.get_location(),
		data_fields.get_facilities(),
		data_fields.get_food_and_drink(),
		data_fields.get_images(),
		data_fields.get_excursions()
	]
	return data_fields_list


def get_tui_data_fields(driver: WebDriver) -> list[str]:
	data_fields = TuiDataFields(driver)
	data_fields_list = [
		data_fields.get_name(),
		data_fields.get_description(),
		data_fields.get_rooms(),
		data_fields.get_location(),
		data_fields.get_facilities(),
		data_fields.get_food_and_drink(),
		data_fields.get_images()
	]
	return data_fields_list


if __name__ == '__main__':
	ingham_url_list = ['https://www.inghams.co.uk/destinations/italy/neapolitan-riviera/amalfi-coast/hotel-aurora-amalfi#0',
				'https://www.inghams.co.uk/destinations/france/chamonix/hotel-la-folie-douce?accommodationNode=32317&programCode=GBINB&tourOpCode=ING&catalogue=010&obArrGateway=FRCH&departurePoint=AIRPORT-LGW&propertyCode=FRCH0126&boardBasis=BB&unitCode=A2&transportType=FLT&departureDate=13/05/2023&duration=7&adults=2&children=0&childages=#0']
	tui_url_list = ['https://www.tui.co.uk/destinations/italy/lake-garda/garda/hotels/hotel-la-perla.html',
					]
	inghams_save_data = SaveData(
		filename=f'inghams–{datetime.datetime.today().strftime("%Y-%m-%d")}',
		company='inghams'
	)
	inghams_save_data.create_file()
	for url in tqdm(ingham_url_list):
		url_html_obj = get_html_obj(url)
		hotel_data = get_inghams_data_fields(url_html_obj)
		inghams_save_data.add_data(hotel_data)

	tui_save_data = SaveData(
		filename=f'tui–{datetime.datetime.today().strftime("%Y-%m-%d")}',
		company='tui'
	)
	tui_save_data.create_file()
	for url in tqdm(tui_url_list):
		driver_obj = get_driver_obj(url)
		hotel_data = get_tui_data_fields(driver_obj)
		tui_save_data.add_data(hotel_data)
	driver_obj.close()


