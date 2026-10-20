# MERGE - Cypher Manual

Source: https://neo4j.com/docs/cypher-manual/current/clauses/merge/
Fetched: 2026-05-07T05:05:37.110095+00:00

MERGE - Cypher Manual

Docs

Docs

Neo4j DBMS
- Getting Started

- Operations

- Migration and Upgrade

- Status Codes

- Java Reference

- Kerberos Add-on

Neo4j Aura

Neo4j Tools
- Neo4j Bloom

- Neo4j Browser

- Neo4j Data Importer

- Neo4j Desktop

- Neo4j Ops Manager

- Neodash commercial

Neo4j Graph Data Science
- Neo4j Graph Data Science Library

- Neo4j Graph Data Science Client

- Neo4j Graph Analytics for Snowflake

Cypher Query Language
- Cypher

- Cypher Cheat Sheet

- APOC Library

Generative AI
- Neo4j GraphRAG for Python

- Embeddings and vector indexes tutorial

- GenAI plugin

- Vector search indexes

- Vector search functions

- GraphQL vector index search documentation

Create applications
- Python Driver

- Go Driver

- Java Driver

- JDBC Driver

- JavaScript Driver

- .Net Driver

- Neo4j GraphQL Library

- Neo4j Visualization Library

- OGM Library

- Spring Data Neo4j

- HTTP API

- Neo4j Query API

- Bolt

Connect data sources
- Neo4j Connector for Apache Spark

- Neo4j Connector for Apache Kafka

- Change Data Capture (CDC)

- BigQuery to Neo4j

- Google Cloud to Neo4j

Labs

GenAI Ecosystem
- LLM Knowledge Graph Builder

- Vector Index & Search

- LangChain

- LangChain.js

- LlamaIndex

- Haystack

- DSPy

Developer Tools
- APOC Extended

- Aura CLI

- arrows.app

- Cypher Workbench

- ETL Tool

- NeoDash

Frameworks & Integrations
- Needle Starter Kit

- Neo4j Plugin for Liquibase

- Neo4j Migrations

- neomodel

RDF & Linked Data
- Neosemantics (Java)

- RDFLib-Neo4j (Python)

Get Help

Community Forum

Discord Chat

Product Support

Neo4j Developer Blog

Neo4j Videos

GraphAcademy

Beginners Courses
- Neo4j Fundamentals

- Cypher Fundamentals

- Importing Data Fundamentals

- Importing CSV Data

- Graph Data Modeling

Data Scientist Courses
- Get started with Graph Data Science

- Path Finding

Generative AI Courses
- Neo4j & Generative AI Fundamentals

- Vector Indexes & Unstructured Data

- Constructing Knowledge Graphs

- Building Agents in Neo4j Aura

Neo4j Certification
- Neo4j Certified Professional

- Neo4j Graph Data Science Certification

Get Started Free

Theme

Light

Dark

Search

Skip to content

Cypher Manual

Product Version Version 25 Version 5 Version 4.4

-
- Introduction
- Overview

- Cypher and Neo4j

- Cypher and Aura

- Queries
- Core concepts

- Basic queries

- Select Cypher version

- Composed queries
- Combined queries ( UNION
)

- Conditional queries ( WHEN
)

- Sequential queries ( NEXT
)

- Clauses
- Clause composition

- CALL procedure

- CREATE

- DELETE

- FILTER

- FINISH

- FOR

- FOREACH

- LET

- LIMIT

- LOAD CSV

- MATCH

- MERGE

- OPTIONAL MATCH

- ORDER BY

- REMOVE

- RETURN

- SEARCH

- SET

- SHOW FUNCTIONS

- SHOW PROCEDURES

- SHOW SETTINGS

- SHOW TRANSACTIONS

- SKIP

- TERMINATE TRANSACTIONS

- UNWIND

- USE

- WHERE

- WITH

- Subqueries
- CALL subqueries

- CALL subqueries in transactions

- COLLECT subqueries

- COUNT subqueries

- EXISTS subqueries

- Patterns
- Primer

- Fixed-length paths

- Variable-length paths

- Non-linear paths

- Shortest paths

- Paths with unique relationships

- Paths with repeated nodes and relationships

- Acyclic paths

