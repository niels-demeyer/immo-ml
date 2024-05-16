from ml.classes.PreMl_file import PreMl

preml = PreMl()

data = preml.get_data("ml_data", "*")
# print(data[0])
preml.split_data_property_type(data)
