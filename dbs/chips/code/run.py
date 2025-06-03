#%% load functions and root path
# TODO: remove the separator parameter (handled with csv.Sniffer)

from bdd import db_connect, db_upsert, db_tabi
# root_path = "C:/Users/adisser/Git_repo/iramat-test/"
root_path = "C:/Users/TH282424/Rprojects/iramat-dev/"

#%% Upsert table 'chips' (chips_d DB, development database)

table = 'chips'
engine = db_connect(root_path + "credentials/pg_dev_credentials.json")
db_upsert(data_entry= root_path + "dbs/chips/data/_import_tableChips_test.csv",
                table=table, separator = ',', engine=engine, verbose = True)

#%% Upsert table 'echantillons' (chips_d DB, development database)

table = 'echantillons'
engine = db_connect(root_path + "credentials/pg_dev_credentials.json")
db_upsert(data_entry= root_path + "dbs/chips/data/_import_tableEchantillons_test.csv",
                table=table, separator = ',', engine=engine, verbose = True)

# %%

table = 'sites'
engine = db_connect(root_path + "credentials/pg_dev_credentials.json")
db_upsert(data_entry= root_path + "dbs/chips/data/_import_tableSites_test.csv",
                table=table, separator = ',', engine=engine, verbose = True)