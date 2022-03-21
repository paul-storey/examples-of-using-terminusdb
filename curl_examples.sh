#!/bin/bash
# Examples of using curl to interact with TerminusDB

# Create a database
curl --user admin:root --header "content-type: application/json" --data '{"label": "A label", "comment": "a comment"}' http://127.0.0.1:6363/api/db/admin/db_test


# Upload a schema
 cat person_schema.json | \
    curl --user admin:root -X POST \
    'http://localhost:6363/api/document/admin/db_test?graph_type=schema&author=me&message=createschema&full_replace=true' \
    --data-binary @- -H 'Content-Type: application/json'

# Get the schema
 curl --user admin:root http://localhost:6363/api/document/admin/db_test?graph_type=schema

# Put a Person
curl --user admin:root \
    -X PUT \
    --data '{ "@type": "Person", "id":"123", "names":["Bob", "Jim"] }' \
    --header 'Content-Type: application/json' \
    'http://localhost:6363/api/document/admin/db_test?author=paul&message=message&create=true'

# Get all documents
curl --user admin:root http://localhost:6363/api/document/admin/db_test?graph_type=instance

# WOQLQuery for Persons with 'Jim' among their names
curl --user admin:root \
    --header 'Content-Type: application/json' \
    --data '{"query": {"@type": "Triple", "object": {"@type": "Value", "data": {"@type": "xsd:string", "@value": "Jim"}}, "predicate": {"@type": "NodeValue", "node": "names"}, "subject": {"@type": "NodeValue", "variable": "subj"}}}' \
    http://localhost:6363/api/woql//admin/db_test

# Document query for Persons with 'Jim' among their names,
# based on documentation at
# https://terminusdb.com/docs/index/terminusx-db/reference-guides/document-interface
curl --user admin:root \
    --header 'Content-Type: application/json' \
    --header 'X-HTTP-Method-Override: GET' \
    -X POST \
    --data '{ "query": { "@type": "Person", "id": "123" } }' \
    http://localhost:6363/api/document/admin/db_test

# Delete a database
curl --user admin:root -X DELETE http://127.0.0.1:6363/api/db/admin/db_test

# Get the system graph
curl --user admin:root  http://127.0.0.1:6363/api/document/_system
