import pandas as pd
import os

# List of CSV files to be combined
csv_files = ["APSRTC_bus_details.csv","ASTC_bus_detais.csv","BSRTC_bus_detais.csv","HRTC_bus_details.csv","KSRTC_bus_details.csv","RSRTC_bus_details.csv","South_Bengal_bus_details.csv","TSRTC_bus_details.csv","UPSRTC_bus_details.csv","WBTC_bus_details.csv "]# Add the path of your CSV files

# Create an empty DataFrame to hold the combined data
combined_csv = pd.DataFrame()

# Loop through each CSV file and append its content to the combined DataFrame
for file in csv_files:
    df = pd.read_csv(file)  # Read each CSV file
    combined_csv = pd.concat([combined_csv, df], ignore_index=True)  # Append to combined DataFrame

# Save the combined CSV to a new file
combined_csv.to_csv('Bus_data_file.csv', index=False)  # Save the combined DataFrame to a new CSV file
