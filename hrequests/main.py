from properties import ExtractPage
from FileUtils_class import FileUtils
import os
import pandas as pd
import glob
from dotenv import load_dotenv
import psycopg2

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

# Now you can use raw_data, single_listing_data, and page_dict as needed
# For example, you can write them to a PostgreSQL database using the FileUtils class
if single_listing_data is not None:
    file_utils.write_dict_to_postgres('raw_data_table', single_listing_data)