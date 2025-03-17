# CHIPS
> *CHImie en PaléoSidérurgie*

<p align="center">
  <img src="../../img/bdd-chips-landing-page.png" width="600">
  <br>
    <em>CHIPS le 18/02/25</em>
</p>

voir [Python Jupyter NB](https://colab.research.google.com/drive/1EHUO9JaBNLIyNdiHLCTtPAODgFhEvgcq#scrollTo=umLAT9DA2efl)

## BBD

BDD Postgres hebergée sur les serveurs d'Huma-Num

### Tables

#### chips

La table `chips` est la table principale pour le stockage des données brutes et traitées des analyses physico-chimiques.

* ajouter

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

* `ajoute à`:
  1. vérification des données saisies dans l'XLSX (types attendus, etc.)
  2. effectue un `INSERT INTO` dans la table chips avec auto-incrémentation des indenfiants ❓updates
  3. retourne un rapport: identifiants, etc. ❓Zenodo

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
