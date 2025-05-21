from bdd import db_connect, db_upsert, db_tabi

root_path = "C:/Users/adisser/Git_repo/iramat-test/"
engine = db_connect(root_path + "credentials/pg_dev_credentials.json")
<<<<<<< HEAD
db_upsert(data_entry= root_path + "dbs/chips/data/import_tableChips_test1.csv",
                table="chips", separator = ',', engine=engine, verbose = True)
=======
db_upsert(data_entry= root_path + "dbs/chips/data/import_tableEchantillons_test.csv",
                table="echantillons", separator = ',', engine=engine, verbose = True)


# %%

>>>>>>> 09bd1e30dffaef7fdb4089ece8f18f15ba0f28bb
