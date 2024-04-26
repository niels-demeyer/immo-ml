import json


def read_json_file(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def remove_duplicates(data):
    seen = set()
    unique_items = []
    for item in data:
        href = item["href"]
        if href not in seen:
            unique_items.append(item)
            seen.add(href)
    return unique_items


# Read data from file
data = read_json_file("./output.json")


# Remove duplicates from data
unique_data = remove_duplicates(data)

# Print the number of unique items
print(f"Number of unique items: {len(unique_data)}")
print(f"Number of duplicate items: {len(data) - len(unique_data)}")
# Save unique items to a JSON file
with open("unique_data.json", "w") as f:
    json.dump(unique_data, f)
