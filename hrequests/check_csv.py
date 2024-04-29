import pandas as pd
from pprint import pprint

# Load the CSV file as a pandas DataFrame with 'latin1' encoding
df = pd.read_csv("./outputs/output_requests(0-500).csv", encoding="ISO-8859-1")

# Now df is a DataFrame, and you can use pandas methods on it.
# Set the options
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

chunk_size = 100
for i in range(0, len(df.columns), chunk_size):
    print(df.columns[i : i + chunk_size])

print(len(df.columns))
print(len(df))