- Syntax and semantics

- Values and types
- Property, structural, and constructed values

- Boolean, numeric, and string literals

- Temporal values

- Spatial values

- Lists

- Maps

- Vectors

- Graph references

- Working with null

- Casting data values

- Equality, ordering, and comparison of value types

- Expressions
- Predicates
- Boolean operators

- Comparison operators

- List operators

- String operators

- Label expression predicates

- Path pattern expressions

- Type predicate expressions

- Node and relationship operators

- Mathematical operators

- String concatenation operators

- Temporal operators

- List expressions

- Map expressions

- Conditional expressions (CASE)

- Functions
- Aggregating functions

- Database functions

- Graph functions

- List functions

- LOAD CSV functions

- Mathematical functions
- Logarithmic functions

- Numeric functions

- Trigonometric functions

- Predicate functions

- Scalar functions

- Spatial functions

- String functions

- Temporal functions
- Duration functions

- Instant type functions

- Format functions

- User-defined functions

- Vector functions

- Indexes
- Search-performance indexes
- Create indexes

- Show indexes

- Drop indexes

- The impact of indexes on query performance

- Index hints for the Cypher planner

- Semantic indexes
- Full-text indexes

- Vector indexes

- Syntax

- Schema
- Graph types (Preview feature)
- Set graph types

- Extend graph types

- Alter element types

- Show graph types

- Drop graph type elements

- Constraints
- Create constraints

- Show constraints

- Drop constraints

- Syntax

- Execution plans and query tuning
- Understanding execution plans

- Operators
- Operators in detail

- Cypher runtimes
- Concepts

- Parallel runtime: reference

- Query tuning

- Query caches
- Unifying query caches

- Administration

- Syntax
- Parsing

- Naming rules and recommendations

- Variables

- Keywords

- Parameters

- Comments

- Additions, deprecations, removals, and compatibility

- Appendix
- Cypher styleguide

- GQL conformance
- Supported mandatory GQL features

- Currently unsupported mandatory GQL features

- Supported optional GQL features

- Optional GQL features and analogous Cypher

- Additional Cypher features

- Tutorials and extended examples
- Basic query tuning example

- Advanced query tuning example

Is this page helpful?

- Cypher Manual

- Clauses

- MERGE

Raise an issue

# MERGE

## Introduction

The MERGE
clause either matches existing node patterns in the graph and binds them or, if not present, creates new data and binds that. In this way, it acts as a combination of MATCH
and CREATE
that allows for specific actions depending on whether the specified data was matched or created.

For example, MERGE
can be used to specify that a graph must contain a node with a Person
label and a specific name
property. If there isn’t a node with the specific name
property, a new node will be created with that name
property.

For performance reasons, creating a schema index on the label or property is highly recommended when using MERGE
. See Create indexes for more information.

When using MERGE
on full patterns, the behavior is that either the whole pattern matches, or the whole pattern is created. MERGE
will not partially use existing patterns. If partial matches are needed, this can be accomplished by splitting a pattern into multiple MERGE
clauses.

Under concurrent updates, MERGE
only guarantees the existence of the MERGE
pattern, but not uniqueness. To guarantee uniqueness of nodes with certain properties, a property uniqueness constraint should be used. See Using property uniqueness constraints with MERGE
.

Similar to MATCH
, MERGE
can match multiple occurrences of a pattern. If there are multiple matches, they will all be passed on to later stages of the query.

The last part of a MERGE
clause is the ON CREATE
and/or ON MATCH
operators. These allow a query to express additional changes to the properties of a node or relationship, depending on whether the element was matched ( MATCH
) in the database or if it was created ( CREATE
).

## Example graph

The following graph is used for the examples below:

To recreate the graph, run the following query in an empty Neo4j database:

