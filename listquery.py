"""RDF collections in TerminusDB

See https://www.w3.org/TR/rdf-primer/#collections
"""
from pprint import PrettyPrinter
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
        "@type": "Enum",
        "@id": "Fruit",
        "@value": [ "apple", "pear", "orange", "banana" ],
    },
    {
        "@id": "Bowl",
        "@type": "Class",
        "@base": "Bowl_",
        "desc": "xsd:string",
        "@key": 
            {
                "@type": "Lexical",
                "@fields": [ "desc" ]
            },
        "contains":
            {
                "@type": "List",
                "@class": "Fruit"
            },
    },
    ]

instance_doc = [
    {
        "@type": "Bowl",
        "desc": "ceramic",
        "contains": [ "apple", "banana", "apple", "pear" ]
    },
    ]

def query_and_return(client, subj, pred, obj) -> str:
    query_variable: str = subj.partition(":")[2] if subj.startswith("v:") else\
        obj.partition(":")[2]
    result = client.query(WOQLQuery().triple(subj, pred, obj))
    bindings: List[Dict[str,str]] = result.get("bindings")
    assert len(bindings) == 1
    assert query_variable in bindings[0]
    return bindings[0].get(query_variable)

def end_of_list(list_id: str) -> bool:
    return list_id.endswith("nil")

client = WOQLClient("http://127.0.0.1:6363/")
client.connect()
try:
    client.create_database(db_name, team="admin")
    client.insert_document(schema_doc, graph_type="schema", full_replace=True)
    client.insert_document(instance_doc, graph_type="instance")
    for d in client.get_all_documents():
        print(d)
    bowl_id = query_and_return(client, "v:id", "rdf:type", "@schema:Bowl")
    list_id = query_and_return(client, bowl_id, "contains", "v:id")
    while not(end_of_list(list_id)):
        fruit = query_and_return(client, list_id, "rdf:first", "v:id")
        print(fruit)
        list_id = query_and_return(client, list_id, "rdf:rest", "v:id")
finally:
    print(f"Deleting database {db_name}")
    client.delete_database(dbid=db_name, team="admin")
    client.close()


