import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('ml-latest-small/merged_data.csv')

# Example of the map
user_address_map = {'1': 'address1', '2': 'address2'}

user_address_map = {};
for each in range(1000):
	user_address_map[each] = "address_" + str(each) 

print(user_address_map)
# Map the addresses to the DataFrame
df['address'] = df['userId'].map(user_address_map)

# Save the DataFrame to a new CSV file
df.to_csv('ml-latest-small/modified_merged_data.csv', index=False)
