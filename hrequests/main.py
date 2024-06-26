from properties_file import ExtractPage
from FileUtils_class import FileUtils
import os
from dotenv import load_dotenv
from pprint import pprint
import time
import random
import logging

# Set up logging
logging.basicConfig(
    filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)

try:
    load_dotenv()
    port = os.getenv("DB_PORT")
    password = os.getenv("DB_PASS")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    host = os.getenv("DB_HOST")
except Exception as e:
    logging.error("Failed to load environment variables: " + str(e))
    raise

# Create an instance of FileUtils
try:
    file_utils = FileUtils()
except Exception as e:
    logging.error("Failed to create FileUtils instance: " + str(e))
    raise


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


# Get unchecked URLs
try:
    unchecked_urls = file_utils.get_unchecked_urls()
except Exception as e:
    logging.error("Failed to get unchecked URLs: " + str(e))
    raise

# Loop through each unchecked URL
for url in unchecked_urls:
    try:
        sleep_time = random.randint(1, 5)
        time.sleep(sleep_time)
        # Create an instance of ExtractPage with the URL
        page = ExtractPage(
            url[0]
        )  # url is a tuple, so we use url[0] to get the actual URL string

        # Get the raw data
        raw_data = page.get_raw_data()

        # Check if it's a single listing and get the raw data if it is
        single_listing_data = page.check_and_return_single_listing()

        # Convert the page data to a dictionary
        page_dict = page.to_dict()

        # Remove 'media' key from the dictionary
        remove_key_recursive(page_dict, "media")

        # Now you can use raw_data, single_listing_data, and page_dict as needed
        # For example, you can write them to a PostgreSQL database using the FileUtils class
        if single_listing_data is not None:
            file_utils.write_dict_to_postgres("raw_data_table", page_dict)
        pprint(page_dict)

    except Exception as e:
        logging.error("Failed to process URL " + url[0] + ": " + str(e))
    finally:
        # Set the URL as checked in the database
        file_utils.set_checked(url[0])
