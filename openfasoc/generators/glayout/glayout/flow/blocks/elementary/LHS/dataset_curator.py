import json
import pandas as pd

# Paths
input_json = 'sweep_outputs/sweep_results.json'
output_jsonl = 'sweep_outputs/sweep_results.jsonl'
output_csv  = 'sweep_outputs/sweep_results.csv'

# 1. Load full JSON results
with open(input_json, 'r') as f:
    data = json.load(f)

# 2. Write JSONL (one record per line)
with open(output_jsonl, 'w') as f:
    for rec in data:
        f.write(json.dumps(rec) + "\n")

# 3. Flatten and assemble tabular DataFrame
records = []
for rec in data:
    flat = {
        'pcell': rec.get('pcell'),
        'index': rec.get('index')
    }
    # Flatten params
    for k, v in rec.get('params', {}).items():
        flat[f'param_{k}'] = v
    # Flatten report
    for k, v in rec.get('report', {}).items():
        flat[f'report_{k}'] = v
    records.append(flat)

df = pd.DataFrame(records)

# 4. Save CSV
df.to_csv(output_csv, index=False)

# 5. Display summary
print(f"Written {len(data)} records to:")
print(f" - JSONL: {output_jsonl}")
print(f" - CSV:   {output_csv}")
