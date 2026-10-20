# MATCH - Cypher Manual

Source: https://neo4j.com/docs/cypher-manual/current/clauses/match/
Fetched: 2026-05-07T05:05:36.800960+00:00

MATCH - Cypher Manual

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

- MATCH

Raise an issue

# MATCH

The MATCH
clause enables you to define specific patterns that the database will search for within its graph structure. The MATCH
clause can specify the nodes, relationships, and properties in a pattern, allowing for queries that traverse the graph to retrieve relevant data.

## Example graph

The following graph is used for the examples below:

To recreate the graph, run the following query against an empty Neo4j database:

CREATE (charlie:Person:Actor {name: 'Charlie Sheen'}), (martin:Person:Actor {name: 'Martin Sheen'}), (michael:Person:Actor {name: 'Michael Douglas'}), (oliver:Person:Director {name: 'Oliver Stone'}), (rob:Person:Director {name: 'Rob Reiner'}), (wallStreet:Movie {title: 'Wall Street'}), (charlie)-[:ACTED_IN {role: 'Bud Fox'}]->(wallStreet), (martin)-[:ACTED_IN {role: 'Carl Fox'}]->(wallStreet), (michael)-[:ACTED_IN {role: 'Gordon Gekko'}]->(wallStreet), (oliver)-[:DIRECTED]->(wallStreet), (thePresident:Movie {title: 'The American President'}), (martin)-[:ACTED_IN {role: 'A.J. MacInerney'}]->(thePresident), (michael)-[:ACTED_IN {role: 'President Andrew Shepherd'}]->(thePresident), (rob)-[:DIRECTED]->(thePresident)

## Find nodes

The MATCH
clause allows you to specify node patterns of varying complexity to retrieve from a graph. For more information about finding node patterns, see Patterns → Node patterns .

### Find all nodes

By specifying a pattern with a single node and no labels, all nodes in the graph will be returned.

Find all nodes in a graph

MATCH (n) RETURN n

Result
n

(:Person {"name":"Charlie Sheen"})

(:Person {"name":"Martin Sheen"})

(:Person {"name":"Michael Douglas"})

(:Person {"name":"Oliver Stone"})

(:Person {"name":"Rob Reiner"})

(:Movie {"title":"Wall Street"})

(:Movie {"title":"The American President"})

Rows: 7

### Find nodes with a specific label

Find all nodes with the Movie
label

MATCH (movie:Movie) RETURN movie.title

Result
movie.title

"Wall Street"

"The American President"

Rows: 2

### MATCH using node label expressions

Node pattern using the OR
( |
) label expression

MATCH (n:Movie|Person) RETURN n.name AS name, n.title AS title

Result
name
title

"Charlie Sheen"

<null>

"Martin Sheen"

<null>

"Michael Douglas"

<null>

"Oliver Stone"

<null>

"Rob Reiner"

<null>

<null>

"Wall Street"

<null>

"The American President"

Rows: 7

Node pattern using negation ( !
) label expression

MATCH (n:!Movie) RETURN labels(n) AS label, count(n) AS labelCount

The above query uses the labels()
and count()
functions.

Result
label
labelCount

["Person", "Actor"]

3

["Person", "Director"]

2

Rows: 2

For a list of all label expressions supported by Cypher®, see Patterns → Label expressions .

## Find relationships

The MATCH
clause allows you to specify relationship patterns of varying complexity to retrieve from a graph. Unlike a node pattern, a relationship pattern cannot be used in a MATCH
clause without node patterns at both ends. For more information about relationship patterns, see Patterns → Relationship patterns .

By default, Cypher will only match a relationship once inside a single pattern. This behavior can be bypassed using REPEATABLE ELEMENTS
, which allows both nodes and relationships to occur more than once in a given MATCH
result. For more information, see REPEATABLE ELEMENTS
.

### Empty relationship patterns

By applying --
, a pattern will be matched for a relationship with any direction and without any filtering on relationship types or properties.

Find connected nodes using an empty relationship pattern

