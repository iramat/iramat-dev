# Structuration des données produites à l'IRAMAT

## filesystem
> structure hiérarchique de dossiers/fichiers

Exemples de schémas/structures (_filesystem_ ou fs):

### fs1
> Utilisée par Terrifer

De la forme `projet` > `site` > `objet` > `échantillon`

```
├───project1
│   ├───site1
│   │   ├───objet1
│   │   │   │   macro1.jpg
│   │   │   │   macro2.jpg
│   │   │   │   macro3.jpg
│   │   │   │
│   │   │   ├───iiif1
│   │   │   │       iiif1.jpg
│   │   │   │
│   │   │   ├───metallo1
│   │   │   │       micrographie1.jpg
│   │   │   │       micrographie2.jpg
│   │   │   │       micrographie3.jpg
│   │   │   │
│   │   │   ├───metallo2
│   │   │   │       micrographie1.jpg
│   │   │   │       micrographie2.jpg
│   │   │   │
│   │   │   ├───metallo3
│   │   │   │       micrographie1.jpg
│   │   │   │
│   │   │   └───rti1
│   │   │           rti1.jpg
│   │   │
│   │   └───objet2
│   │       │   macro1.jpg
│   │       │   macro2.jpg
│   │       │
│   │       ├───iiif1
│   │       │       iiif1.jpg
│   │       │
│   │       ├───iiif2
│   │       │       iiif1.jpg
│   │       │
│   │       ├───iiif3
│   │       │       iiif1.jpg
│   │       │
│   │       ├───metallo1
│   │       │       micrographie1.jpg
│   │       │       micrographie2.jpg
│   │       │
│   │       ├───metallo2
│   │       │       micrographie1.jpg
│   │       │
│   │       └───rti1
│   │               rti1.jpg
│   │
│   └───site2
│       ├───objet1
│       │   │   macro1.jpg
│       │   │   macro2.jpg
│       │   │
│       │   ├───iiif1
│       │   │       iiif1.jpg
│       │   │
│       │   ├───metallo1
│       │   │       micrographie1.jpg
│       │   │       micrographie2.jpg
│       │   │       micrographie3.jpg
│       │   │
│       │   ├───metallo2
│       │   │       micrographie1.jpg
│       │   │       micrographie2.jpg
│       │   │
│       │   └───metallo3
│       │           micrographie1.jpg
│       │
│       └───objet2
│           │   macro1.jpg
│           │
│           ├───metallo1
│           │       micrographie1.jpg
│           │       micrographie2.jpg
│           │
│           ├───metallo2
│           │       micrographie1.jpg
│           │
│           ├───rti1
│           │       rti1.jpg
│           │
│           └───rti2
│                   rti1.jpg
│
└───project2
    ├───site1
    │   ├───objet1
    │   │   │   macro1.jpg
    │   │   │   macro2.jpg
    │   │   │   macro3.jpg
    │   │   │
    │   │   ├───iiif1
    │   │   │       iiif1.jpg
    │   │   │
    │   │   ├───iiif2
    │   │   │       iiif1.jpg
    │   │   │
    │   │   ├───metallo1
    │   │   │       micrographie1.jpg
    │   │   │       micrographie2.jpg
    │   │   │       micrographie3.jpg
    │   │   │
    │   │   ├───metallo2
    │   │   │       micrographie1.jpg
    │   │   │       micrographie2.jpg
    │   │   │
    │   │   ├───metallo3
    │   │   │       micrographie1.jpg
    │   │   │
    │   │   └───rti1
    │   │           rti1.jpg
    │   │
    │   ├───objet2
    │   │   │   macro1.jpg
    │   │   │   macro2.jpg
    │   │   │
    │   │   ├───iiif1
    │   │   │       iiif1.jpg
    │   │   │
    │   │   └───metallo1
    │   │           micrographie1.jpg
    │   │           micrographie2.jpg
    │   │
    │   └───objet3
    │       │   macro1.jpg
    │       │
    │       ├───metallo1
    │       │       micrographie1.jpg
    │       │       micrographie2.jpg
    │       │
    │       ├───metallo2
    │       │       micrographie1.jpg
    │       │
    │       ├───rti1
    │       │       rti1.jpg
    │       │
    │       └───rti2
    │               rti1.jpg
    │
    └───site2
        └───objet1
            │   macro1.jpg
            │
            ├───iiif1
            │       iiif1.jpg
            │
            ├───metallo1
            │       micrographie1.jpg
            │       micrographie2.jpg
            │       micrographie3.jpg
            │
            ├───metallo2
            │       micrographie1.jpg
            │       micrographie2.jpg
            │
            └───metallo3
                    micrographie1.jpg
```
