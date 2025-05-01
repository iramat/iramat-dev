from bdd import db_connect, db_upsert, db_tabi

root_path = "C:/Users/TH282424/Rprojects/iramat-test/"
engine = db_connect(root_path + "credentials/pg_dev_credentials.json")
db_upsert(data_entry= root_path + "dbs/chips/data/import_tableEchantillons_test.csv",
                table="echantillons", separator = ',', engine=engine, verbose = True)


# %%

from bdd import db_connect, db_query

root_path = "C:/Users/TH282424/Rprojects/iramat-test/"
engine = db_connect(root_path + "credentials/pg_dev_credentials.json")
conn = engine.raw_connection()
cur = conn.cursor

table="machines"
excl_field="id_dispositif"

df=db_query(query = f"SELECT * FROM {table};", engine=engine)
df = df.drop(excl_field, axis=1)
# df.head()
sub = dt.Frame(df)


# %%