import os
import json
import time
import sys
from pyairtable import Api

def load_config(config_file='airtable.json'):
  try:
    with open(config_file, 'r') as f:
      return json.load(f)
  except Exception as e:
    print(f"[ERROR] Failed to load config file: {e}")
    return None

def ensure_dir(path):
  os.makedirs(os.path.dirname(path), exist_ok=True)

def fetch_table(api, base_id, table_id):
  table = api.table(base_id, table_id)
  records = table.all()
  return [{"id": record["id"], **record["fields"]} for record in records]

def main():
  start_time = time.time()
  print(f"Script started at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}\n")

  config = load_config()
  if not config:
    sys.exit(1)

  api_key = config.get("airtable_api")
  base_id = config.get("base_id")
  tables = config.get("tables", [])
  output_dir = config.get("output_dir", "data")

  if not all([api_key, base_id, tables]):
    print("[ERROR] Missing required fields in airtable.json")
    sys.exit(1)

  api = Api(api_key)
  all_success = True

  for entry in tables:
    table_name = entry.get("table_name")
    table_id = entry.get("table_id")

    if not table_name or not table_id:
      print(f"[WARN] Skipping invalid table config: {entry}")
      all_success = False
      continue

    output_path = os.path.join(output_dir, f"{table_name}.json")
    ensure_dir(output_path)

    print(f"→ Fetching: {table_name}")
    table_start = time.time()

    try:
      data = fetch_table(api, base_id, table_id)
      with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
      elapsed = time.time() - table_start
      print(f"✓ Saved {len(data)} records to {output_path} in {elapsed:.2f} seconds\n")
    except Exception as e:
      elapsed = time.time() - table_start
      print(f"✗ Failed to fetch {table_name} after {elapsed:.2f} seconds: {e}\n")
      all_success = False

  total_time = time.time() - start_time
  print(f"Script finished in {total_time:.2f} seconds")

  if all_success:
    print("✓ All tables processed successfully.")
    sys.exit(0)
  else:
    print("✗ Some tables failed to process.")
    sys.exit(1)

if __name__ == "__main__":
  main()
