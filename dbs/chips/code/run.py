from bdd import db_connect, db_upsert, db_tabi

root_path = "C:/Users/TH282424/Rprojects/iramat-test/"
engine = db_connect(root_path + "credentials/pg_dev_credentials.json")
db_upsert(data_entry= root_path + "dbs/chips/data/import_tableEchantillons_test.csv",
                table="echantillons", separator = ',', engine=engine, verbose = True)


# %%