MATCH (:Person {name: 'Oliver Stone'})--(n) RETURN n AS connectedNodes

Result
connectedNodes

(:Movie {title: "Wall Street"})

Rows: 1

### Directed relationship patterns

The direction of a relationship in a pattern is indicated by arrows: -->
or <--
.

Find all nodes connected to Oliver Stone
by an outgoing relationship.

MATCH (:Person {name: 'Oliver Stone'})-->(movie:Movie) RETURN movie.title AS movieTitle

Result
movieTitle

"Wall Street"

Rows: 1

### Relationship variables

It is possible to introduce a variable to a pattern, either for filtering on relationship properties or to return a relationship.

Find the types of an aliased relationship

MATCH (:Person {name: 'Oliver Stone'})-[r]->() RETURN type(r) AS relType

The above query uses the type()
function .

Result
relType

"DIRECTED"

Rows: 1

### MATCH on an undirected relationship

When a pattern contains a bound relationship, and that relationship pattern does not specify direction, Cypher will match the relationship in both directions.

Relationship pattern without direction

MATCH (a)-[:ACTED_IN {role: 'Bud Fox'}]-(b) RETURN a, b

Result
a
b

(:Movie {"title":"Wall Street"})

(:Person {"name":"Charlie Sheen"})

(:Person {"name":"Charlie Sheen"})

(:Movie {"title":"Wall Street"})

Rows: 2

### Filter on relationship types

It is possible to specify the type of a relationship in a relationship pattern by using a colon ( :
) before the relationship type.

Relationship pattern filtering on the ACTED_IN
relationship type

MATCH (:Movie {title: 'Wall Street'})<-[:ACTED_IN]-(actor:Person) RETURN actor.name AS actor

Result
actor

"Michael Douglas"

"Martin Sheen"

"Charlie Sheen"

Rows: 3

### MATCH using relationship type expressions

It is possible to match a pattern containing one of several relationship types using the OR
symbol, |
.

Relationship pattern including either ACTED_IN
or DIRECTED
relationship types

MATCH (:Movie {title: 'Wall Street'})<-[:ACTED_IN|DIRECTED]-(person:Person) RETURN person.name AS person

Result
person

"Oliver Stone"

"Michael Douglas"

"Martin Sheen"

"Charlie Sheen"

Rows: 4

As relationships can only have exactly one type each, ()-[:A&B]→()
will never match a relationship.

For a list of all relationship type expressions supported by Cypher, see Patterns → Label expressions .

### Find multiple relationships

A graph pattern can contain several relationship patterns.

Graph pattern including several relationship patterns

MATCH (:Person {name: 'Charlie Sheen'})-[:ACTED_IN]->(movie:Movie)<-[:DIRECTED]-(director:Person) RETURN movie.title AS movieTitle, director.name AS director

Result
movieTitle
director

"Wall Street"

"Oliver Stone"

Rows: 1

## MATCH with WHERE predicates

The MATCH
clause is often paired with a WHERE
sub-clause, which adds predicates to refine the patterns, making them more specific. These predicates are part of the pattern itself, not just filters applied after matching. Thus, always place the WHERE
clause with its corresponding MATCH
clause.

Simple WHERE
predicate

MATCH (charlie:Person)-[:ACTED_IN]->(movie:Movie) WHERE charlie.name = 'Charlie Sheen' RETURN movie.title AS movieTitle

Result
movieTitle

"Wall Street"

Rows: 1

More complex WHERE
predicate

MATCH (martin:Person)-[:ACTED_IN]->(movie:Movie) WHERE martin.name = 'Martin Sheen' AND NOT EXISTS { MATCH (movie)<-[:DIRECTED]-(director:Person {name: 'Oliver Stone'}) } RETURN movie.title AS movieTitle

The above query uses an EXISTS
subquery .

Result
movieTitle

"The American President"

Rows: 1

For more information, see the WHERE
page.

## MATCH with parameters

The MATCH
clause can be used with parameters.

Parameters

{ "movieTitle": "Wall Street", "actorRole": "Fox" }

