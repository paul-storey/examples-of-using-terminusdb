"""
client.update_document({ "@type": "CataloguePerson", "catalogue": "hebrew", "id": "716" } )
query = WOQLQuery()
query.add_triple("Person_9a4d8ad", "sameAs", "CataloguePerson_hebrew+572")

query.add_triple("Person_9a4d8ad", "sameAs", "CataloguePerson_hebrew+716")

client.query(query)



runquery(client, "v:var", "sameAs", "CataloguePerson_hebrew+572")
runquery(client, 'Person_9a4d8ad', 'sameAs', 'v:var')

runquery(client, 'v:var', 'sameAs', 'Person_9a4d8ad') 
"""
import code
from pprint import PrettyPrinter
from terminusdb_client import WOQLClient, WOQLQuery
from terminusdb_client.woqlschema import WOQLSchema
from typing import Dict, List, Tuple

db_name : str = "test_database"

schema_doc = [ 
    {   
        "@type"     : "@context",
        "@schema"   : "http://bodleian.ox.ac.uk#",
        "@base"     : "bodleian://famous/data/",
        "xsd"       : "http://www.w3.org/2001/XMLSchema#"
    },
    {
        "@id"           : "Person",
        "@type"         : "Class",
        "@base"         : "Person_",
        "name"          : "xsd:string",
        "ark"           : "xsd:string",
        "@key"      : 
            {
                "@type"     : "Lexical",
                "@fields"   : [ "ark" ]
            },
        "sameAs"      :
        {
            "@type"     : "Set",
            "@class"    : "CataloguePerson"
        }
   
    },
    {
        "@id"           : "CataloguePerson",
        "@type"         : "Class",
        "@base"         : "CataloguePerson_",
        "catalogue"     : "xsd:string",
        "id"            : "xsd:string",
        "sameAs"        :
        {
            "@type" : "Optional",
            "@class": "Person"
        },
        "@key"      : 
        {
            "@type"     : "Lexical",
            "@fields"   : [ "catalogue", "id" ]
        },   
    },
    {
        "@id"           : "Manuscript",
        "@type"         : "Class",
        "@base"         : "Manuscript_",
        "name"          : "xsd:string",
        "@key"          :
        {
            "@type"     : "Lexical",
            "@fields"   : [ "name" ]
        },
        "refersto"      :
        {
            "@type"     : "Set",
            "@class"    : "CataloguePerson"
        }
    }
    ]

instance_doc = [
    {
        "@type"   : "Person",
        "name"    : "Avicenna",
        "ark"     : "9a4d8ad"
    },
    {
        "@type"     : "CataloguePerson",
        "catalogue" : "medieval",
        "id"        : "89770781"
    },
    {
        "@type"     : "CataloguePerson",
        "catalogue" : "hebrew",
        "id"        : "572"
    },
    {
        "@type"     : "CataloguePerson",
        "catalogue" : "hebrew",
        "id"        : "716"
    }
    ]

def runquery(client, subject, predicate, obj) -> None:
    print(f"Query: {subject}, {predicate}, {obj}")
    query = WOQLQuery()\
        .triple(subject, predicate, obj)\
        .read_document("v:var", "v:Full Record")
    result = client.query(query)
    PrettyPrinter(indent=4).pprint(result)
    
#"ark"     : "ark:/99999/9a4d8ad",
client = WOQLClient("http://127.0.0.1:6363/")
client.connect()
try:
    client.create_database(db_name, team="admin")
    client.insert_document(schema_doc, graph_type="schema", full_replace=True, 
            commit_msg="Define schema")
    avicenna: Dict[str,str] = {"name": "Avicenna", "ark": "9a4d8ad"}
    avicenna_identities : List[Tuple[str,int]] = [ 
        ("hebrew",716),
        ("hebrew", 572),
        ("medieval", 89770781)]
    client.update_document([ \
        {"id": catid, "catalogue": catname, "@type": "CataloguePerson"} \
        for catname, catid in avicenna_identities])
    client.update_document(
        [{"name": avicenna["name"], "ark": avicenna["ark"], "@type": "Person"}]) 
    for catname, catid in avicenna_identities:
        query = WOQLQuery().add_triple(
            f"Person_{avicenna['ark']}", "sameAs", f"CataloguePerson_{catname}+{catid}"
            ).add_triple(
            f"CataloguePerson_{catname}+{catid}", "sameAs", f"Person_{avicenna['ark']}")
        client.query(query)
    for d in client.get_all_documents():
        print(d)
    variables = globals().copy()
    variables.update(locals())
    shell = code.InteractiveConsole(variables)
    shell.interact()
finally:
    print(f"Deleting database {db_name}")
    client.delete_database(dbid=db_name, team="admin")
    client.close()


