import pandas as pd

# Replace 'input_file.xlsx' with the name of your input file
input_file = pd.read_excel('output.xlsx', sheet_name=None)

# Initialize an empty list to store each sheet's data
data_frames = []

# Loop through each sheet in the input file
for sheet_name, df in input_file.items():
    # Add a new column called "Firewall" with the source sheet name
    df['Firewall'] = sheet_name
    # Append the sheet's data to the list
    data_frames.append(df)

# Concatenate all the sheets into one DataFrame
consolidated_data = pd.concat(data_frames)

# Replace 'output_file.xlsx' with the name of your output file
consolidated_data.to_excel('formatted.xlsx', index=False)
