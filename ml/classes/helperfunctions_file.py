import re


class HelperFunctions:
    def __init__(self):
        pass

    def return_price_int(self, price):
        if price is None:
            return 0
        try:
            price = re.sub("[^0-9]", "", price)  # Keep only numeric characters
            if price == "":
                return 0
            return int(price)
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0

    def return_int(self, value):
        if value is None:
            return 0
        try:
            return int(value)
        except Exception as e:
            print(f"An error occurred: {e}")

    def return_bool(self, value):
        try:
            return bool(value)
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def return_str(self, value):
        try:
            return str(value)
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""

    def return_dict(self, value):
        try:
            return dict(value)
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}

    def return_list(self, value):
        try:
            return list(value)
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
