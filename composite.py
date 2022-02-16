from terminusdb_client import WOQLClient
from terminusdb_client.woqlschema import WOQLSchema

db_name : str = "test_database"

schema_doc = [ 
    {   
        "@type"     : "@context",
        "@schema"   : "http://bodleian.ox.ac.uk#",
        "@base"     : "bodleian://famous/data/",
        "xsd"       : "http://www.w3.org/2001/XMLSchema#"
    },
    {
        "@id"           : "Composite",
        "@type"         : "Class",
        "name"          : "xsd:string",
        "ark"           : "xsd:string",
        "@key"          :
        {
            "@type"     : "Lexical",
            "@fields"   : [ "ark" ]
        },
        "components"    :
        {
            "@type"     : "Optional",
            "@class"    : "Components"
        }
    },
    {
        "@id"           : "Components",
        "@type"         : "Class",
        "members"       :
        {
            "@type"     : "List",
            "@class"    : "Composite"
        }
    }
    ]

instance_doc = [
        {
            "@type"     : "Composite",
            "name"      : "A",
            "ark"       : "ark:/12345/A",
            "components": 
            {
                "@type" : "Components",
                "members": 
                [
                    {
                        "@type"     : "Composite",
                        "name"      : "B",
                        "ark"       : "ark:/12345/B",
                        "components":
                        {
                            "@type" : "Components",
                            "members": 
                            [
                                {
                                    "@type" : "Composite",
                                    "name"  : "C",
                                    "ark"   : "ark:/12345/C"
                                }
                            ]
                        }
                    }
                ]
            }
        }
        ]

client = WOQLClient("http://127.0.0.1:6363/")
client.connect()
try:
    client.create_database(db_name, team="admin")
    client.insert_document(schema_doc, graph_type="schema", full_replace=True, 
            commit_msg="Define schema")
    client.insert_document(instance_doc, graph_type="instance", commit_msg="Add instance data")
    for d in client.get_all_documents():
        print(d)
finally:
    client.delete_database(dbid=db_name, team="admin")
    client.close()