CREATE (charlie:Person {name: 'Charlie Sheen', bornIn: 'New York', chauffeurName: 'John Brown'}), (martin:Person {name: 'Martin Sheen', bornIn: 'Ohio', chauffeurName: 'Bob Brown'}), (michael:Person {name: 'Michael Douglas', bornIn: 'New Jersey', chauffeurName: 'John Brown'}), (oliver:Person {name: 'Oliver Stone', bornIn: 'New York', chauffeurName: 'Bill White'}), (rob:Person {name: 'Rob Reiner', bornIn: 'New York', chauffeurName: 'Ted Green'}), (wallStreet:Movie {title: 'Wall Street'}), (theAmericanPresident:Movie {title: 'The American President'}), (charlie)-[:ACTED_IN]->(wallStreet), (martin)-[:ACTED_IN]->(wallStreet), (michael)-[:ACTED_IN]->(wallStreet), (martin)-[:ACTED_IN]->(theAmericanPresident), (michael)-[:ACTED_IN]->(theAmericanPresident), (oliver)-[:DIRECTED]->(wallStreet), (rob)-[:DIRECTED]->(theAmericanPresident)

## Merge nodes

### Merge single node with a label

Merge a node with a specific label:

Query

MERGE (robert:Critic) RETURN labels(robert)

A new node is created because there are no nodes labeled Critic
in the database:

Result
labels(robert)

["Critic"]

### Merge single node with multiple labels

Multiple labels are separated by colons:

Query

MERGE (robert:Critic:Viewer) RETURN labels(robert)

A new node is created because there are no nodes labeled both Critic
and Viewer
in the database:

Result
labels(robert)

["Critic","Viewer"]

Multiple labels can also be separated by an ampersand &
, in the same manner as it is used in label expressions . Separation by colon :
and ampersand &
cannot be mixed in the same clause.

Query

MERGE (robert:Critic&Viewer) RETURN labels(robert)

No new node is created because there was already a node labeled both Critic
and Viewer
in the database:

Result
labels(robert)

["Critic","Viewer"]

### Merge single node with properties

Merging a node with properties that differ from the properties on existing nodes in the graph will create a new node:

Query

MERGE (charlie {name: 'Charlie Sheen', age: 10}) RETURN charlie

A new node with the name Charlie Sheen
is created since not all properties matched those set to the pre-existing Charlie Sheen
node:

Result
charlie

(:Person {"name":"Charlie Sheen", "age":10})

MERGE
cannot be used for nodes with property values that are null
. For example, the following query will throw an error:

Query

MERGE (martin:Person {name: 'Martin Sheen', age: null}) RETURN martin

GQLSTATUS error chain

22N31 : error: data exception - invalid properties in merge pattern. The node property age
in '(:Person {age: null})' is invalid. 'MERGE' cannot be used with a graph element property value that is null.

22G03 : error: data exception - invalid value type

### Merge single node specifying both label and property

Merging a single node with both label and property matching an existing node will not create a new node:

Query

MERGE (michael:Person {name: 'Michael Douglas'}) RETURN michael.name, michael.bornIn

Michael Douglas
is matched and the name
and bornIn
properties are returned:

Result
michael.name
michael.bornIn

"Michael Douglas"

"New Jersey"

### Merge single node derived from an existing node property

It is possible to merge nodes using existing node properties:

Query

MATCH (person:Person) MERGE (location:Location {name: person.bornIn}) RETURN person.name, person.bornIn, location

In the above query, three nodes labeled Location
are created, each of which contains a name
property with the value of New York
, Ohio
, and New Jersey
respectively. Note that even though the MATCH
clause results in three bound nodes having the value New York
for the bornIn
property, only a single New York
node (i.e. a Location
node with a name of New York
) is created. As the New York
node is not matched for the first bound node, it is created. However, the newly-created New York
node is matched and bound for the second and third bound nodes.

Result
person.name
person.bornIn
location

"Charlie Sheen"

"New York"

{name:"New York"}

"Martin Sheen"

"Ohio"

{name:"Ohio"}

"Michael Douglas"

"New Jersey"

{name:"New Jersey"}

"Oliver Stone"

"New York"

{name:"New York"}

"Rob Reiner"

"New York"

{name:"New York"}

## Use ON CREATE
and ON MATCH

### Merge with ON CREATE

Merge a node and set properties if the node needs to be created:

Query

MERGE (keanu:Person {name: 'Keanu Reeves', bornIn: 'Beirut', chauffeurName: 'Eric Brown'}) ON CREATE SET keanu.created = timestamp() RETURN keanu.name, keanu.created

