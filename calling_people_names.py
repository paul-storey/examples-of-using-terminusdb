"""Further adventures with TerminusDB

This script demonstrates a few things.

It is harmless to repeat the same triple e.g.
    Person_123, name, Bob
    Person_123, name, Bob
The names that a Person can have are specified
as a Set. Duplicates are effectively ignored.

It is possible to use triples to refer to
the relationship between a document
and its attributes. In this example, 'name'
is a property of 'Person' and the value
of 'name' for a Person can be queried
and updated using a triple in which 'name'
is used as a predicate.

Finally this example illustrates how update_document
overwrites a document if it is already present.
Thus has_doc becomes an important way of
testing for the presence of a document in order
to avoid overwriting it.

An earlier development version of this script used a 
schema with a Name class. In this way, each name
was its own document node in the graph. However
it remained true that, when a person document
got updated, its associations with name documents
was lost.
"""
from pprint import PrettyPrinter
from terminusdb_client import WOQLClient, WOQLQuery
from terminusdb_client.woqlschema import WOQLSchema
from typing import Any, Dict, List

db_name : str = "test_database"

schema_doc = [ 
    {   
        "@type": "@context",
        "@schema": "http://xyz#",
        "@base": "base://path/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    },
    {
        "@id": "Person",
        "@type": "Class",
        "@base": "Person_",
        "identifier": "xsd:string",
        "@key": 
             {
                 "@type": "Lexical",
                 "@fields": [ "identifier" ]
             },
        "name":
             {
                 "@type": "Set",
                 "@class": "xsd:string"
             }
    }
]

def add_triple(client, subj, pred, obj) -> None:
    client.query(WOQLQuery().add_triple(subj, pred, obj))

def query(client, subj, pred, obj) -> List[Any]:
    result = client.query(WOQLQuery().triple(subj, pred, obj))
    return result.get("bindings")

client = WOQLClient("http://127.0.0.1:6363/")
client.connect()
try:
    client.create_database(db_name, team="admin")
    client.insert_document(schema_doc, graph_type="schema", full_replace=True, 
            commit_msg="Define schema")
    client.update_document([{"@type": "Person", "identifier": "123"}])
    add_triple(client, "Person_123", "name", {"@type": "xsd:string", "@value": "Bob"})
    add_triple(client, "Person_123", "name", {"@type": "xsd:string", "@value": "Sue"})
    add_triple(client, "Person_123", "name", {"@type": "xsd:string", "@value": "Bob"})
    assert 2 == len(query(client, "Person_123", "name", "v:name"))
    client.update_document([{"@type": "Person", "identifier": "123"}])
    assert 0 == len(query(client, "Person_123", "name", "v:name"))
finally:
    client.delete_database(dbid=db_name, team="admin")
    client.close()

