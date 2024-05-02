from mlclass import MLClass
from pprint import pprint

ml = MLClass()
data = ml.get_data("raw_data_table", "raw_property_type, raw_property_constructionpermit_floodzonetype, ")
pprint(data)