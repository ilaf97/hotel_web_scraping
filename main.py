import sys

from src.util.user_input_helper import validate_user_input
from src.cms.cms_instance import CmsInstance
from src.cms.cms_operations import CmsOperations
from datapipeline import DataPipeline
from src.util.config_helper import ConfigHelper


def ask_user_if_continue_after_scraping() -> bool:
	user_prompt = "Web scraping is complete!\n" \
				  "Populate the CMS with the data? (Y/N)"
	user_response = input(user_prompt)
	return validate_user_input(user_response)


def ask_user_to_define_process_start_point() -> bool:
	user_prompt = "This program can be started either from the very beginning," \
				  "scraping the web page data then populating the CMS right away, " \
				  "or can be started mid-way at the CMS input stage.\n" \
				  "Start from the beginning of the process? (Y/N)"
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
			config_helper.set_new_filename_in_config(new_filename)

	filename = config_helper.read_filename(company_name)

	cms_instance = CmsInstance()
	cms_operations = CmsOperations(cms_instance)
	web_driver = cms_instance.driver

	data_pipeline = DataPipeline(
		filename=filename,
		web_driver=web_driver,
		company_name=company_name
	)

	# Scrape data from web pages
	if start_at_beginning:
		data_pipeline.scrape_and_save_data()
		if not ask_user_if_continue_after_scraping():
			sys.exit()

	# Add data to CMS
	cms_operations.instantiate_cms_add_page()
	controller = data_pipeline.read_data_and_enter_into_cms()

	if data_pipeline.check_for_failed_runs(controller):
		print(f'Some listings failed to be recorded in {company_name} data')

	print('Complete! Please check site listings to ensure data is correct')