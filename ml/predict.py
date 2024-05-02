from Ml_file import ModelTrainer

# Create an instance of ModelTrainer
trainer = ModelTrainer()

# Define input data (without 'price')
input_data = {
    "bathroom_count": 1,
    "building_condition": "None",
    "cadastral_income": 0,
    "construction_year": 1968,
    "district": "Maaseik",
    "floodzone_type": "None",
    "garden_surface": 0,
    "has_basement": False,
    "has_swimming_pool": False,
    "has_terrace": False,
    "heating_type": "FUELOIL",
    "is_furnished": True,
    "land_surface": 35799,
    "locality": "Oudsbergen",
    "net_habitable_surface": 0,
    "postal_code": 3670,
    "property_subtype": "MIXED_USE_BUILDING",
    "property_type": "HOUSE",
    "renovation_obligation": True,
    "room_count": 0,
    "url": "https://www.immoweb.be/en/classified/mixed-use-building/for-sale/oudsbergen/3670/10828459",
}

# Make a prediction
predicted_price = trainer.predict(input_data)

print(f"Predicted price: {predicted_price}")
