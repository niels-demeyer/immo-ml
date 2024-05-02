from PreMl_file import PreMl
from helperfunctions_file import HelperFunctions
from pprint import pprint

ml = PreMl()
help = HelperFunctions()


def preprocess_data():
    data = ml.get_data("ml_data", "*")
    processed_data = []
    for row in data:
        processed_row = {}
        processed_row["price"] = help.return_price_int(
            row["raw_price_accessibilityprice"]
        )
        processed_row["bathroom_count"] = help.return_int(
            row["raw_property_bathroomcount"]
        )
        processed_row["building_condition"] = help.return_str(
            row["raw_property_building_condition"]
        )
        processed_row["construction_year"] = help.return_int(
            row["raw_property_building_constructionyear"]
        )
        processed_row["floodzone_type"] = help.return_str(
            row["raw_property_constructionpermit_floodzonetype"]
        )
        processed_row["heating_type"] = help.return_str(
            row["raw_property_energy_heatingtype"]
        )
        processed_row["garden_surface"] = help.return_int(
            row["raw_property_gardensurface"]
        )
        processed_row["has_basement"] = help.return_bool(
            row["raw_property_hasbasement"]
        )
        processed_row["has_swimming_pool"] = help.return_bool(
            row["raw_property_hasswimmingpool"]
        )
        processed_row["has_terrace"] = help.return_bool(row["raw_property_hasterrace"])
        processed_row["land_surface"] = help.return_int(
            row["raw_property_land_surface"]
        )
        processed_row["district"] = help.return_str(
            row["raw_property_location_district"]
        )
        processed_row["locality"] = help.return_str(
            row["raw_property_location_locality"]
        )
        processed_row["postal_code"] = help.return_int(
            row["raw_property_location_postalcode"]
        )
        processed_row["net_habitable_surface"] = help.return_int(
            row["raw_property_nethabitablesurface"]
        )
        processed_row["room_count"] = help.return_int(row["raw_property_roomcount"])
        processed_row["property_subtype"] = help.return_str(row["raw_property_subtype"])
        processed_row["property_type"] = help.return_str(row["raw_property_type"])
        processed_row["renovation_obligation"] = help.return_bool(
            row["raw_transaction_certificates_renovationobligation"]
        )
        processed_row["cadastral_income"] = help.return_int(
            row["raw_transaction_sale_cadastralincome"]
        )
        processed_row["is_furnished"] = help.return_bool(
            row["raw_transaction_sale_isfurnished"]
        )
        processed_row["url"] = row["url"]
        processed_data.append(processed_row)
    return processed_data


preprocessed_data = preprocess_data()
pprint(preprocessed_data[0])
# ml.save_to_pre_ml_data(preprocessed_data)
