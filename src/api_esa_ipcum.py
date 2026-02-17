import requests
import time
import numpy as np
import re
from astropy.table import QTable, vstack
from astropy import units as u

def get_esa_asteroids_sum():
    url = "https://neo.ssa.esa.int/PSDB-portlet/download?file=esa_risk_list"
    
    try:
        # Fetch the data
        print(f"Querying {url}...")
        response = requests.get(url)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        
        # Define Columns
        col_names = [
            "object_name", 
            "diameter_m", 
            "estimated_flag",
            "vi_max_date", 
            "ip_max", 
            "ps_max", 
            "ts", 
            "vel_km_s", 
            "years", 
            "ip_cum", 
            "ps_cum"
        ]
        
        data_rows = []
        
        # Parse Lines
        for line in lines:
            stripped_line = line.strip()
            
            # Skip empty lines or metadata headers
            if not stripped_line or stripped_line.startswith("Last Update"):
                continue
            
            # Skip the complex header lines
            if "Object" in stripped_line or "Num/des" in stripped_line or "AAAA" in stripped_line:
                continue

            # Split by pipe '|'
            raw_parts = stripped_line.split('|')
            
            # Clean whitespace from each part
            parts = [p.strip() for p in raw_parts]
            
            # Remove the very last element if it's empty
            if parts and parts[-1] == '':
                parts.pop()
                
            # Check if this looks like a valid data row
            if len(parts) >= len(col_names):
                # Take only the first 11 columns to match our names
                row_data = parts[:len(col_names)]
                data_rows.append(row_data)

        if not data_rows:
            print("Error: No valid data rows parsed.")
            return None

        # Construct QTable
        data_dict = {}
        for idx, col_name in enumerate(col_names):
            data_dict[col_name] = [row[idx] for row in data_rows]

        qtable = QTable(data_dict)

        return qtable

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Usage ---
# ESA_table_sum = get_esa_asteroids_sum()

# if ESA_table_sum:
#     print(f"\nSuccessfully created ESA QTable with {len(ESA_table_sum)} asteroids.")
    

# ESA_table_sum