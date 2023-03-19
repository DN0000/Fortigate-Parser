import os
import json
import pandas as pd

# Get all json files in the current directory
json_files = [f for f in os.listdir('.') if f.endswith('.json')]

# Loop through each json file and convert to excel
for file in json_files:
    # Read json file
    with open(file, 'r') as f:
        data = json.load(f)
    # Convert to pandas dataframe
    df = pd.json_normalize(data)
    # Create excel writer object
    writer = pd.ExcelWriter(os.path.splitext(file)[0] + '.xlsx', engine='xlsxwriter')
    # Write dataframe to worksheet named after file name
    df.to_excel(writer, sheet_name=os.path.splitext(file)[0])
    # Save and close excel writer object
    writer.save()
