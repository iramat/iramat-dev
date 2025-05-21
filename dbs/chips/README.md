# CHIPS
> *CHImie en PaléoSidérurgie*

<p align="center">
  <img src="../../img/bdd-chips-landing-page.png" width="600">
  <br>
    <em>CHIPS le 18/02/25</em>
</p>

voir [Python Jupyter NB](https://colab.research.google.com/drive/1EHUO9JaBNLIyNdiHLCTtPAODgFhEvgcq#scrollTo=umLAT9DA2efl)

## BBD
> Postgres 11, PostGis v2.5

BDD Postgres hebergée sur les serveurs d'Huma-Num

### Installation de PostgREST

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

#### Lancer plusieurs PostgresREST
> sur les BDD chips, chips_d, etc. 

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


### Tables

#### chips

La table `chips` est la table principale pour le stockage des données brutes et traitées des analyses physico-chimiques.

* description des champs: [chips_template_fields.tsv](https://github.com/zoometh/iramat-test/blob/main/dbs/chips/data/reference_data/chips_template_fields.tsv)


## Flux de travail

```mermaid
flowchart LR
    subgraph BDD_CHIPS
      tC[table chips] -- est lue par --> A[vue ICP-MS]
      tI[table instrument] -- est lue par --> A[vue ICP-MS]
    end
    subgraph local
      Xt[template XLSX];
      U[un utilsateur];
    end
    subgraph Python
      P1[fonction_1];
      P2[fonction_2];
    end
    subgraph Plateforme
      Pl1;
      Pl2;
    end
    A -- est lue par --> P1;
    P1 -- export vers --> Pl1;
    Xt -- télécharge --> Pl1;
    Xt -- est rempli par --> U;
    U -- enregistre et soumet à --> Pl2;
    Pl2 --  est lue par --> P2;
    P2 -- contrôle --> P2
    P2 -- ajoute à --> tC;

click A "https://github.com/zoometh/iramat-test/tree/main/dbs#table_chimie"
style Python fill:#02fa02
```

![#02fa02](https://placehold.co/15x15/02fa02/02fa02.png): fichiers/fonctions Python

* `contrôle`
  1. vérification des données saisies dans l'XLSX (types attendus, etc.)


* `ajoute à`:
  1. effectue un `INSERT INTO` dans la table chips avec auto-incrémentation des indenfiants ❓updates
  2. retourne un rapport: identifiants, etc. ❓Zenodo

#### _refbib

La table `_refbib` regroupe les références bibliographiques des différentes vues (*views*). Ces références sont au format BibTeX et seront mappées pour correspondre aux champs de Zenodo (table de correspondance [bibtex2zenodo.tsv](https://github.com/zoometh/iramat-test/blob/main/projects/citation/bibtex2zenodo.tsv))

* structure

| champs          | description                         |
|-----------------|-------------------------------------|
| ref_table       |  le nom de la table ou de la vue qui sera référencée par la référence bibliographique                             |
| ref_biblio      |  la référence bibliographique au format texte                           |


* ajouter

```sql
INSERT INTO _refbib (ref_table, ref_biblio)
VALUES ('instrument_incertitude','@techreport{Doe2024TechReport,
  author      = {John Doe and Jane Smith},
  title       = {A Comprehensive Guide to Dummy Data Processing},
  institution = {Institute of Advanced Computing},
  year        = {2024},
  number      = {TR-2024-001},
  address     = {New York, USA},
  month       = {February},
  note        = {Available online at \url{https://example.com/techreport}},
}');
```

### notes
  
| id_machinei         | integer   |                     |  analytical setup used to acquire isotopic amounts                |  
| id_machinem         | integer   |                     |  analytical setup used to measure major elements                |  
| id_machinet         | integer   |                     |  analytical setup used to measure trace elements                |  
