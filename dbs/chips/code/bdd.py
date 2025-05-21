# TODO: move everything to the function repository

def db_connect(pg_creds = 'C:/Rprojects/iramat-test/credentials/pg_credentials.json', verbose = True):
  """
  Connect a database connection (engine)

  :param pg_creds: my PG credentials (local)
  """
  from sqlalchemy import create_engine
  import json

  # read credentials (secret) and connect the Pg DB
  if verbose:
      print("Read Pg")
  with open(pg_creds, 'r') as file:
      db_config = json.load(file)
  connection_str = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
  engine = create_engine(connection_str)

  return(engine)

def db_query(query = "SELECT * FROM instrument_incertitude;", engine=None, verbose = True):
  """
  Query a database. Returns a pandas

  :param query: a SQL query, default: View 'instrument_incertitude'
  :param engine: a sqlalchemy.engine
  """
  import pandas as pd

  df = pd.read_sql(query, engine)
  return(df)

def db_store(data=None, verbose = True):
  """
  Store a dataset in a local temp file 

  :param data: a dataset
  """
  import tempfile

  tmp = tempfile.NamedTemporaryFile()
  with open(tmp.name, 'w') as f:
      f.write(data)
  
  return(tmp.name)


def db_refbib(table = "instrument_incertitude", engine=None, output_format = "JSON", verbose = True):
  """
  Query a table of bibliographic references related to different views. This bibliographic reference is for the whole Postgres table or view. It is different from bibliographic references related to rows. Bibliographic references are stored in the table '_refbib'. These references are stored as text, in a bibtex layout, in the column 'ref_biblio'. 

  :param table: the selected table or view
  :param engine: a sqlalchemy.engine
  :param output_format: the output format (default: JSON).

  >>> # JSON format (JSON object)
  >>> bibref_json = ch.db_refbib(table = "instrument_incertitude", engine=engine, output_format = "JSON")
  >>> print(f"📚 Bibliographic Reference in JSON format:\n{bibref_json}")

  >>> # IEEE format
  >>> bibref_ieee = ch.db_refbib(table = "instrument_incertitude", engine=engine, output_format = "IEEE")
  >>> print(f"📚 Bibliographic Reference in IEEE style:\n{bibref_ieee}")
  """
  import json
  import psycopg2
  import bibtexparser
  from bibtexparser.customization import convert_to_unicode
  from pybtex.database import parse_string
  from pybtex.plugin import find_plugin

  db_params = json.load(open("pg_credentials.json"))

  conn = psycopg2.connect(**db_params)
  cur = conn.cursor()
  cur.execute(f"SELECT ref_biblio FROM _refbib WHERE ref_table='{table}'")
  row = cur.fetchone()
  # Close connection
  cur.close()
  conn.close()

  try:
    bibtex_entry = row[0]  # Extract the BibTeX string
  except:
      print("Pas d'entrée bibliographique pour cette vue")

  if(output_format == "JSON"):
    #TODO: check bibtex syntax
    bib_data = bibtexparser.loads(bibtex_entry)
    output = json.dumps(bib_data.entries, indent=4, ensure_ascii=False)
    bibref = json.loads(output)
    return(bibref)
  if(output_format == "IEEE"):
    bib_data = parse_string(bibtex_entry, "bibtex")
    # Find the style formatter
    ieee_style = find_plugin("pybtex.style.formatting", "unsrt")()  # "unsrt" is closest to IEEE
    formatted_entries = ieee_style.format_entries(bib_data.entries.values())
    # return the entries as a list instead of a generator
    ieee = list(formatted_entries)
    first_bib = ieee[0]
    bibref = first_bib.text.render_as("text")
    return(bibref)
    # return(list(formatted_entries))

