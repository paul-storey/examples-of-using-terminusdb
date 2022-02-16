from terminusdb_client import WOQLClient
from terminusdb_client.woqlschema import WOQLSchema

db_name : str = "test_database"

schema_doc = [ 
    {   
        "@type"     : "@context",
        "@schema"   : "http://bodleian.ox.ac.uk",
        "@base"     : "bodleian://famous/data/",
        "xsd"       : "http://www.w3.org/2001/XMLSchema#"
    },
    {
        "@id"           : "Manuscript",
        "@type"         : "Class",
        "@base"         : "Manuscript_",
        "name"          : "xsd:string",
        "temporal"      : "xsd:string",
        "material"      : "xsd:string",
        "creator"       : "Person",
        "sdPublisher"   : "Organization"
    },
    {
        "@id"       : "Person",
        "@type"     : "Class",
        "@base"     : "Person_",
        "familyName": "xsd:string",
        "givenName" : "xsd:string"
    },
    {
        "@id"       : "Organization",
        "@type"     : "Class",
        "@base"     : "Organization_",
        "@key"      : 
            {
                "@type"     : "Lexical",
                "@fields"   : [ "name" ]
            },
        "name"      : "xsd:string",
        "email"     : 
            {
                "@type" : "Optional",
                "@class": "xsd:string" 
            },
        "parentOrganization"    : 
            {
                "@type" : "Optional",
                "@class": "Organization"
            }
    }
    ]

instance_doc = [
        {
            "@type"   : "Manuscript",
            "name"    : "MS. Auct. T. 1. 10",
            "temporal": "16th centure (before 1573)",
            "material": "paper",
            "creator" : {
                "@type"     : "Person",
                "familyName": "Tzetzes",
                "givenName": "Johannes"
                },
            "sdPublisher"   : {
                "@type" : "Organization",
                "name"  : "Special Collections",
                "email" : "specialcollections.enquiries@bodleian.ox.ac.uk",
                "parentOrganization" : {
                    "@type" : "Organization",
                    "name"  : "University of Oxford"
                    }
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


