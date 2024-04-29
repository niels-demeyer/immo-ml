from properties import ExtractPage
from FileUtils_class import FileUtils
import os
import pandas as pd
import glob

# Create an instance of ExtractPage with a URL
page = ExtractPage("https://www.immoweb.be/en/classified/house/for-sale/sint-martens-latem/9830/11238297")

# Print the raw data
print(page.raw)

# Print whether it's a single listing
print(page.single)