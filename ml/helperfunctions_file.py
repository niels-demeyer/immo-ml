class HelperFunctions:
    def __init__(self):
        pass

    def return_price_int(self, price):
        try:
            price = price.replace("€", "").replace(",", "").replace(".", "")
            return int(price)
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0

    def return_int(self, value):
        try:
            return int(value)
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0

    def return_float(self, value):
        try:
            return float(value)
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0.0

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
