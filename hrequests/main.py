from properties import ExtractPage
from FileUtils_class import FileUtils
import os
import pandas as pd
import glob
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
port = os.getenv("DB_PORT")
password = os.getenv("DB_PASS")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")



# Create an instance of ExtractPage with a URL
page = ExtractPage("https://www.immoweb.be/en/classified/house/for-sale/sint-martens-latem/9830/11238297")

# Print the raw data
print(page.raw)

# Print whether it's a single listing
print(page.single)