from src.util.config_helper import ConfigHelper
from src.web_scraping.read_data import ReadWebScrapingData
from src.web_scraping.save_data import SaveWebScrapingData


def exception_handler(company_name: str) -> None:
	save_filename = ConfigHelper().read_filename(company_name)
	save_data = SaveWebScrapingData(
		filename=save_filename,
		source_company=company_name
	)
	read_data = ReadWebScrapingData(
		filename=save_filename,
		source_company=company_name
	)
	try:
		read_data.read_data(failed_scrape_runs=True)
	except FileNotFoundError:
		save_data.create_json_file(failed_scrape_runs=True)