The query creates the Person
node named Keanu Reeves
, with a bornIn
property set to Beirut
and a chauffeurName
property set to Eric Brown
. It also sets a timestamp for the created
property.

Result
keanu.name
keanu.created

"Keanu Reeves"

1655200898563

### Merge with ON MATCH

Merging nodes and setting properties on found nodes:

Query

MERGE (person:Person) ON MATCH SET person.found = true RETURN person.name, person.found

The query finds all the Person
nodes, sets a property on them, and returns them:

Result
person.name
person.found

"Charlie Sheen"

true

"Martin Sheen"

true

"Michael Douglas"

true

"Oliver Stone"

true

"Rob Reiner"

true

"Keanu Reeves"

true

### Merge with ON CREATE
and ON MATCH

Query

MERGE (keanu:Person {name: 'Keanu Reeves'}) ON CREATE SET keanu.created = timestamp() ON MATCH SET keanu.lastSeen = timestamp() RETURN keanu.name, keanu.created, keanu.lastSeen

Because the Person
node named Keanu Reeves
already exists, this query does not create a new node. Instead, it adds a timestamp on the lastSeen
property.

Result
keanu.name
keanu.created
keanu.lastSeen

"Keanu Reeves"

1655200902354

1674655352124

### Merge with ON MATCH
setting multiple properties

If multiple properties should be set, separate them with commas:

Query

MERGE (person:Person) ON MATCH SET person.found = true, person.lastAccessed = timestamp() RETURN person.name, person.found, person.lastAccessed

Result
person.name
person.found
person.lastAccessed

"Charlie Sheen"

true

1655200903558

"Martin Sheen"

true

1655200903558

"Michael Douglas"

true

1655200903558

"Oliver Stone"

true

1655200903558

"Rob Reiner"

true

1655200903558

"Keanu Reeves"

true

1655200903558

## Merge relationships

### Merge on a relationship

MERGE
can be used to match or create a relationship:

Query

MATCH (charlie:Person {name: 'Charlie Sheen'}), (wallStreet:Movie {title: 'Wall Street'}) MERGE (charlie)-[r:ACTED_IN]->(wallStreet) RETURN charlie.name, type(r), wallStreet.title

Charlie Sheen
had already been marked as acting in Wall Street
, so the existing relationship is found and returned. Note that in order to match or create a relationship when using MERGE
, at least one bound node must be specified, which is done via the MATCH
clause in the above example.

Result
charlie.name
type(r)
wallStreet.title

"Charlie Sheen"

"ACTED_IN"

"Wall Street"

MERGE
cannot be used for relationships with property values that are null
. For example, the following query will throw an error:

Query

MERGE (martin:Person {name: 'Martin Sheen'})-[r:FATHER_OF {since: null}]->(charlie:Person {name: 'Charlie Sheen'}) RETURN type(r)

GQLSTATUS error chain

22N31 : error: data exception - invalid properties in merge pattern. The relationship property since
in '(martin)-[:FATHER_OF {since: null}]→(charlie)' is invalid. 'MERGE' cannot be used with a graph element property value that is null.

22G03 : error: data exception - invalid value type

Specifying a property of an entity (node or relationship) by referring to the property of another entity within the same MERGE
clause is not allowed.

For example, referring to charlie.bornIn
in the property definition of oliver.bornIn
is not allowed.

Query

MERGE (charlie:Person {name: 'Charlie Sheen', bornIn: 'New York'})-[:ACTED_IN]->(movie:Movie)<-[:DIRECTED]-(oliver:Person {name: 'Oliver Stone', bornIn: charlie.bornIn}) RETURN movie

GQLSTATUS error chain

42I58 : error: syntax error or access rule violation - invalid entity reference. Entity, 'charlie', cannot be created and referenced in the same clause.

42001 : error: syntax error or access rule violation - invalid syntax

### Merge on multiple relationships

Query

MATCH (oliver:Person {name: 'Oliver Stone'}), (reiner:Person {name: 'Rob Reiner'}) MERGE (oliver)-[:DIRECTED]->(movie:Movie)<-[:DIRECTED]-(reiner) RETURN movie

In the example graph, Oliver Stone
and Rob Reiner
have never worked together. When trying to MERGE
a Movie
node between them, Neo4j will not use any of the existing Movie
nodes already connected to either person. Instead, a new Movie
node is created.

