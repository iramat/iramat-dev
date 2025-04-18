# This file is useful to manage reference data from the Postgres DB

# %%

import requests 
import tempfile
import importlib.util
import os

url = 'https://raw.githubusercontent.com/zoometh/iramat-test-functions/main/chips.py'
response = requests.get(url)

# with open('bdd.py', 'w', encoding='utf-8') as f:
#     f.write(response.text)
# Save to a temporary file
with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp_file:
    tmp_file.write(response.content)
    tmp_file_path = tmp_file.name

# Import the module
module_name = "bdd"
spec = importlib.util.spec_from_file_location(module_name, tmp_file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


# %%

import bdd

# Call a function from it
bdd.db_connect()

# %%

engine = ch.db_connect("pg_credentials.json")