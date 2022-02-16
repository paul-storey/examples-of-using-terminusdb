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

