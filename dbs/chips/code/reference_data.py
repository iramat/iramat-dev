# This file is useful to manage reference data from the Postgres DB

# %%

import requests

url = 'https://raw.githubusercontent.com/zoometh/iramat-test-functions/main/chips.py'
response = requests.get(url)

with open('bdd.py', 'w', encoding='utf-8') as f:
    f.write(response.text)

# %%

import bdd

# Call a function from it
bdd.db_connect()

# %%

engine = ch.db_connect("pg_credentials.json")