Result
movie

(:Movie)

### Merge on an undirected relationship

MERGE
can also be used without specifying the direction of a relationship. Cypher® will first try to match the relationship in both directions. If the relationship does not exist in either direction, it will create one left to right.

Query

MATCH (charlie:Person {name: 'Charlie Sheen'}), (oliver:Person {name: 'Oliver Stone'}) MERGE (charlie)-[r:KNOWS]-(oliver) RETURN r

As Charlie Sheen
and Oliver Stone
do not know each other in the example graph, this MERGE
query will create a KNOWS
relationship between them. The direction of the created relationship is left to right.

Result
r

[:KNOWS]

### Merge on a relationship between two existing nodes

MERGE
can be used in conjunction with preceding MATCH
and MERGE
clauses to create a relationship between two bound nodes m
and n
, where m
is returned by MATCH
and n
is created or matched by the earlier MERGE
.

Query

MATCH (person:Person) MERGE (location:Location {name: person.bornIn}) MERGE (person)-[r:BORN_IN]->(location) RETURN person.name, person.bornIn, location

This builds on the example from Merge single node derived from an existing node property . The second MERGE
creates a BORN_IN
relationship between each person and a location corresponding to the value of the personâs bornIn
property. Charlie Sheen
, Rob Reiner
, and Oliver Stone
all have a BORN_IN
relationship to the same Location
node ( New York
).

Result
person.name
person.bornIn
location

"Charlie Sheen"

"New York"

(:Location {name:"New York"})

"Martin Sheen"

"Ohio"

(:Location {name:"Ohio"})

"Michael Douglas"

"New Jersey"

(:Location {name:"New Jersey"})

"Oliver Stone"

"New York"

(:Location {name:"New York"})

"Rob Reiner"

"New York"

(:Location {name:"New York"})

"Keanu Reeves"

"Beirut"

(:Location {name:"Beirut"})

### Merge on a relationship between an existing node and a merged node derived from a node property

MERGE
can be used to simultaneously create both a new node n
and a relationship between a bound node m
and n
:

Query

MATCH (person:Person) MERGE (person)-[r:HAS_CHAUFFEUR]->(chauffeur:Chauffeur {name: person.chauffeurName}) RETURN person.name, person.chauffeurName, chauffeur

As MERGE
found no matches — in the example graph, there are no nodes labeled with Chauffeur
and no HAS_CHAUFFEUR
relationships — MERGE
creates six nodes labeled with Chauffeur
, each of which contains a name
property whose value corresponds to each matched Person
node’s chauffeurName
property value. MERGE
also creates a HAS_CHAUFFEUR
relationship between each Person
node and the newly-created corresponding Chauffeur
node. As 'Charlie Sheen'
and 'Michael Douglas'
both have a chauffeur with the same name — 'John Brown'
— a new node is created in each case, resulting in two Chauffeur
nodes having a name
of 'John Brown'
, correctly denoting the fact that even though the name
property may be identical, these are two separate people. This is in contrast to the example shown above in Merge on a relationship between two existing nodes , where the first MERGE
was used to bind the Location
nodes and to prevent them from being recreated (and thus duplicated) on the second MERGE
.

Result
person.name
person.chauffeurName
chauffeur

"Charlie Sheen"

"John Brown"

(:Person {name:"John Brown"})

"Martin Sheen"

"Bob Brown"

(:Person {name:"Bob Brown"})

"Michael Douglas"

"John Brown"

(:Person {name:"John Brown"})

"Oliver Stone"

"Bill White"

(:Person {name:"Bill White"})

"Rob Reiner"

"Ted Green"

(:Person {name:"Ted Green"})

"Keanu Reeves"

"Eric Brown"

(:Person {name:"Eric Brown"})

## Using node property uniqueness constraints with MERGE

Cypher prevents getting conflicting results from MERGE
when using patterns that involve property uniqueness constraints . In this case, there must be at most one node that matches that pattern.

For example, given two property node uniqueness constraints on :Person(id)
and :Person(ssn)
, a query such as MERGE (n:Person {id: 12, ssn: 437})
will fail, if there are two different nodes (one with id
12 and one with ssn
437), or if there is only one node with only one of the properties. In other words, there must be exactly one node that matches the pattern, or no matching nodes.

