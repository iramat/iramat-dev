# Métadonnées

---

1. Les métadonnées sont objet d'une discussion: https://github.com/orgs/iramat/discussions/51
2. Les métadonnées identifiées pertinentes: [metadata_dev.tsv](./metadata_dev.tsv)

Des tests utilisant des [images](./img/) et des [templates](./templates/).

## Liste

Une fois la liste [metadata_dev.tsv](./metadata_dev.tsv) validée, les métadonnées doivent aller ici: https://github.com/iramat/iramat-apps/blob/hugo-files/static/data/metadata.tsv

### Identifées dans le XMP de XnView

Les métadonnées suivantes ont été correctement identifiées dans le fichier d'[export XMP des métadonnées](./templates/photo/XnView_metadata_template.xmp) d'une image depuis XnView

- [ ] Nom du champ dans le logiciel   Nom du champ standard
- [ ] Document Title  dc:title
- [ ] Document Identifiant  dc:identifier
- [ ] Author  dc:creator
- [ ] Description dc:description
- [ ] Keywords  dc:subject
- [ ] Source  dc:source
- [ ] Image Rights  dc:rights
- [ ] References  dcterms:references
- [ ] Collection Owner  Iptc4xmpExt:AOSource
- [ ] Collection Location Iptc4xmpExt:AOLocation
- [ ] Object Identifier/Inventory Number  Iptc4xmpExt:AOSourceInvNo
- [ ] Catalog URL Iptc4xmpExt:AOCatalogURL
- [ ] Temporal Coverage dcterms:temporal

## Templates

issus de:

- [microscopie optique](./templates/micro-opt/) (AXIO Zeiss du LAPA)
- [photographie classique](./templates/photo/)
