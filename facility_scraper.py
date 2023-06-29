# This file is intended only to populate the facility mapping object!
import json
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from src.cms.cms_instance import CmsInstance
from src.cms.cms_operations import CmsOperations

cms_instance = CmsInstance()
web_driver = cms_instance.driver
cms_operations = CmsOperations(
	web_driver=web_driver
)
time.sleep(2)
cms_operations.instantiate_cms_add_page()
facility_mapping_dict = {}
i = 1
while True:
	try:
		facility = web_driver.find_element(By.XPATH, f'//*[@id="id_features_from"]/option[{i}]')
		facility_mapping_dict[facility.text.lower()] = str(i)
		i += 1
	except NoSuchElementException:
		break

with open('src/util/facility_mapping.json', 'w') as f:
	json.dump(facility_mapping_dict, f)
