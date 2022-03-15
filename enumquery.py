from pprint import PrettyPrinter

from terminusdb_client import WOQLClient, WOQLQuery
from terminusdb_client.woqlschema import WOQLSchema


db_name : str = "test_database"

schema_doc = [ 
    {   
        "@type"     : "@context",
        "@schema"   : "http://xyz#",
        "@base"     : "someorg://base/path/",
        "xsd"       : "http://www.w3.org/2001/XMLSchema#"
    },
    {
        "@type": "Enum",
        "@id": "TextLang",
        "@value": [ "en", "fr", "it", "la" ],
    },
    {
        "@id": "Comment",
        "@type": "Class",
        "@base": "Comment_",
        "title": "xsd:string",
        "@key": {
            "@type": "Lexical",
            "@fields": ["title"],
            },
        "text": "xsd:string",
        "lang": {
                "@type": "Set",
                "@class": "TextLang",
        },
    },
    ]

instance_doc = [
    {
        "@type": "Comment",
        "title": "title",
        "text": "some text",
        "lang": [ "en", "fr" ],
    },
    ]

def runquery(client, subject, predicate, obj) -> None:
    print(f"Query: {subject}, {predicate}, {obj}")
    query = WOQLQuery().triple(subject, predicate, obj)
    result = client.query(query)
    PrettyPrinter(indent=4).pprint(result)
 
client = WOQLClient("http://127.0.0.1:6363/")
client.connect()
try:
    client.create_database(db_name, team="admin")
    client.insert_document(schema_doc, graph_type="schema", full_replace=True, 
            commit_msg="Define schema")
    client.insert_document(instance_doc, graph_type="instance")
    for d in client.get_all_documents():
        print(d)
    runquery(client, "v:subj", "lang", "v:obj")
    runquery(client, "v:subj", "lang", "fr")
    runquery(client, "v:subj", "lang", "http://xyz#TextLang/fr")
    runquery(client, "v:subj", "lang", "@schema:TextLang/fr")
finally:
    print(f"Deleting database {db_name}")
    client.delete_database(dbid=db_name, team="admin")
    client.close()

