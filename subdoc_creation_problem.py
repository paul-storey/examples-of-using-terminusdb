import json
from pprint import PrettyPrinter
from terminusdb_client import WOQLClient, WOQLQuery
from terminusdb_client.woqlschema import WOQLSchema

db_name : str = "test_database"

schema_doc = [
    {
        "@type": "@context",
        "@schema": "http://xyz#",
        "@base": "xyz://base/path/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    },
    {
        "@id": "QualifiedPersonLink",
        "@type": "Class",
        "@subdocument": [],
        "@key": {
            "@type": "Random"
        },
        "person": "Person",
        "qualifier": "xsd:string"
    },
    {
        "@id": "Person",
        "@type": "Class",
        "name": "xsd:string",
        "@key": {
            "@type": "Lexical",
            "@fields": [ "name" ]
            },
    },
    {
        "@id": "Work",
        "@type": "Class",
        "title": "xsd:string",
        "@key": {
            "@type": "Lexical",
            "@fields": [ "title" ]
            },
        "about_qualified": {
            "@class": "QualifiedPersonLink",
            "@type": "Set"
            },
        "about": {
            "@class": "Person",
            "@type": "Set"
            },
    }
    ]

instance_docs = [
    {
        "@type": "Work",
        "title": "Ideas"
    },
    {
        "@type": "Person",
        "name": "Bob"
    }

]

client = WOQLClient("http://127.0.0.1:6363/")
client.connect()
try:
    client.create_database(db_name, team="admin")
    client.insert_document(schema_doc, graph_type="schema", full_replace=True,
            commit_msg="Define schema")
    client.insert_document(instance_docs)
    for doc in client.get_all_documents():
        print(doc)
    client.query(WOQLQuery().add_triple("Work/Ideas", "about", "Person/Bob"))
    client.query(WOQLQuery().add_triple("Work/Ideas", "about_qualified",
        {
            "@type": "QualifiedPersonLink",
            "person": "Person/Bob",
            "qualifier": "according to Bob"
        }))
    for doc in client.get_all_documents():
        print(doc)
finally:
    client.delete_database(dbid=db_name, team="admin")
    client.close()

