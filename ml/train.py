from Ml_file import ModelTrainer

ml = ModelTrainer()
data = ml.clean_data()
print(data.columns)
#print the data types 
print(data.dtypes)

ml.train_model(data=data)
