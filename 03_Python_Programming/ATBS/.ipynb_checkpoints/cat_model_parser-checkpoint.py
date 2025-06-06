import re
import pandas as pd

# Load file
with open("/Users/dantsai/python-notebooks/ATBS/Chapter7_mini_project/nyc_flood_loss_10000_realistic.txt", "r") as f:
    text = f.read()

# Split into event blocks
event_blocks = text.strip().split("\n\n")
records = []

for block in event_blocks:
    try:
        event_id = re.search(r'Event ID: (EVT\d{4})', block).group(1)
        date = re.search(r'Date: ([\d\-]+)', block).group(1)
        city = re.search(r'City: ([A-Za-z ]+)', block).group(1)
        zip_codes = ", ".join(re.findall(r'\b\d{5}\b', block))
        lat = float(re.search(r'Latitude: ([\d\.\-]+)', block).group(1))
        lon = float(re.search(r'Longitude: ([\d\.\-]+)', block).group(1))
        hazard = re.search(r'Hazard Type: (\w{3})', block).group(1)
        time = re.search(r'Time: (\d{2}:\d{2})', block).group(1)
        policyholders = re.search(r'Policyholders: (.+)', block).group(1)
        claim_refs = ", ".join(re.findall(r'CLM\d{5}', block))
        
        # New breakdown extraction
        breakdowns = re.findall(
            r'\$[\d,]+\.\d{2} \(Bldg: \$([\d,]+\.\d{2}), Cont: \$([\d,]+\.\d{2}), Bsmt: \$([\d,]+\.\d{2}), Elev: \$([\d,]+\.\d{2})\)',
            block
        )
        
        for bldg, cont, bsmt, elev in breakdowns:
            records.append({
                "Event ID": event_id,
                "Date": date,
                "City": city,
                "ZIP": zip_codes,
                "Latitude": lat,
                "Longitude": lon,
                "Hazard Type": hazard,
                "Time": time,
                "Policyholders": policyholders,
                "Claim References": claim_refs,
                "Building Loss": float(bldg.replace(",", "")),
                "Contents Loss": float(cont.replace(",", "")),
                "Basement/Foundation Loss": float(bsmt.replace(",", "")),
                "Elevator/Utility Loss": float(elev.replace(",", "")),
                "Total Loss": float(bldg.replace(",", "")) + float(cont.replace(",", "")) + float(bsmt.replace(",", "")) + float(elev.replace(",", ""))
            })

    except Exception as e:
        print(f"Skipping block due to error: {e}")

# Create DataFrame
df = pd.DataFrame(records)
csv_path = "/Users/dantsai/python-notebooks/ATBS/Chapter7_mini_project/nyc_flood_loss_10000_realistic.csv"
df.to_csv(csv_path, index=False)
print(f"Saved structured loss data to {csv_path}")