Note that the following examples assume the existence of property uniqueness constraints that have been created using:

CREATE CONSTRAINT FOR (n:Person) REQUIRE n.name IS UNIQUE; CREATE CONSTRAINT FOR (n:Person) REQUIRE n.role IS UNIQUE;

### Merge node using property uniqueness constraints creates a new node if no node is found

Given the node property uniqueness constraint on the name
property for all Person
nodes, the below query will create a new Person
with the name
property Laurence Fishburne
. If a Laurence Fishburne
node had already existed, MERGE
would match the existing node instead.

Query

MERGE (laurence:Person {name: 'Laurence Fishburne'}) RETURN laurence.name

Result
laurence.name

"Laurence Fishburne"

### Merge using node property uniqueness constraints matches an existing node

Given property uniqueness constraint on the name
property for all Person
nodes, the below query will match the pre-existing Person
node with the name
property Oliver Stone
.

Query

MERGE (oliver:Person {name: 'Oliver Stone'}) RETURN oliver.name, oliver.bornIn

Result
oliver.name
oliver.bornIn

"Oliver Stone"

"New York"

### Merge with property uniqueness constraints and partial matches

Merge using property uniqueness constraints fails when finding partial matches:

Query

MERGE (michael:Person {name: 'Michael Douglas', role: 'Gordon Gekko'}) RETURN michael

While there is a matching unique Person
node with the name Michael Douglas
, there is no unique node with the role of Gordon Gekko
and MERGE
, therefore, fails to match.

GQLSTATUS error chain

22N41 : error: data exception - merge node uniqueness constraint violation. The 'MERGE' clause did not find a matching node michael
and cannot create a new node due to conflicts with existing uniqueness constraints.

22G03 : error: data exception - invalid value type

To set the role
of Gordon Gekko
to Michael Douglas
, use the SET
clause instead:

Query

MERGE (michael:Person {name: 'Michael Douglas'}) SET michael.role = 'Gordon Gekko'

Result

Set 1 property

### Merge with property uniqueness constraints and conflicting matches

Merge using property uniqueness constraints fails when finding conflicting matches:

Query

MERGE (oliver:Person {name: 'Oliver Stone', role: 'Gordon Gekko'}) RETURN oliver

While there is a matching unique Person
node with the name Oliver Stone
, there is also another unique Person
node with the role of Gordon Gekko
and MERGE
fails to match.

GQLSTATUS error chain

22N41 : error: data exception - merge node uniqueness constraint violation. The 'MERGE' clause did not find a matching node oliver
and cannot create a new node due to conflicts with existing uniqueness constraints.

22G03 : error: data exception - invalid value type

## Using relationship property uniqueness constraints with MERGE

All that has been said above about node uniqueness constraints also applies to relationship uniqueness constraints. However, for relationship uniqueness constraints there are some additional things to consider.

For example, if there exists a relationship uniqueness constraint on ()-[:ACTED_IN(year)]-()
, then the following query, in which not all nodes of the pattern are bound, would fail:

Query

MERGE (charlie:Person {name: 'Charlie Sheen'})-[r:ACTED_IN {year: 1987}]->(wallStreet:Movie {title: 'Wall Street'}) RETURN charlie.name, type(r), wallStreet.title

This is due to the all-or-nothing semantics of MERGE
, which causes the query to fail if there exists a relationship with the given year
property but there is no match for the full pattern. In this example, since no match was found for the pattern, MERGE
will try to create the full pattern including a relationship with {year: 1987}
, which will lead to constraint violation error.

Therefore, it is advised - especially when relationship uniqueness constraints exist - to always use bound nodes in the MERGE
pattern. The following would, therefore, be a more appropriate composition of the query:

Query

MATCH (charlie:Person {name: 'Charlie Sheen'}), (wallStreet:Movie {title: 'Wall Street'}) MERGE (charlie)-[r:ACTED_IN {year: 1987}]->(wallStreet) RETURN charlie.name, type(r), wallStreet.title

### Using map parameters with MERGE

