from mlclass_file import MLClass
from helperfunctions_file import HelperFunctions
from pprint import pprint

ml = MLClass()
help = HelperFunctions()


def preprocess_data(self):
    data = ml.get_data("ml_data", "*")
    for row in data:
        row["price"] = help.return_price_int(row["raw_price_accessibilityprice"])
        row["bathroom_count"] = help.return_int(row["raw_property_bathroomcount"])
        row["building_condition"] = help.return_str(
            row["raw_property_building_condition"]
        )
        row["construction_year"] = help.return_int(
            row["raw_property_building_constructionyear"]
        )
        row["floodzone_type"] = help.return_str(
            row["raw_property_constructionpermit_floodzonetype"]
        )
        row["heating_type"] = help.return_str(row["raw_property_energy_heatingtype"])
        row["garden_surface"] = help.return_int(row["raw_property_gardensurface"])
        row["has_basement"] = help.return_bool(row["raw_property_hasbasement"])
        row["has_swimming_pool"] = help.return_bool(row["raw_property_hasswimmingpool"])
        row["has_terrace"] = help.return_bool(row["raw_property_hasterrace"])
        row["land_surface"] = help.return_int(row["raw_property_land_surface"])
        row["district"] = help.return_str(row["raw_property_location_district"])
        row["locality"] = help.return_str(row["raw_property_location_locality"])
        row["postal_code"] = help.return_int(row["raw_property_location_postalcode"])
        row["net_habitable_surface"] = help.return_int(
            row["raw_property_nethabitablesurface"]
        )
    return data


pprint(preprocess_data(ml))
