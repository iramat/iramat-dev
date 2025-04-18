# This file is useful to manage reference data from the Postgres DB

# %%

import requests 
import tempfile
import importlib.util
import os

root = 'C:/Users/TH282424/Rprojects/iramat-test/'

url = 'https://raw.githubusercontent.com/zoometh/iramat-test-functions/main/chips.py'
response = requests.get(url)

# %%
with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp_file:
    tmp_file.write(response.content)
    tmp_file_path = tmp_file.name

# Import the module
module_name = "ch"
spec = importlib.util.spec_from_file_location(module_name, tmp_file_path)
ch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ch)

# %%
# Call a function from it
engine = ch.db_connect(root + "credentials/pg_credentials.json")

# %%
my_schema = 'public'
my_table = 'chips'
query = f"""
SELECT column_name, data_type
  FROM information_schema.columns
 WHERE table_schema = '{my_schema}'
   AND table_name   = '{my_table}'
     ;
"""
df = ch.db_query(query=query, engine=engine)
df
# %%
import pandas

df.to_csv(root + 'dbs/chips/data/reference_data/chips_template_fields.tsv', sep='\t', index=False)



# %%
