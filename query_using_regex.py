"""Trivial example of using a regular expression in a query
"""
from terminusdb_client import WOQLClient, WOQLQuery

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
        "@key": {"@type": "Lexical", "@fields": ["name"]}
    }
    ]

instance_doc = [
    {
        "@type": "Person",
        "name": "John Smith",
    },
    {
        "@type": "Person",
        "name": "Jane Smith",
    },
    {
        "@type": "Person",
        "name": "Jim Smythe",
    },
    ]

client = WOQLClient("http://127.0.0.1:6363/")
client.connect()
try:
    client.create_database(db_name, team="admin")
    client.insert_document(schema_doc, graph_type="schema", full_replace=True)
    client.insert_document(instance_doc, graph_type="instance")
    assert 3 == len(list(client.get_all_documents()))
    q = WOQLQuery()
    q = q.triple("v:Person", "rdf:type", "@schema:Person")
    q = q.triple("v:Person", "name", "v:Name")
    q = q.re("Smith", "v:Name", "v:Result")
    r = q.execute(client)
    assert 2 == len(r.get("bindings"))
finally:
    print(f"Deleting database {db_name}")
    client.delete_database(dbid=db_name, team="admin")
    client.close()
