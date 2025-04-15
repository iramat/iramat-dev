
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

Avec le daemon cron:


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

