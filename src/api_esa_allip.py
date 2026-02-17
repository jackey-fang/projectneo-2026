import requests
import time
import numpy as np
import re
from astropy.table import QTable, vstack
from astropy import units as u


def get_esa_asteroids():
    base_url = "https://neo.ssa.esa.int/PSDB-portlet/download"
    
    # Fetch the Master Risk List to get Object Designations
    print("Fetching master risk list...")
    try:
        r = requests.get(f"{base_url}?file=esa_risk_list")
        r.raise_for_status()
        risk_list_lines = r.text.splitlines()
    except Exception as e:
        print(f"Failed to fetch risk list: {e}")
        return None

    # Parse designations from the risk list
    designations = []
    for line in risk_list_lines:
        line = line.strip()
        # Skip headers and metadata
        if not line or "Last Update" in line or "Object" in line or "Num/des" in line or "AAAA" in line:
            continue
        
        parts = [p.strip() for p in line.split('|')]
        if parts:
            # Extract the ID. 
            # Take the first part of the string to get the lookup key.
            raw_name = parts[0]
            clean_desig = raw_name.split()[0]
            designations.append(clean_desig)

    print(f"Found {len(designations)} objects in risk list.")
    
    # Iterate through objects and fetch "Possible Impacts" for each
    all_impacts_rows = []
    
    # --- CONFIGURATION ---
    # Set this to None to fetch ALL objects (will take a long time).
    # Set to a number (e.g., 5) to test the code quickly.
    MAX_OBJECTS = None  
    # ---------------------

    count = 0
    for desig in designations:
        if MAX_OBJECTS and count >= MAX_OBJECTS:
            print(f"\nReached limit of {MAX_OBJECTS} objects. Stopping.")
            break
            
        print(f"\rFetching: {desig:<20} ({count + 1}/{len(designations)})", end="", flush=True)

        time.sleep(0.1) 
        
        try:
            # Request the specific risk file
            # URL Pattern: download?file={designation}.risk
            file_url = f"{base_url}?file={desig}.risk"
            r_obj = requests.get(file_url)
            
            if r_obj.status_code == 200:
                # Parse the "Possible Impacts" table
                obj_lines = r_obj.text.splitlines()
                parsing_data = False
                
                for line in obj_lines:
                    line = line.strip()
                    
                    # Detect start of data
                    # Skip header lines
                    if "Object:" in line or "YYY" in line or "----" in line or "MJD" in line:
                        continue
    
                    # Stop if we hit the footer
                    if not line or line.startswith("<"):
                        continue
                        
                    # Parse Data Line
                    parts = line.split()
                    
                    # Check if the first part starts with a digit and contains a dash.
                    if not (parts[0][0].isdigit() and '-' in parts[0]):
                        continue

                    if len(parts) >= 10:
                        # Create a row dict
                        # Map columns based on the documentation order
                        row = {
                            'object_name': desig,
                            'date': parts[0],
                            'mjd': float(parts[1]),
                            'sigma': float(parts[2]),
                            'sigimp': float(parts[3]),
                            'dist': float(parts[4]),
                        }
                        
                        # Handle the "+/-" column shift
                        current_idx = 5
                        if parts[current_idx] == '+/-':
                            current_idx += 1
                        
                        row['width'] = float(parts[current_idx])
                        row['stretch'] = float(parts[current_idx+1])
                        row['p_re'] = float(parts[current_idx+2]) # Impact Probability
                        row['exp_energy'] = float(parts[current_idx+3])
                        row['ps'] = float(parts[current_idx+4])
                        row['ts'] = float(parts[current_idx+5])
                        
                        all_impacts_rows.append(row)
                        parsing_data = True
                        
            else:
                print(f"  -> Failed (Status {r_obj.status_code})")

        except Exception as e:
            print(f"  -> Error: {e}")
            
        count += 1

    # Create QTable
    if not all_impacts_rows:
        print("No impact data found.")
        return None
        
    # Convert list of dicts to dict of lists for QTable
    keys = all_impacts_rows[0].keys()
    data_dict = {k: [row[k] for row in all_impacts_rows] for k in keys}
    
    qtable = QTable(data_dict)
    return qtable

# --- Usage ---
# ESA_table = get_esa_asteroids()

# if ESA_table:
#     print(f"\nSuccessfully retrieved {len(ESA_table)} possible impacts.")
#     print(ESA_table[:5])

# ESA_table