from PreMl_file import PreMl
from helperfunctions_file import HelperFunctions
from pprint import pprint

ml = PreMl()

# Fetch data from the specified columns
columns = ", ".join(ml.raw_column_names)
raw_data = ml.get_data("raw_data_table", columns)

clean_data = ml.clean_data(raw_data)
print(clean_data.dtypes)
# houses, apartments = ml.split_data_property_type(raw_data)
