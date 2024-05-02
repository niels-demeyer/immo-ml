from ml.mlclass_file import MLClass
from pprint import pprint

ml = MLClass()
data = ml.preprocess_data()
pprint(data[0])
