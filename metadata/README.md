# Métadonnées

1. Les métadonnées sont objet d'une discussion: https://github.com/orgs/iramat/discussions/51
2. Les métadonnées identifiées pertinentes: [metadata_dev.tsv](./metadata_dev.tsv)

---

Des tests utilisant des [images](./img/) et des [templates](./templates/).

## Liste

Une fois la liste [metadata_dev.tsv](./metadata_dev.tsv) validée, les métadonnées doivent aller ici: https://github.com/iramat/iramat-apps/blob/hugo-files/static/data/metadata.tsv

### Identifées dans le XMP de XnView

Les métadonnées cochées n'ont pas été identifiées dans le fichier d'[export XMP des métadonnées](./templates/photo/XnView_metadata_template.xmp) d'une image depuis XnView. Les autres ont un lien vers la ligne correspondante. De la forme 'Nom du champ dans le logiciel   Nom du champ standard  lien'

- [ ] Document Title  `dc:title`  https://github.com/iramat/iramat-dev/blob/2fb3fb32de2c4c4d5bfe3e034872a1e42e347ace/metadata/templates/photo/XnView_metadata_template.xmp#L34
- [X] Document Identifiant  `dc:identifier`
- [ ] Author  `dc:creator`  https://github.com/iramat/iramat-dev/blob/2fb3fb32de2c4c4d5bfe3e034872a1e42e347ace/metadata/templates/photo/XnView_metadata_template.xmp#L31
- [ ] Description `dc:description`  https://github.com/iramat/iramat-dev/blob/2fb3fb32de2c4c4d5bfe3e034872a1e42e347ace/metadata/templates/photo/XnView_metadata_template.xmp#L32
- [X] Keywords  `dc:subject`
- [X] Source  `dc:source`
- [ ] Image Rights  `dc:rights`  https://github.com/iramat/iramat-dev/blob/2fb3fb32de2c4c4d5bfe3e034872a1e42e347ace/metadata/templates/photo/XnView_metadata_template.xmp#L33
- [X] References  `dcterms:references`
- [X] Collection Owner  `Iptc4xmpExt:AOSource`
- [X] Collection Location `Iptc4xmpExt:AOLocation`
- [X] Object Identifier/Inventory Number  `Iptc4xmpExt:AOSourceInvNo`
- [X] Catalog URL` Iptc4xmpExt:AOCatalogURL`
- [X] Temporal Coverage `dcterms:temporal`

## Templates

issus de:

- [microscopie optique](./templates/micro-opt/) (AXIO Zeiss du LAPA)
- [photographie classique](./templates/photo/)