def zn_metadata(meta_data = None, verbose = True):
  """
  Fill a metadata template to be pushed on Zenodo from a bibtex reference stored in Postgres (table '_refbib'). This function is called after `db_refbib()`

  :param meta_data: a JSON object
  """

  #TODO: check values, map values (https://github.com/zoometh/iramat-test/blob/main/projects/citation/bibtex2zenodo.tsv)

  metadata = {
      'metadata': {
          'title': meta_data[0]['title'],
          'description': meta_data[0]['abstract'],
          'upload_type': 'dataset',
          'license': 'cc-by',
          'subjects': [{"term": "Archaeometry", "identifier": "http://id.loc.gov/authorities/subjects/sh85006517", "scheme": "url"},
                       {"term": "laboratory methods", "identifier": "https://apps.usgs.gov/thesaurus/term-simple.php?thcode=2&code=619", "scheme": "url"},
                       {"term": "chemical elements", "identifier": "https://apps.usgs.gov/thesaurus/term-simple.php?thcode=2&code=1427", "scheme": "url"}],
          'method': 'IRAMAT data entry methodology',
          'creators': [{'name': meta_data[0]['author'],
                        'affiliation': "IRAMAT"}],
          'keywords': meta_data[0]['keywords'],
          'dates': [{"start": meta_data[0]['year'], "end": meta_data[0]['year'], "type": "Collected", "description": "Lorem Ipsum dates"}],
      }
  }
  return(metadata)

def ref_dyntab(table=None, engine=None, excl_field=None, verbose = True):
  """
  Create a dynamic table from a Postgres table or view

  :param table: the name of a table
  :param engine: a Postgres connector created with the db_connect function
  :param excl_field: the name of the fields that have to be excluded from the final output
  :param verbose: verbose
  """
  import pandas as pd

  conn = engine.raw_connection()
  cur = conn.cursor()
  if verbose:
     pass
  return None


def db_tabi(data_entry=None, table=None, separator=';', engine=None, verbose = True):
  """
  Manage the temporary table i. Used in the db_upsert() function.

  Lorem ispum (doc SQL)

  :param data_entry: a CSV file
  :param engine: a Postgres connector created with the db_connect function
  :param verbose: verbose
  """
  import pandas as pd

  conn = engine.raw_connection()
  cur = conn.cursor()
  query = """
  DROP TABLE IF EXISTS i;
  ;
  """
  cur.execute(query)
  conn.commit()
  query = f"""
  CREATE TABLE i as
  TABLE {table} with no data
  ;
  """
  if verbose:
     print(query)
  cur.execute(query)
  conn.commit()
  # compare structures
  query = f"""
  SELECT column_name
  FROM information_schema.columns
 WHERE table_schema = 'public'
   AND table_name   = '{table}'
     ;"""
  table__i = cur.execute(query)
  conn.commit()
  if verbose:
     print(query)
  data_to_i = pd.read_csv(data_entry, sep=';').columns
  print(f"table   i: {table__i}")
  print(f"data to i: {data_to_i}")
  try:
    with open(data_entry, 'r', encoding='utf-8') as f:
      if verbose:
           print(f.readline())  # Try reading first line to test access
      cur.copy_expert(
          f"COPY i FROM STDIN WITH (FORMAT csv, DELIMITER '{separator}', HEADER TRUE)", f
      )
      conn.commit()
    if verbose:
      print("... temporary table i has been created (sample):")
      df = pd.read_sql("SELECT * FROM i LIMIT 3", engine)
      print(df)
  except Exception as e:
      print("❌ ERROR during CSV import:", e)
  cur.close()
  conn.close()

