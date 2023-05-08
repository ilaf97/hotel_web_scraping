from datetime import datetime
from pathlib import Path
from user_input_helper import validate_user_input

import yaml


class ConfigHelper:

	def __init__(self):
		self.__ROOT_DIR = Path(__file__).parent.parent
		self.config_file_path = f'{self.__ROOT_DIR}/data/config.yaml'

	@staticmethod
	def user_prompt_about_generating_filename() -> bool:
		user_prompt = "The program can store all scraped data into a new JSON file.\n" \
					  "This generated new file will be named '<company_name>-YYYY-MM-DD', " \
					  "with the date being today's date.\n" \
					  "Note that generating a new file with overwrite any existing files with the same name.\n\n" \
					  "Generate new file for today's date? (Y/N)"
		user_response = input(user_prompt)
		return validate_user_input(user_response)

	def get_company_name(self) -> str:
		config = self.__open_config_file()
		company_name = config['company_data_is_from']
		return company_name

	def read_filename(self, company_name: str) -> str:
		config = self.__open_config_file()
		filename = config['file_names'][company_name]
		return filename

	def set_new_filename_in_config(self, filename: str, company_name: str):
		config = self.__open_config_file()
		config['file_names'][company_name] = filename
		with open(self.config_file_path) as f:
			yaml.safe_dump(config, f, default_flow_style=False)

	@staticmethod
	def generate_filename(company_name: str):
		current_date = datetime.today().strftime("%Y-%m-%d")
		return company_name + '-' + current_date

	@staticmethod
	def check_company_name_valid(company_name: str):
		if company_name not in ['inghams', 'crystal_ski', 'tui']:
			raise ValueError(
				f'source_company must be either "inghams", "tui" or "crystal_ski" ("{company_name}" given')

	def __open_config_file(self):
		with open(self.config_file_path) as f:
			config = yaml.safe_load(f)
		return config






