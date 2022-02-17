## Examples of using TerminusDB

### define_a_schema_and_add_a_doc.py
Defines a Manuscript with a creator that is a Person and a `sdPublisher` that is 
an Organisation.
Definition of these classes follows their definition in schema.org

### composite.py 
A Composite has an `ark` property and contains zero or more Composites. 
```
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
        "contains"      :
        {
            "@type"     : "Set",
            "@class"    : "Composite"
        }
    }
```
In composite.py, A contains B which contains C.
```
python composite.py 
{'@id': 'Composite/A', '@type': 'Composite', 'ark': 'A', 'contains': ['Composite/B'], 'name': 'A'}
{'@id': 'Composite/B', '@type': 'Composite', 'ark': 'B', 'contains': ['Composite/C'], 'name': 'B'}
{'@id': 'Composite/C', '@type': 'Composite', 'ark': 'C', 'name': 'C'}
```

### When a subdocument with the same ID occurs multiple times
Some aspects of the behaviour of terminusdb are illustrated by `when_the_subdoc_already_exists.py`
`B` is added twice, but is only listed as occurring once:
```
{'@id': 'Composite/A', '@type': 'Composite', 'ark': 'A', 'contains': ['Composite/B'], 'name': 'A'}
{'@id': 'Composite/B', '@type': 'Composite', 'ark': 'B', 'contains': ['Composite/C'], 'name': 'B'}
{'@id': 'Composite/C', '@type': 'Composite', 'ark': 'C', 'name': 'C'}
{'@id': 'Composite/D', '@type': 'Composite', 'ark': 'D', 'contains': ['Composite/B'], 'name': 'D'}
```
However, if the second occurrence of `B` differs from the first for one of other, non-identifying
properties (for example, changing the `name` of the second `B` to `b`, then an exception is raised:
```
terminusdb_client.errors.DatabaseError: Schema check failure
{
    "@type": "api:ReplaceDocumentErrorResponse",
    "api:error": {
        "@type": "api:SchemaCheckFailure",
        "api:witnesses": [
            {
                "@type": "instance_not_cardinality_one",
                "class": "http://www.w3.org/2001/XMLSchema#string",
                "instance": "bodleian://famous/data/Composite/B",
                "predicate": "http://bodleian.ox.ac.uk#name"
            }
        ]
    },
    "api:message": "Schema check failure",
    "api:status": "api:failure"
}
```
### Trivial WOQL query
`trivial_woql_query.py` is a trivial example of using the Web Object Query Language (WOQL).
I'm struggling to find good resources on using WOQL. 
There is [this blog](https://terminusdb.com/blog/the-power-of-web-object-query-language/)
and there is a [single page tutorial](https://terminusdb.com/docs/index/terminusx-db/how-to-guides/perform-graph-queries)
The query is constructed as follows
```
query = WOQLQuery()\
        .triple("v:Subject", "name", {"@type": "xsd:string", "@value": "B"})\
        .read_document("v:Subject", "v:Full Record")
```
Notes:
- use of `v: Full Record` is inspired by the aforementioned blog. I am not aware it is otherwise documented.
- Using the simpler `triple("v:Subject", "name", "B")` would have been nice but didn't work for me.

This query returns:
```
{   '@type': 'api:WoqlResponse',
    'api:status': 'api:success',
    'api:variable_names': ['Subject', 'Full Record'],
    'bindings': [   {   'Full Record': {   '@id': 'Composite/B',
                                           '@type': 'Composite',
                                           'ark': 'B',
                                           'contains': ['Composite/C'],
                                           'name': 'B'},
                        'Subject': 'Composite/B'}],
    'deletes': 0,
    'inserts': 0,
    'transaction_retry_count': 0
}
```


### Notes

This is how terminusdb states the basic unit of specification:
```
{ 
    "@type" : "Class",
    "@id"   : "Person",
    "name"  : "xsd:string" 
}
```

There's also the Context object, e.g.
```
{   "@type"            : "@context",
    "@schema"          : "http://terminusdb.com/schema/woql#",
    "@base"            : "terminusdb://woql/data/",
    "xsd"              : "http://www.w3.org/2001/XMLSchema#",
    "@documentation"   :
    {
        "@title"       : "WOQL schema",
        "@authors"     : ["Gavin Mendel-Gleason"],
        "@description" : "The WOQL schema providing a complete specification of the WOQL syntax.
                         This enables:
                         * WOQL queries to be checked for syntactic correctness.
                         * Storage and retrieval of queries.
                         * Queries to be associated with data products.
                         * Helps to prevent errors and detect conflicts in merge of queries.",
    }
}
```
`@schema` specifies the default URI expansion

For real, could be:
```
{   "@type"            : "@context",
    "@schema"          : "http://schema.org",
    "@base"            : "bodleian://data/"
}
```

Example of a manuscript description in JSON-LD:
```
{
  "@context": "https://schema.org",
  "@type": "Manuscript",
  "sdPublisher": {
    "name": "Special Collections",
    "email": "specialcollections.enquiries@bodleian.ox.ac.uk",
    "parentOrganization": {
      "name": "Bodleian Libraries",
      "parentOrganization": {
        "name": "University of Oxford"
      }
    }
  },
  "sdDatePublished": "2022-02-15",
  "material": "paper",
  "inLanguage": "Grek",
  "creator": {
    "familyName": "Tzetzes",
    "givenName": "Johannes"
  },
  "temporal": "16th centure (before 1573)",
  "description": "MS. Auct. T. 1. 10",
  "identifier": {
    "propertyID": "shelfmark",
    "value": "MS. Auct. T. 1. 10"
  },
  "name": "MS. Auct. T. 1. 10"
}
```

The above JSON-LD has been validated using the [JSON-LD Playground](https://json-ld.org/playground/)

