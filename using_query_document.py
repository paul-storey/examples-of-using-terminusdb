from terminusdb_client import WOQLClient, WOQLQuery
from pprint import PrettyPrinter
from terminusdb_client.woqlschema import WOQLSchema

db_name: str = "test_database"

schema_doc = [
    {
        "@type": "@context",
        "@schema": "http://bodleian.ox.ac.uk#",
        "@base": "bodleian://famous/data/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    },
    {
        "@id": "Composite",
        "@type": "Class",
        "name": "xsd:string",
        "ark": "xsd:string",
        "@key":
            {
                "@type": "Lexical",
                "@fields": ["ark"]
            },
        "contains":
            {
                "@type": "Set",
                "@class": "Composite"
            }
    }
]

A_contains_B_contains_C = [
    {
        "@type": "Composite",
        "name": "A",
        "ark": "A",
        "contains":
            [
                {
                    "@type": "Composite",
                    "name": "B",
                    "ark": "B",
                    "contains":
                        [
                            {
                                "@type": "Composite",
                                "name": "C",
                                "ark": "C"
                            }
                        ]
                }
            ]
    }
]

client = WOQLClient("http://127.0.0.1:6363/")
client.connect()
try:
    client.create_database(db_name, team="admin")
    client.insert_document(schema_doc, graph_type="schema", full_replace=True,
                           commit_msg="Define schema")
    client.update_document(A_contains_B_contains_C, graph_type="instance", commit_msg="A contains B contains C")
    documents = client.query_document({'@type': 'Composite', 'name': 'B'})
    pp = PrettyPrinter(indent=4)
    for doc in documents:
        pp.pprint(doc)
finally:
    client.delete_database(dbid=db_name, team="admin")
    client.close()
