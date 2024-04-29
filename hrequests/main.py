from properties import ExtractPage
from FileUtils_class import FileUtils
import os
import pandas as pd
import glob
from dotenv import load_dotenv
import psycopg2
from pprint import pprint
load_dotenv()
port = os.getenv("DB_PORT")
password = os.getenv("DB_PASS")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")

# Create an instance of FileUtils
file_utils = FileUtils()
# Create an instance of ExtractPage with a URL
page = ExtractPage("https://www.immoweb.be/en/classified/house/for-sale/sint-martens-latem/9830/11238297")

# Get the raw data
raw_data = page.get_raw_data()

# Check if it's a single listing and get the raw data if it is
single_listing_data = page.check_and_return_single_listing()

# Convert the page data to a dictionary
page_dict = page.to_dict()
# pprint(page_dict)

def remove_key_recursive(dict_, key_to_remove):
    if isinstance(dict_, dict):
        for key in list(dict_.keys()):
            if key == key_to_remove:
                dict_.pop(key)
            else:
                remove_key_recursive(dict_[key], key_to_remove)
    elif isinstance(dict_, list):
        for item in dict_:
            remove_key_recursive(item, key_to_remove)

# Now use this function to remove 'media' key from the dictionary
remove_key_recursive(page_dict, 'media')
print(page_dict)
# Now you can use raw_data, single_listing_data, and page_dict as needed
# For example, you can write them to a PostgreSQL database using the FileUtils class
if single_listing_data is not None:
    file_utils.write_dict_to_postgres('raw_data_table', page_dict)
    