import code
from pprint import PrettyPrinter
from terminusdb_client import WOQLClient, WOQLQuery
from terminusdb_client.woqlschema import WOQLSchema

db_name : str = "one_way"

# This example illustrates that it is possible to
# query 'upstream'. Take the following graph as
# an example:
# 
#        n
#       /
#      p->n
#     /
#    cr->p->n
#   /   /
# ie<-cr->p->n
#          \
#           n
# 
# Key:
# n: name
# p: person
# cr: catalogue record
# ie: intellectual entity (aka stuff)
#
# In words:
# a person has zero or more names
# a catalogue record refers to zero or more people
# a catalogue record describes an intellectual entity
#      
# It is possible to start from a node on the right (a name)
# and arrive at the left-most node (an intellectual entity)
# despite the fact that some of the relationships in the graph
# are defined left-to-right e.g. person->name and
# cataloguerecord->person

schema_doc = [ 
    {   
        "@type": "@context",
        "@schema": "http://xyz#",
        "@base": "base://path/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    },
    {
        "@id": "Stuff",
        "@type": "Class",
        "@base": "Stuff_",
        "ark": "xsd:string",
        "@key": {"@type": "Lexical", "@fields": ["ark"]},
    },
    {
        "@id": "CatalogueRecord",
        "@type": "Class",
        "@base": "CatalogueRecord_",
        "shelfmark": "xsd:string",
        "@key": {"@type": "Lexical", "@fields": ["shelfmark"]},  
        "describes": "Stuff",
        "refersto": {"@type": "Set", "@class": "Person"}
    },
    {
        "@id": "Person",
        "@type": "Class",
        "@base": "Person_",
        "unique_id": "xsd:string",
        "name": {"@type": "Set", "@class": "xsd:string"},
        "@key": {"@type": "Lexical", "@fields": ["unique_id"]},
    }
    ]

instance_doc = [
    {
        "@type": "Stuff",
        "ark": "stuff-1"
    },
    {
        "@type": "CatalogueRecord",
        "shelfmark": "MS. Col. f. 1",
        "describes": "Stuff_stuff-1",
        "refersto": ["Person_bob"]
    },
    {
        "@type": "Person",
        "unique_id": "bob",
        "name": ["Bobbie", "Robert", "Bob", "Rob"]
    },
    {
        "@type": "Person",
        "unique_id": "robert",
        "name": ["Bobbie", "Robert", "Bob", "Rob"]
    },
    ]

def prettyprint(obj, printer=PrettyPrinter(indent=4)):
    printer.pprint(obj)

client = WOQLClient("http://127.0.0.1:6363/")
client.connect()
try:
    client.create_database(db_name, team="admin")
    client.insert_document(schema_doc, graph_type="schema", full_replace=True, 
            commit_msg="Define schema")
    client.update_document(instance_doc)
    for d in client.get_all_documents():
        print(d)
    # Find me stuff related to somebody that some people call "Rob"
    query: WOQLQuery = WOQLQuery()\
        .triple("v:All the Robs", "rdf:type", "@schema:Person")\
        .triple("v:All the Robs", "name", WOQLQuery().string("Rob"))\
        .triple("v:Records referring to a Rob", "refersto", "v:All the Robs")\
        .triple("v:Records referring to a Rob", "rdf:type", "@schema:CatalogueRecord")\
        .triple("v:Records referring to a Rob", "describes", "v:Stuff associated with a Rob")
    prettyprint(client.query(query))
finally:
    print(f"Deleting database {db_name}")
    client.delete_database(dbid=db_name, team="admin")
    client.close()

