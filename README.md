# Airtable Export to JSON

A simple Python script to export multiple Airtable tables from the same base to JSON files using the [PyAirtable](https://github.com/gtalarico/pyairtable) library.  
It reads configuration from a single `airtable.json` file, making it ideal for batch exporting multiple tables into local `.json` files.

---

## 🔧 Features

- No CLI arguments required — just run the script
- Exports each Airtable table to its own file (e.g., `sites.json`, `contents.json`)
- Automatically creates output directories
- Prints execution time per table and total script duration
- Designed for automation (e.g., Cronicle or cron jobs)

---

## 📁 Example Output

If your `airtable.json` looks like this:

```json
{
  "airtable_api": "input_your_personal_access_token_here",
  "base_id": "appBDr8eF3af5CrHI",
  "tables": [
    {
      "table_name": "sites",
      "table_id": "tblJm1LB7GAw10jXv"
    },
    {
      "table_name": "contents",
      "table_id": "tblFDPsjNmsYX6Lpv"
    },
    {
      "table_name": "apps",
      "table_id": "tbl7p89FjlJQwm3wE"
    }
  ],
  "output_dir": "data"
}
````

The script will save:

```
data/sites.json
data/contents.json
data/apps.json
```

👉 The `"table_name"` field determines the filename. For example:

```json
{ "table_name": "sites" } → data/sites.json
```

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/deuts/airtable-json-export.git my-custom-folder
cd my-custom-folder
```

### 2. Install Requirements

This script uses [PyAirtable](https://github.com/gtalarico/pyairtable):

```bash
pip install pyairtable
```

### 3. Set Up `airtable.json`

Rename the provided sample config:

```bash
cp sample-airtable.json airtable.json
```

Then edit `airtable.json` with your own credentials and table settings.

#### How to find your values:

* **Airtable API Token**:
  Go to [airtable.com/account](https://airtable.com/account), scroll down to **"Developer Hub"** → **"Personal Access Tokens"**.
  Create a token with at least `data.records:read` access to your base.

* **Base ID** and **Table ID**:
  Open your Airtable base in a browser. The URL will look like this:

  ```
  https://airtable.com/appBDr8eF3af5CrHI/tblJm1LB7GAw10jXv/viwxyz...
  ```

  * `appBDr8eF3af5CrHI` is the **base\_id**
  * `tblJm1LB7GAw10jXv` is the **table\_id**

🔁 Repeat this for every table you want to export and add them to the `tables` list.

---

## 📦 Usage

Once your `airtable.json` is configured:

```bash
python get_airtable_data.py
```

You’ll see output like this:

```
→ Fetching: sites
✓ Saved 42 records to data/sites.json in 1.15 seconds

→ Fetching: contents
✓ Saved 35 records to data/contents.json in 0.95 seconds

→ Fetching: apps
✓ Saved 10 records to data/apps.json in 0.43 seconds

Script finished in 2.56 seconds
✓ All tables processed successfully.
```

The script will exit with code `0` on success and `1` on failure — useful for integration with automation tools like Cronicle or cron jobs.

---

## 📝 Notes

* This script does **not** update or write to Airtable — it only **reads and exports** data.
* Ensure your Airtable token has access to the base you indicated.
* Output files are **overwritten** on every run.

---

## 📂 File Structure

```
airtable-json-export/
├── get_airtable_data.py        ← main script
├── sample-airtable.json        ← sample config
├── airtable.json               ← your real config (add this yourself)
└── data/                       ← JSON output goes here
```