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
raw_data = page.raw

# Write the raw data to the PostgreSQL database
file_utils.write_dict_to_postgres('raw_data_table', raw_data)

# Get whether it's a single listing
single = page.single

# Write the single data to the PostgreSQL database
file_utils.write_dict_to_postgres('single_data_table', {'single': single})