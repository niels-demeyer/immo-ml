from PreMl_file import PreMl
from helperfunctions_file import HelperFunctions
from pprint import pprint

ml = PreMl()

raw_data = ml.get_data("raw_data_table", "*")

houses, apartments = ml.split_data_property_type(raw_data)