Find nodes using paramters

MATCH (:Movie {title: $movieTitle})<-[r:ACTED_IN]-(p:Person) WHERE r.role CONTAINS $actorRole RETURN p.name AS actor, r.role AS role

The above query uses the CONTAINS
operator .

Result
actor
role

"Charlie Sheen"

"Bud Fox"

"Martin Sheen"

"Carl Fox"

Rows: 2

For more information about how to set parameters, see Syntax → Parameters .

## Find paths

The MATCH
clause can also be used to bind whole paths to variables.

Find all paths matching a pattern

MATCH path = ()-[:ACTED_IN]->(movie:Movie) RETURN path

Result
path

(:Person {name: "Charlie Sheen"})-[:ACTED_IN {role: "Bud Fox"}]→(:Movie {title: "Wall Street"})

(:Person {name: "Martin Sheen"})-[:ACTED_IN {role: "Carl Fox"}]→(:Movie {title: "Wall Street"})

(:Person {name: "Martin Sheen"})-[:ACTED_IN {role: "A.J. MacInerney"}]→(:Movie {title: "The American President"})

(:Person {name: "Michael Douglas"})-[:ACTED_IN {role: "Gordon Gekko"}]→(:Movie {title: "Wall Street"})

(:Person {name: "Michael Douglas"})-[:ACTED_IN {role: "President Andrew Shepherd"}]→(:Movie {title: "The American President"})

Rows: 5

Find paths matching a pattern including a WHERE
predicate

MATCH path = (:Person)-[:ACTED_IN]->(movie:Movie)<-[:DIRECTED]-(:Person) WHERE movie.title = 'Wall Street' RETURN path

Result
path

(:Person {name: "Charlie Sheen"})-[:ACTED_IN {role: "Bud Fox"}]→(:Movie {title: "Wall Street"})←[:DIRECTED]-(:Person {name: "Oliver Stone"})

(:Person {name: "Martin Sheen"})-[:ACTED_IN {role: "Carl Fox"}]→(:Movie {title: "Wall Street"})←[:DIRECTED]-(:Person {name: "Oliver Stone"})

(:Person {name: "Michael Douglas"})-[:ACTED_IN {role: "Gordon Gekko"}]→(:Movie {title: "Wall Street"})←[:DIRECTED]-(:Person {name: "Oliver Stone"})

Rows: 3

For more information about how MATCH
is used to find patterns of varying complexity (including quantified path patterns , quantified relationships , and the shortest paths between nodes), see the section on Patterns .

## Multiple MATCH clauses, the WITH clause, and clause composition

In Cypher, the behavior of a query is defined by its clauses. Each clause takes the current graph state and a table of intermediate results, processes them, and passes the updated graph state and results to the next clause. The first clause starts with the graph’s initial state and an empty table, while the final clause produces the query result.

Chaining consecutive MATCH
clauses

MATCH (:Person {name: 'Martin Sheen'})-[:ACTED_IN]->(movie:Movie) (1) MATCH (director:Person)-[:DIRECTED]->(movie) (2) RETURN director.name AS director, movie.title AS movieTitle

1
The result of the first MATCH
clause is the variable movie
which holds all the Movies
that Martin Sheen
has ACTED_IN
.

2
The second MATCH
clause uses the movie
variable to find any Person
node with a DIRECTED
relationship to those Movie
nodes that Martin Sheen
has ACTED_IN
.

Result
director
movieTitle

"Oliver Stone"

"Wall Street"

"Rob Reiner"

"The American President"

Rows: 2

A variable can be implicitly carried over to the following clause by being referenced in another operation. A variable can also be explicitly passed to the following clause using the WITH
clause. If a variable is neither implicitly nor explicitly carried over to its following clause, it will be discarded and is not available for reference later in the query.

Using WITH
and multiple MATCH
clauses

MATCH (actors:Person)-[:ACTED_IN]->(movies:Movie) (1) WITH actors, count(movies) AS movieCount (2) ORDER BY movieCount DESC LIMIT 1 (3) MATCH (actors)-[:ACTED_IN]->(movies) (4) RETURN actors.name AS actor, movieCount, collect(movies.title) AS movies

