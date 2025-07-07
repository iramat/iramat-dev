
## BDD

### Installation
> Postgres 11, PostGis v2.5

Sous Linux (depuis `ubuntu@vm:~$`):

```sh
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

sudo apt-get update

sudo apt-get install postgresql-11 postgresql-contrib-11
sudo apt-get install postgresql-11-postgis-2.5
sudo apt-get install postgresql-11-postgis-2.5-scripts
```

Vérifier l'installation

```sh
psql --version
## psql (PostgreSQL) 11.22 (Ubuntu 11.22-9.pgdg22.04+1)
```

Logger dans Postgres

```sh
sudo -i -u postgres
postgres@vm:~$ psql
## psql (11.22 (Ubuntu 11.22-9.pgdg22.04+1))
## Type "help" for help.
##
## postgres=# 
```

### Sauvegardes
> Sauvegardres automatisées

Avec le daemon `cron`:


```sh
crontab -e
## Ajouter
# 0 2 * * * /home/ubuntu/backup_toy_db.sh >> /home/ubuntu/backup.log 2>&1
```

Le script `backup_toy_db.sh`

```sh
#!/bin/bash

# Set variables
DB_HOST="157.136.252.188"
DB_NAME="toy_db"
DB_USER="my_user"
BACKUP_DIR="/home/ubuntu/backups"
DATE=$(date +\%F)  # YYYY-MM-DD
FILENAME="${DATE}_${DB_NAME}.sql"
FULL_PATH="$BACKUP_DIR/$FILENAME.gz"

# Export password securely
export PGPASSWORD='my_password'

# Run the dump
# pg_dump -h "$DB_HOST" -U "$DB_USER" "$DB_NAME" > "$BACKUP_DIR/$FILENAME" # without compression
pg_dump -h "$DB_HOST" -U "$DB_USER" "$DB_NAME" | gzip > "$FULL_PATH"

# remove archives older than 7 days
find "$BACKUP_DIR" -name "*.sql.gz" -type f -mtime +7 -exec rm {} \;

# Optionally unset password
unset PGPASSWORD
```

### Upsert
> Update & Insert, Mettre à jour et/ou Insérer dans la BDD

Lancer the fichier [run.py](https://github.com/zoometh/iramat-test/blob/main/dbs/chips/code/run.py). Exemple:

```py
root_path = "C:/Users/TH282424/Rprojects/iramat-test/"
engine = db_connect(root_path + "credentials/pg_dev_credentials.json")
db_upsert(data_entry= root_path + "dbs/chips/data/import_tableEchantillons_test.csv",
                table="echantillons", separator = ',', engine=engine, verbose = True)
```

- `"pg_dev_credentials.json"`: le fichier de paramètres de connection (_username_, _password_, etc.)
- `"import_tableEchantillons_test.csv"`: le CSV qui servira a l'upsert, par exemple: [import_tableEchantillons_test.csv](https://github.com/zoometh/iramat-test/blob/main/dbs/chips/data/import_tableEchantillons_test.csv)
- `"echantillons"`: le nom de la table dans laquelle sera upserté le CSV

### PostgREST


#### Installation
> Installation de PostgREST

PostgREST est une extension pour créer une API

* Dans la BD elle-même, en SQL
  - créer un nouveau rôle (`web_anon`)
  - exposer la vue `instrument_incertitude` (API)
  - accorder les droits de `web_anon` a `mon_utilisateur` (ex: utilisateur `postgres`)

```sql
CREATE ROLE web_anon NOLOGIN;
GRANT USAGE ON SCHEMA public TO web_anon;
GRANT SELECT ON instrument_incertitude TO web_anon;
GRANT web_anon TO mon_utilisateur;
```

* créer le fichier de configuration

```sh
cd /etc/postgresql/11/main
sudo nano postgrest.conf
```

Dans `postgrest.conf`:

```
db-uri = "postgres://mon_utilisateur:mon_password@localhost:5432/chips_d"
db-schema = "public"
db-anon-role = "web_anon"
server-port = 3000
```

Importer et installer PostgREST v11.2 (pour PostgreSQL v11)

```sh
cd /usr/local/bin
sudo wget https://github.com/PostgREST/postgrest/releases/download/v11.2.0/postgrest-v11.2.0-linux-static-x64.tar.xz
sudo tar -xvf postgrest-v11.2.0-linux-static-x64.tar.xz 
sudo chmod +x /usr/local/bin/postgrest
```

Tester la version:

```sh
postgrest --version
```

=> PostgREST 11.2.0

Lancer l'extension en arrière-plan

```sh
sudo nohup postgrest postgrest.conf &
```
L'URL de la vue `instrument_incertitude` est ici (par défaut sur le port `3000`): http://157.136.252.188:3000/instrument_incertitude

#### Lancer plusieurs instances
> Lancer plusieurs PostgresREST sur les BDD chips, chips_d, etc. 

Créer un deuxième fichier de configuration

```sh
cd /etc/postgresql/11/main
sudo nano postgrest_chips.conf
```

Dans `postgrest_chips.conf`, changer de port (`3000` -> `3001`):

```
db-uri = "postgres://mon_autre_utilisateur:mon_autre_password@localhost:5432/chips"
db-schema = "public"
db-anon-role = "web_anon"
server-port = 3001
```

Lancer

```sh
sudo nohup postgrest postgrest_chips.conf &
```

Accéder: 

[postgresql11.db.huma-num.fr:3001/instrument_incertitude](http://postgresql11.db.huma-num.fr:3001/instrument_incertitude)


#### Faire sortir une vue

Soit `dataset_nom` le nom de la vue, dans Postgres faire:

```sql
GRANT SELECT ON dataset_nom TO web_anon;
```

Puis consulter l'API ici: http://157.136.252.188:3000/dataset_nom

## GitHub

### Inscription

### Issues

créer: https://github.com/iramat/iramat-dev/issues/new