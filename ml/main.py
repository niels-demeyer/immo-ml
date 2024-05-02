from mlclass import MLClass
from pprint import pprint

ml = MLClass()
data = ml.get_data(
    "raw_data_table", 
    "raw_property_type, "
    "raw_property_constructionpermit_floodzonetype, "
    "raw_property_location_locality, "
    "raw_property_location_district, "
    "raw_property_building_condition, "
    "raw_property_location_postalcode, "
    "raw_transaction_sale_cadastralincome,"
    "raw_price_accessibilityprice, "
    "raw_property_subtype, "
    "raw_property_land_surface, "
    "raw_property_nethabitablesurface, "
    "raw_property_energy_heatingtype, "
    "raw_property_roomcount, "
    "raw_property_hasbasement, "
    "raw_property_hasterrace, "
    "raw_property_hasswimmingpool,"
    "raw_property_building_constructionyear, "
    "raw_property_gardensurface,"
    "raw_transaction_certificates_renovationobligation,"
    "raw_property_bathroomcount, "
    "raw_transaction_sale_isfurnished"
    ""
)
pprint(data)