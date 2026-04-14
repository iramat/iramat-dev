## Patrimin
> traitement et évaluation du patrimoine minier en milieu semi-désertique


### Données

Le fichier source `BIB 4043.xlsx` vient de:

```bib
@incollection{klemm2012gold,
  title={Gold Production Sites and Gold Mining in Nubia/Sudan},
  author={Klemm, Rosemarie and Klemm, Dietrich},
  booktitle={Gold and Gold Mining in Ancient Egypt and Nubia: Geoarchaeology of the Ancient Gold Mining Sites in the Egyptian and Sudanese Eastern Deserts},
  pages={341--599},
  year={2012},
  publisher={Springer},
  bth = 4043
}
```

### workflow

Dans Pg

```sql
CREATE TABLE sites (
    name_site text,
    y float,
    x float,
    num_biblio text,
    group_site text,
    notes text
);

ALTER TABLE sites
ADD COLUMN geom geometry(Point, 4326);

UPDATE sites
SET geom = ST_SetSRID(ST_MakePoint(x, y), 4326);

CREATE INDEX sites_geom_gix
ON sites
USING GIST (geom);

ALTER TABLE sites ADD PRIMARY KEY (name_site)
```