MERGE
does not support map parameters the same way that CREATE
does. To use map parameters with MERGE
, it is necessary to explicitly use the expected properties, such as in the following example. For more information on parameters, see Parameters .

Parameters

{ "param": { "name": "Keanu Reeves", "bornIn": "Beirut", "chauffeurName": "Eric Brown" } }

Query

MERGE (person:Person {name: $param.name, bornIn: $param.bornIn, chauffeurName: $param.chauffeurName}) RETURN person.name, person.bornIn, person.chauffeurName

Result
person.name
person.bornIn
person.chauffeurName

"Keanu Reeves"

"Beirut"

"Eric Brown"

## MERGE using dynamic node labels and relationship types

Node labels and relationship types can be referenced dynamically in expressions, parameters, and variables when merging nodes and relationships. This allows for more flexible queries and mitigates the risk of Cypher injection. (For more information about Cypher injection, see Neo4j Knowledge Base → Protecting against Cypher injection ).

Syntax for merging nodes and relationships dynamically

MERGE (n:$(<expr>)) MERGE ()-[r:$(<expr>)]->()

The expression must evaluate to a STRING NOT NULL | LIST<STRING NOT NULL> NOT NULL
value. Using a LIST<STRING>
with more than one item when merging a relationship using dynamic relationship types will fail. This is because a relationship can only have exactly one type.

Parameters

{ "nodeLabels": ["Person", "Director"], "relType": "DIRECTED", "movies": ["Ladybird", "Little Women", "Barbie"] }

Merge nodes and relationships using dynamic node labels and relationship types

MERGE (greta:$($nodeLabels) {name: 'Greta Gerwig'}) WITH greta UNWIND $movies AS movieTitle MERGE (greta)-[rel:$($relType)]->(m:Movie {title: movieTitle}) RETURN greta.name AS name, labels(greta) AS labels, type(rel) AS relType, collect(m.title) AS movies

Result
name
labels
relType
movies

"Greta Gerwig"

["Person", "Director"]

"DIRECTED"

["Ladybird", "Little Women", "Barbie"]

Rows: 1

### Performance caveats

MERGE
queries that use dynamic values may not perform as well as those with static values. Neo4j is actively working to improve the performance of these queries. The table below outlines performance caveats for specific Neo4j versions.

Neo4j versions and performance caveats
Neo4j versions
Performance caveat

5.26 — 2025.07

The Cypher planner is not able to leverage indexes with index scans or seeks and must instead utilize the AllNodesScan
operator, which reads all nodes from the node store and is therefore more costly.

2025.08 — 2025.10

The Cypher planner is able to leverage token lookup indexes when matching node labels and relationship types dynamically. This is enabled by the introduction of three new query plan operators: DynamicLabelNodeLookup
, DynamicDirectedRelationshipTypeLookup
, and DynamicUndirectedRelationshipTypeLookup
. It is not, however, able to use indexes on property values. For example, MERGE (n:$(Label) {foo: bar})
will not use any indexes on n.foo
but can use a DynamicLabelNodeLookup
on $(label)
.

2025.11 — current

The Cypher planner is able to leverage indexes on property values, however:

-
It only supports exact seeks on range indexes (no full text or spatial).

-
The index order cannot be leveraged, so the planner must insert separate ordering if required later on in the query.

-
Parallel runtime seeks and scans are single-threaded.

MATCH OPTIONAL MATCH

## Nov 12 2026

The Call for Papers is now open. Submit your talk by June 15, 2026

Submit your talk

## Learn

- Sandbox

- Neo4j Community Site

- Neo4j Developer Blog

- Neo4j Videos

- GraphAcademy

- Neo4j Labs

## Social

- Twitter

- Meetups

- Github

- Stack Overflow

- Want to Speak?

## Contact Us â

- US: 1-855-636-4532

- Sweden +46 171 480 113

- UK: +44 20 3868 3223

- France: +33 (0) 1 88 46 13 20

Â© 2026 Neo4j, Inc.
Terms | Privacy | Sitemap

Neo4j Â® , Neo Technology Â® , Cypher Â® , Neo4j Â® Bloom â¢ and Neo4j Â® Aura â¢ are registered trademarks of Neo4j, Inc. All other marks are owned by their respective companies.