1
The Person
and Movie
nodes matched in this step are stored in variables, which are then passed on to the second row of the query.

2
The movies
variable is implicitly imported by its occurrence in the count()
function. The WITH
clause explicitly imports the actors
variable.

3
An ORDER BY
clause orders the results by movieCount
in descending order, ensuring that the Person
with the highest number of movies appears at the top, and LIMIT
1
ensures that all other Person
nodes are discarded.

4
The second MATCH
clause finds all Movie
nodes associated with the Person
nodes currently bound to the actors
variable.

The above query uses the collect()
function .

Result
actor
movieCount
movies

"Martin Sheen"

2

["Wall Street", "The American President"]

Rows: 1

For more information about how Cypher queries work, see Clause composition .

## MATCH using dynamic node labels and relationship types

Node labels and relationship types can be referenced dynamically in expressions, parameters, and variables when matching nodes and relationships. This allows for more flexible queries and mitigates the risk of Cypher injection. (For more information about Cypher injection, see Neo4j Knowledge Base → Protecting against Cypher injection ).

Syntax for matching node labels dynamically

MATCH (n:$(<expr>)) MATCH (n:$any(<expr>)) MATCH (n:$all(<expr>))

MATCH (n:$all(<expr>))
is functionally equivalent to MATCH (n:$(<expr>))
.

Syntax for matching relationship types dynamically

MATCH ()-[r:$(<expr>))]->() MATCH ()-[r:$any(<expr>)]->() MATCH ()-[r:$all(<expr>))]->()

The expression must evaluate to a STRING NOT NULL | LIST<STRING NOT NULL> NOT NULL
value. If you use a LIST<STRING>
with more than one item in a relationship pattern with dynamic relationship types, no results will be returned. This is because a relationship can only have exactly one type.

Match labels dynamically

WITH ["Person", "Director"] AS labels MATCH (directors:$(labels)) RETURN directors

Result
directors

(:Person:Director {name: "Oliver Stone"})

(:Person:Director {name: "Rob Reiner"})

Rows: 2

Match nodes dynamically using any()

MATCH (n:$any(["Movie", "Actor"])) RETURN n AS nodes

Result
nodes

(:Person:Actor {name: "Charlie Sheen"})

(:Person:Actor {name: "Martin Sheen"})

(:Person:Actor {name: "Michael Douglas"})

(:Movie {title: "Wall Street"})

(:Movie {title: "The American President"})

Rows: 5

Parameter

{ "label": "Movie" }

Match nodes dynamically using a parameter

MATCH (movie:$($label)) RETURN movie.title AS movieTitle

Result
movieTitle

"Wall Street"

"The American President"

Rows: 2

Match relationships dynamically using a variable

CALL db.relationshipTypes() YIELD relationshipType MATCH ()-[r:$(relationshipType)]->() RETURN relationshipType, count(r) AS relationshipCount

Result
relationshipType
relationshipCount

"ACTED_IN"

5

"DIRECTED"

2

Rows: 2

### Performance caveats

MATCH
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
. It is not, however, able to use indexes on property values. For example, MATCH (n:$(Label) {foo: bar})
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

-
The planner doesn’t combine multiple property index seeks when generating the results for the dynamic part of the query. For example, using $any
in combination with multiple labels that share an index on a property result in the operator choosing one of the indexes based on selectivity and then stepping through the seek results and filtering for the remainder of the expression. + Example:

CREATE RANGE INDEX actor_has_birthyear FOR (a:Actor) ON (a.birthYear) CREATE RANGE INDEX director_has_birthyear FOR (d:Director) ON (d.birthYear) MATCH (p:$any(["Actor", "Director"]) { birthYear: 1983 }) RETURN p.name

### Further reading

Neo4j Developer Blog: Cypher Dynamism: A Step Toward Simpler and More Secure Queries

LOAD CSV MERGE

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
