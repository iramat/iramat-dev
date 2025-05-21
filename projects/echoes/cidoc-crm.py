import networkx as nx
from rdflib import Graph, Namespace, URIRef, Literal, RDF

# Create namespaces
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
EX = Namespace("http://example.org/")

# Create an RDF graph
g = Graph()
g.bind("crm", CRM)
g.bind("ex", EX)

# Define URIs
sword = EX["MERO-123"]
identifier = EX["Identifier_MERO-123"]
location = EX["Musee_de_Cluny"]
image = EX["MERO-123_IMG001"]
manifest = EX["IIIF_Manifest_MERO-123"]
observation = EX["OBS001"]
material = EX["BladeSample"]
actor = EX["IRAMAT-CNRS"]
result = EX["Result_001"]
digital_event = EX["ImageProcessing001"]
software = EX["PythonScript_SEMEnhancer_v1.2"]
digital_twin = EX["DigitalTwin_MERO-123"]

# Add triples
g.add((sword, RDF.type, CRM["E22_Man-Made_Object"]))
g.add((sword, CRM["P1_is_identified_by"], identifier))
g.add((sword, CRM["P2_has_type"], Literal("AAT:300264578")))
g.add((sword, CRM["P55_has_current_location"], location))

g.add((image, RDF.type, CRM["E73_Information_Object"]))
g.add((image, CRM["P138_represents"], sword))
g.add((image, CRM["P2_has_type"], Literal("SEM Image")))
g.add((image, CRM["P148_is_component_of"], manifest))

g.add((observation, RDF.type, CRM["S4_Observation"]))
g.add((observation, CRM["S15_has_identified"], material))
g.add((observation, CRM["P14_carried_out_by"], actor))
g.add((observation, CRM["P39_measured"], Literal("Elemental composition")))
g.add((observation, CRM["S21_has_measurement_result"], result))

g.add((digital_event, RDF.type, CRM["D7_Digital_Machine_Event"]))
g.add((digital_event, CRM["P14_carried_out_by"], software))
g.add((software, CRM["P1_is_identified_by"], Literal("v1.2")))

g.add((digital_twin, RDF.type, CRM["E84_Information_Carrier"]))
g.add((digital_twin, CRM["P128_carries"], image))
g.add((digital_twin, CRM["P67_refers_to"], sword))

# Create a NetworkX graph from RDF
G_nx = nx.DiGraph()
for subj, pred, obj in g:
    G_nx.add_edge(str(subj), str(obj), label=str(pred))

G_nx.nodes, G_nx.edges(data=True)

