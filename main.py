import sys
import time

from src.cms.cms_instance import CmsInstance
from src.cms.cms_pipeline import CmsOperations
from src.cms.cms_pipeline import CmsPipeline
from src.util.config_helper import ConfigHelper
from src.util.user_input_helper import validate_user_input
from src.web_scraping.scraping_pipeline import ScrapingPipeline


def ask_user_if_continue_after_scraping() -> bool:
	user_prompt = "\n\n\nWeb scraping is complete!\n" \
				  "Populate the CMS with the data? (Y/N)\n"
	user_response = input(user_prompt)
	return validate_user_input(user_response)


def ask_user_to_define_process_start_point() -> bool:
	user_prompt = "This program can be started either from the very beginning, " \
				  "scraping the web page data then populating the CMS right away, " \
				  "or can be started mid-way at the CMS input stage.\n" \
				  "Start from the beginning of the process? (Y/N)\n"
	user_response = input(user_prompt)
	return validate_user_input(user_response)


if __name__ == '__main__':
	config_helper = ConfigHelper()
	company_name = config_helper.get_company_name()
	config_helper.check_company_name_valid(company_name)
	start_at_beginning = ask_user_to_define_process_start_point()
	if start_at_beginning:
		generate_filename = config_helper.user_prompt_about_generating_filename()
		if generate_filename:
			new_filename = config_helper.generate_filename(company_name)
			config_helper.set_new_filename_in_config(new_filename, company_name)

	filename = config_helper.read_filename(company_name)

	# Scrape data from web pages
	if start_at_beginning:
		scraping_pipeline = ScrapingPipeline(
			company_name=company_name,
			filename=filename
		)
		scraping_pipeline.scrape_and_save_data()
		if not ask_user_if_continue_after_scraping():
			sys.exit()

	cms_instance = CmsInstance()
	web_driver = cms_instance.driver
	cms_operations = CmsOperations(
		web_driver=web_driver
	)

	cms_pipeline = CmsPipeline(
		filename=filename,
		company_name=company_name,
		cms_operations=cms_operations,

	)

	time.sleep(2)
	# Add data to CMS
	cms_operations.instantiate_cms_add_page()
	controller = cms_pipeline.read_data_and_enter_into_cms()

	if cms_pipeline.check_for_failed_runs(controller):
		print(f'Some listings failed to be recorded in {company_name} data')

	print('Complete! Please check site listings to ensure data is correct')