def db_upsert(data_entry=None, table=None, separator=';', engine=None, verbose = True):
  """
  Read a CSV file and Insert or Update (Upsert) data into a specific tables

  Lorem ispum (doc SQL)

  :param data_entry: a CSV file
  :param table: the name of a table
  :param separator: the field separator in the CSV, default: ";"
  :param engine: a Postgres connector created with the db_connect function
  :param verbose: verbose
  """
  import pandas as pd

  conn = engine.raw_connection()
  cur = conn.cursor()
  if verbose:
    print(f"Add or Update the {data_entry} dataset to the table '{table}'")
  if table == "echantillons":
    db_tabi(data_entry=data_entry, table=table, separator=separator, engine=engine, verbose=verbose)
    query = """
    INSERT INTO echantillons
    SELECT * FROM i
    ON CONFLICT (id_ech) DO UPDATE 
      SET (id_site, id_typo, nom_ech, referent, type_metal, bibreference, bibreference2, commentaire) = (excluded.id_site, excluded.id_typo, excluded.nom_ech, excluded.referent, excluded.type_metal, excluded.bibreference, excluded.bibreference2, excluded.commentaire)
      WHERE echantillons.id_site IS DISTINCT FROM excluded.id_site
      OR echantillons.id_site IS NULL 
      OR echantillons.id_typo IS DISTINCT FROM excluded.id_typo
      OR echantillons.id_typo IS NULL
      OR echantillons.nom_ech IS DISTINCT FROM excluded.nom_ech
      OR echantillons.nom_ech IS NULL 
      OR echantillons.referent IS DISTINCT FROM excluded.referent
      OR echantillons.referent IS NULL 
      OR echantillons.type_metal IS DISTINCT FROM excluded.type_metal
      OR echantillons.type_metal IS NULL
      OR echantillons.bibreference IS DISTINCT FROM excluded.bibreference
      OR echantillons.bibreference IS NULL
      OR echantillons.bibreference2 IS DISTINCT FROM excluded.bibreference2
      OR echantillons.bibreference2 IS NULL
      OR echantillons.commentaire IS DISTINCT FROM excluded.commentaire
      OR echantillons.commentaire IS NULL
    ;
    -- DROP TABLE i
    ;
    """
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

  if table == "sites":
    db_tabi(data_entry=data_entry, table=table, separator=separator, engine=engine, verbose=verbose)
    query = """
      INSERT INTO sites 
      SELECT * FROM i
      ON CONFLICT (id_site) DO UPDATE 
        SET (id_localite, nom_site, centroid, srid, longitude, latitude, date_debut, date_fin, doute_date, key_periodo, key_periodo2) = (excluded.id_localite, excluded.nom_site, excluded.centroid, excluded.srid, excluded.longitude, excluded.latitude, excluded.date_debut, excluded.date_fin, excluded.doute_date, excluded.key_periodo, excluded.key_periodo2)
        WHERE sites.id_localite IS DISTINCT FROM excluded.id_localite
        OR sites.id_localite IS NULL
        OR sites.nom_site IS DISTINCT FROM excluded.nom_site
        OR sites.nom_site IS NULL
        OR sites.centroid IS DISTINCT FROM excluded.centroid 
        OR sites.centroid IS NULL 
        OR sites.srid IS DISTINCT FROM excluded.srid
        OR sites.srid IS NULL
        OR sites.longitude IS DISTINCT FROM excluded.longitude
        OR sites.longitude IS NULL 
        OR sites.latitude IS DISTINCT FROM excluded.latitude 	
        OR sites.latitude IS NULL
        OR sites.date_debut IS DISTINCT FROM excluded.date_debut
        OR sites.date_debut IS NULL
        OR sites.date_fin IS DISTINCT FROM excluded.date_fin
        OR sites.date_fin IS NULL
        OR sites.doute_date IS DISTINCT FROM excluded.doute_date
        OR sites.doute_date IS NULL
        OR sites.key_periodo IS DISTINCT FROM excluded.key_periodo
        OR sites.key_periodo IS NULL
        OR sites.key_periodo2 IS DISTINCT FROM excluded.key_periodo2
        OR sites.key_periodo2 IS NULL
      ;
      ;
      UPDATE sites
      SET points = ST_SetSRID(ST_MakePoint(longitude, latitude),4326)
      WHERE srid = '4326'
      ;
      -- DROP TABLE i
      ;
      """
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

  if table == "chips":
      db_tabi(data_entry=data_entry, table=table, separator=separator, engine=engine, verbose=verbose)
      query = """
      INSERT INTO chips 
      SELECT * FROM i
      ON CONFLICT (id_chips) DO UPDATE 
        SET (id_ech, id_machinem, id_machinet, o, na, mg, al, si, p, s, cl, k, ca, mn, fe, perte_feu, arsenic, ba, be, bi, cd, ce, co, cr, cs, cu, dy, er, eu, ga, gd, ge, hf, ho, indium, la, lu, mo, nb, nd, ni, pb, pd, pr, rb, sb, sc, sm, sn, sr, ta, tb, th, ti, tm, u, v, w, y, yb, zn, zr, os187_os188, open, delta57fe, delta56fe, id_machinei, n_crpg, bibreference, os187_os186, os_ppt, ag, sr87_sr86, li, tl, ru, re, se, te, carbon, h, he, b, n, f, ar, br, kr, tc, rh, i, xe, ir, pt, au, hg) = (excluded.id_ech, excluded.id_machinem, excluded.id_machinet, excluded.o, excluded.na, excluded.mg, excluded.al, excluded.si, excluded.p, excluded.s, excluded.cl, excluded.k, excluded.ca, excluded.mn, excluded.fe, excluded.perte_feu, excluded.arsenic, excluded.ba, excluded.be, excluded.bi, excluded.cd, excluded.ce, excluded.co, excluded.cr, excluded.cs, excluded.cu, excluded.dy, excluded.er, excluded.eu, excluded.ga, excluded.gd, excluded.ge, excluded.hf, excluded.ho, excluded.indium, excluded.la, excluded.lu, excluded.mo, excluded.nb, excluded.nd, excluded.ni, excluded.pb, excluded.pd, excluded.pr, excluded.rb, excluded.sb, excluded.sc, excluded.sm, excluded.sn, excluded.sr, excluded.ta, excluded.tb, excluded.th, excluded.ti, excluded.tm, excluded.u, excluded.v, excluded.w, excluded.y, excluded.yb, excluded.zn, excluded.zr, excluded.os187_os188, excluded.open, excluded.delta57fe, excluded.delta56fe, excluded.id_machinei, excluded.n_crpg, excluded.bibreference, excluded.os187_os186, excluded.os_ppt, excluded.ag, excluded.sr87_sr86, excluded.li, excluded.tl, excluded.ru, excluded.re, excluded.se, excluded.te, excluded.carbon, excluded.h, excluded.he, excluded.b, excluded.n, excluded.f, excluded.ar, excluded.br, excluded.kr, excluded.tc, excluded.rh, excluded.i, excluded.xe, excluded.ir, excluded.pt, excluded.au, excluded.hg)
        WHERE chips.id_chips IS DISTINCT FROM excluded.id_chips
        OR chips.id_ech IS NULL 
        OR chips.id_machinem IS DISTINCT FROM excluded.id_machinem
        OR chips.id_machinem IS NULL
        OR chips.id_machinet IS DISTINCT FROM excluded.id_machinet
        OR chips.id_machinet IS NULL 
        OR chips.o IS DISTINCT FROM excluded.o 	
        OR chips.o IS NULL
        OR chips.na IS DISTINCT FROM excluded.na
        OR chips.na IS NULL
        OR chips.mg IS DISTINCT FROM excluded.mg
        OR chips.mg IS NULL
        OR chips.al IS DISTINCT FROM excluded.al
        OR chips.al IS NULL
        OR chips.si IS DISTINCT FROM excluded.si
        OR chips.si IS NULL
        OR chips.p IS DISTINCT FROM excluded.p
        OR chips.p IS NULL
        OR chips.s IS DISTINCT FROM excluded.s
        OR chips.s IS NULL
        OR chips.cl IS DISTINCT FROM excluded.cl
        OR chips.cl IS NULL
        OR chips.k IS DISTINCT FROM excluded.k
        OR chips.k IS NULL
        OR chips.ca IS DISTINCT FROM excluded.ca
        OR chips.ca IS NULL
        OR chips.mn IS DISTINCT FROM excluded.mn
        OR chips.mn IS NULL
        OR chips.fe IS DISTINCT FROM excluded.fe
        OR chips.fe IS NULL
        OR chips.perte_feu IS DISTINCT FROM excluded.perte_feu
        OR chips.perte_feu IS NULL
        OR chips.arsenic IS DISTINCT FROM excluded.arsenic
        OR chips.arsenic IS NULL
        OR chips.ba IS DISTINCT FROM excluded.ba
        OR chips.ba IS NULL
        OR chips.be IS DISTINCT FROM excluded.be
        OR chips.be IS NULL
        OR chips.bi IS DISTINCT FROM excluded.bi
        OR chips.bi IS NULL
        OR chips.cd IS DISTINCT FROM excluded.cd
        OR chips.cd IS NULL
        OR chips.ce IS DISTINCT FROM excluded.ce
        OR chips.ce IS NULL
        OR chips.co IS DISTINCT FROM excluded.co
        OR chips.co IS NULL
        OR chips.cr IS DISTINCT FROM excluded.cr
        OR chips.cr IS NULL
        OR chips.cs IS DISTINCT FROM excluded.cs
        OR chips.cs IS NULL
        OR chips.cu IS DISTINCT FROM excluded.cu
        OR chips.cu IS NULL
        OR chips.dy IS DISTINCT FROM excluded.dy
        OR chips.dy IS NULL
        OR chips.er IS DISTINCT FROM excluded.er
        OR chips.er IS NULL
        OR chips.eu IS DISTINCT FROM excluded.eu
        OR chips.eu IS NULL
        OR chips.ga IS DISTINCT FROM excluded.ga
        OR chips.ga IS NULL
        OR chips.gd IS DISTINCT FROM excluded.gd
        OR chips.gd IS NULL
        OR chips.ge IS DISTINCT FROM excluded.ge
        OR chips.ge IS NULL
        OR chips.hf IS DISTINCT FROM excluded.hf
        OR chips.hf IS NULL
        OR chips.ho IS DISTINCT FROM excluded.ho
        OR chips.ho IS NULL
        OR chips.indium IS DISTINCT FROM excluded.indium
        OR chips.indium IS NULL
        OR chips.la IS DISTINCT FROM excluded.la
        OR chips.la IS NULL
        OR chips.lu IS DISTINCT FROM excluded.lu
        OR chips.lu IS NULL
        OR chips.mo IS DISTINCT FROM excluded.mo
        OR chips.mo IS NULL
        OR chips.nb IS DISTINCT FROM excluded.nb
        OR chips.nb IS NULL
        OR chips.nd IS DISTINCT FROM excluded.nd
        OR chips.nd IS NULL
        OR chips.ni IS DISTINCT FROM excluded.ni
        OR chips.ni IS NULL
        OR chips.pb IS DISTINCT FROM excluded.pb
        OR chips.pb IS NULL
        OR chips.pd IS DISTINCT FROM excluded.pd
        OR chips.pd IS NULL
        OR chips.pr IS DISTINCT FROM excluded.pr
        OR chips.pr IS NULL
        OR chips.rb IS DISTINCT FROM excluded.rb
        OR chips.rb IS NULL
        OR chips.sb IS DISTINCT FROM excluded.sb
        OR chips.sb IS NULL
        OR chips.sc IS DISTINCT FROM excluded.sc
        OR chips.sc IS NULL
        OR chips.sm IS DISTINCT FROM excluded.sm
        OR chips.sm IS NULL
        OR chips.sn IS DISTINCT FROM excluded.sn
        OR chips.sn IS NULL
        OR chips.sr IS DISTINCT FROM excluded.sr
        OR chips.sr IS NULL
        OR chips.ta IS DISTINCT FROM excluded.ta
        OR chips.ta IS NULL
        OR chips.tb IS DISTINCT FROM excluded.tb
        OR chips.tb IS NULL
        OR chips.th IS DISTINCT FROM excluded.th
        OR chips.th IS NULL
        OR chips.ti IS DISTINCT FROM excluded.ti
        OR chips.ti IS NULL
        OR chips.tm IS DISTINCT FROM excluded.tm
        OR chips.tm IS NULL
        OR chips.u IS DISTINCT FROM excluded.u
        OR chips.u IS NULL
        OR chips.v IS DISTINCT FROM excluded.v
        OR chips.v IS NULL
        OR chips.w IS DISTINCT FROM excluded.w
        OR chips.w IS NULL
        OR chips.y IS DISTINCT FROM excluded.y
        OR chips.y IS NULL
        OR chips.yb IS DISTINCT FROM excluded.yb
        OR chips.yb IS NULL
        OR chips.zn IS DISTINCT FROM excluded.zn
        OR chips.zn IS NULL
        OR chips.zr IS DISTINCT FROM excluded.zr
        OR chips.zr IS NULL
        OR chips.os187_os188 IS DISTINCT FROM excluded.os187_os188
        OR chips.os187_os188 IS NULL
        OR chips.open IS DISTINCT FROM excluded.open
        OR chips.open IS NULL
        OR chips.delta57fe IS DISTINCT FROM excluded.delta57fe
        OR chips.delta57fe IS NULL
        OR chips.delta56fe IS DISTINCT FROM excluded.delta56fe
        OR chips.delta56fe IS NULL
        OR chips.id_machinei IS DISTINCT FROM excluded.id_machinei
        OR chips.id_machinei IS NULL
        OR chips.n_crpg IS DISTINCT FROM excluded.n_crpg
        OR chips.n_crpg IS NULL
        OR chips.bibreference IS DISTINCT FROM excluded.bibreference
        OR chips.bibreference IS NULL
        OR chips.os187_os186 IS DISTINCT FROM excluded.os187_os186
        OR chips.os187_os186 IS NULL
        OR chips.os_ppt IS DISTINCT FROM excluded.os_ppt
        OR chips.os_ppt IS NULL
        OR chips.ag IS DISTINCT FROM excluded.ag
        OR chips.ag IS NULL
        OR chips.sr87_sr86 IS DISTINCT FROM excluded.sr87_sr86
        OR chips.sr87_sr86 IS NULL
        OR chips.li IS DISTINCT FROM excluded.li
        OR chips.li IS NULL
        OR chips.tl IS DISTINCT FROM excluded.tl
        OR chips.tl IS NULL
        OR chips.ru IS DISTINCT FROM excluded.ru
        OR chips.ru IS NULL
        OR chips.re IS DISTINCT FROM excluded.re
        OR chips.re IS NULL
        OR chips.se IS DISTINCT FROM excluded.se
        OR chips.se IS NULL
        OR chips.te IS DISTINCT FROM excluded.te
        OR chips.te IS NULL
        OR chips.carbon IS DISTINCT FROM excluded.carbon
        OR chips.carbon IS NULL
        OR chips.h IS DISTINCT FROM excluded.h
        OR chips.h IS NULL
        OR chips.he IS DISTINCT FROM excluded.he
        OR chips.he IS NULL
        OR chips.b IS DISTINCT FROM excluded.b
        OR chips.b IS NULL
        OR chips.n IS DISTINCT FROM excluded.n
        OR chips.n IS NULL
        OR chips.f IS DISTINCT FROM excluded.f
        OR chips.f IS NULL
        OR chips.ar IS DISTINCT FROM excluded.ar
        OR chips.ar IS NULL
        OR chips.br IS DISTINCT FROM excluded.br
        OR chips.br IS NULL
        OR chips.kr IS DISTINCT FROM excluded.kr
        OR chips.kr IS NULL
        OR chips.tc IS DISTINCT FROM excluded.tc
        OR chips.tc IS NULL
        OR chips.rh IS DISTINCT FROM excluded.rh
        OR chips.y IS NULL
        OR chips.i IS DISTINCT FROM excluded.i
        OR chips.i IS NULL
        OR chips.xe IS DISTINCT FROM excluded.xe
        OR chips.xe IS NULL
        OR chips.ir IS DISTINCT FROM excluded.ir
        OR chips.ir IS NULL
        OR chips.pt IS DISTINCT FROM excluded.pt
        OR chips.pt IS NULL
        OR chips.au IS DISTINCT FROM excluded.au
        OR chips.au IS NULL
        OR chips.hg IS DISTINCT FROM excluded.hg
        OR chips.hg IS NULL
      ;
      -- DROP TABLE i
      ;
      """
      cur.execute(query)
      conn.commit()
      cur.close()
      conn.close()
  
  if table == "literature":
      db_tabi(data_entry=data_entry, table=table, separator=separator, engine=engine, verbose=verbose)
      query = """
      INSERT INTO literature
      SELECT * FROM i
      ON CONFLICT (id_lit) DO UPDATE 
        SET (authors, title, journal_book, volume, issue, pub_year, pages, url, doi, pub_type) = (excluded.authors, excluded.title, excluded.journal_book, excluded.volume, excluded.issue, excluded.pub_year, excluded.pages, excluded.url, excluded.doi, excluded.pub_type)
        WHERE literature.authors IS DISTINCT FROM excluded.authors
        OR literature.authors IS NULL 
        OR literature.title IS DISTINCT FROM excluded.title
        OR literature.title IS NULL
        OR literature.journal_book IS DISTINCT FROM excluded.journal_book
        OR literature.journal_book IS NULL 
        OR literature.volume IS DISTINCT FROM excluded.volume
        OR literature.volume IS NULL
        OR literature.issue IS DISTINCT FROM excluded.issue
        OR literature.issue IS NULL
        OR literature.pub_year IS DISTINCT FROM excluded.pub_year
        OR literature.pub_year IS NULL
        OR literature.pages IS DISTINCT FROM excluded.pages
        OR literature.pages IS NULL
        OR literature.url IS DISTINCT FROM excluded.url
        OR literature.url IS NULL
        OR literature.doi IS DISTINCT FROM excluded.doi
        OR literature.doi IS NULL 
        OR literature.pub_type IS DISTINCT FROM excluded.pub_type
        OR literature.pub_type IS NULL
      ;
      -- DROP TABLE i
      ;
      """
      cur.execute(query)
      conn.commit()
      cur.close()
      conn.close()

  if table == "machines":
      db_tabi(data_entry=data_entry, table=table, separator=separator, engine=engine, verbose=verbose)
      query = """
      INSERT INTO machines
      SELECT * FROM i
      ON CONFLICT (id_dispositif) DO UPDATE 
        SET (laboratoire, methode_analyse, marque, modele) = (excluded.laboratoire, excluded.methode_analyse, excluded.marque, excluded.modele)
        WHERE machines.laboratoire IS DISTINCT FROM excluded.laboratoire
        OR machines.laboratoire IS NULL 
        OR machines.methode_analyse IS DISTINCT FROM excluded.methode_analyse
        OR machines.methode_analyse IS NULL 
        OR machines.marque IS DISTINCT FROM excluded.marque
        OR machines.marque IS NULL 
        OR machines.modele IS DISTINCT FROM excluded.modele
        OR machines.modele IS NULL
      ;
      DROP TABLE i
      ;
      """
      cur.execute(query)
      conn.commit()
      cur.close()
      conn.close()

  if table == "typo":
      db_tabi(data_entry=data_entry, table=table, separator=separator, engine=engine, verbose=verbose)
      query = """
      INSERT INTO typo
      SELECT * FROM i
      ON CONFLICT (id_typo) DO UPDATE 
        SET (filiere, contexte, materiau, categorie, sous_categorie, filiere_en, contexte_en, materiau_en, categorie_en, sous_categorie_en, ark_frantic) = (excluded.filiere, excluded.contexte, excluded.materiau, excluded.categorie, excluded.sous_categorie, excluded.filiere_en, excluded.contexte_en, excluded.materiau_en, excluded.categorie_en, excluded.sous_categorie_en, excluded.ark_frantic)
        WHERE typo.filiere IS DISTINCT FROM excluded.filiere
        OR typo.filiere IS NULL 
        OR typo.contexte IS DISTINCT FROM excluded.contexte
        OR typo.contexte IS NULL  
        OR typo.materiau IS DISTINCT FROM excluded.materiau
        OR typo.materiau IS NULL 
        OR typo.categorie IS DISTINCT FROM excluded.categorie
        OR typo.categorie IS NULL
        OR typo.sous_categorie IS DISTINCT FROM excluded.sous_categorie
        OR typo.sous_categorie IS NULL 	
        OR typo.filiere_en IS DISTINCT FROM excluded.filiere_en
        OR typo.filiere_en IS NULL  
        OR typo.contexte_en IS DISTINCT FROM excluded.contexte_en
        OR typo.contexte_en IS NULL  
        OR typo.materiau_en IS DISTINCT FROM excluded.materiau_en
        OR typo.materiau_en IS NULL 
        OR typo.categorie_en IS DISTINCT FROM excluded.categorie_en
        OR typo.categorie_en IS NULL
        OR typo.sous_categorie_en IS DISTINCT FROM excluded.sous_categorie_en
        OR typo.sous_categorie_en IS NULL 
        OR typo.ark_frantic IS DISTINCT FROM excluded.ark_frantic
        OR typo.ark_frantic IS NULL 
      ;
      -- DROP TABLE i
      ;
      """
      cur.execute(query)
      conn.commit()
      cur.close()
      conn.close()

  if table == "incertitudes":
      db_tabi(data_entry=data_entry, table=table, separator=separator, engine=engine, verbose=verbose)
      query = """
      INSERT INTO incertitudes
      SELECT * FROM i
      ON CONFLICT (id_incertitude) DO UPDATE 
        SET (id_machine, id_element, int_min, int_max, val_incertitude) = (excluded.id_machine, excluded.id_element, excluded.int_min, excluded.int_max, excluded.val_incertitude)
        WHERE incertitudes.id_machine IS DISTINCT FROM excluded.id_machine
        OR incertitudes.id_machine IS NULL 
        OR incertitudes.id_element IS DISTINCT FROM excluded.id_element
        OR incertitudes.id_element IS NULL 
        OR incertitudes.int_min IS DISTINCT FROM excluded.int_min
        OR incertitudes.int_min IS NULL 
        OR incertitudes.int_max IS DISTINCT FROM excluded.int_max
        OR incertitudes.int_max IS NULL 
        OR incertitudes.val_incertitude IS DISTINCT FROM excluded.val.incertitudes
        OR incertitudes.val_incertitude IS NULL 
      ;
      -- DROP TABLE i
      ;
      """
      cur.execute(query)
      conn.commit()
      cur.close()
      conn.close()
