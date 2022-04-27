"""label property needs to be qualified in queries

"""
from terminusdb_client import WOQLClient, WOQLQuery
from terminusdb_client.woqlschema import WOQLSchema

db_name : str = "test_database"

schema_doc = [
    {
        "@type": "@context",
        "@schema": "http://example#",
        "@base": "base://example/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    },
    {
        "@id": "Person",
        "@type": "Class",
        "@base": "Person_",
        "name": "xsd:string",
        "@key":
            {
                "@type": "Lexical",
                "@fields": [ "name" ]
            },
        "label": "xsd:string",
        "badge": "xsd:string"
    },
    ]

instance_doc = [
    {
        "@type": "Person",
        "name": "Bob",
        "label": "Stinky",
        "badge": "sheriff"
    },
    ]

def get_bindings(subj, pred, obj) -> str:
    result = client.query(WOQLQuery().triple(subj, pred, obj))
    return result.get("bindings")

client = WOQLClient("http://127.0.0.1:6363/")
client.connect()
try:
    client.create_database(db_name, team="admin")
    client.insert_document(schema_doc, graph_type="schema", full_replace=True)
    client.insert_document(instance_doc, graph_type="instance")
    for d in client.get_all_documents():
        print(d)
    assert 1 == len(get_bindings("Person_Bob", "name", "v:Out"))
    assert 1 == len(get_bindings("Person_Bob", "badge", "v:Out"))
    assert 0 == len(get_bindings("Person_Bob", "label", "v:Out"))
    assert 1 == len(get_bindings("Person_Bob", "@schema:label", "v:Out"))
finally:
    print(f"Deleting database {db_name}")
    client.delete_database(dbid=db_name, team="admin")
    client.close()

