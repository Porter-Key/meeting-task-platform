# Introduction - Cypher Manual

Source: https://neo4j.com/docs/cypher-manual/current/introduction/
Fetched: 2026-05-07T05:05:36.475004+00:00

Introduction - Cypher Manual

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

- Introduction

Raise an issue

# Introduction

Welcome to the Neo4j Cypher® Manual.

Cypher is Neo4jâs declarative query language, allowing users to unlock the full potential of property graph databases.

This manual covers Cypher 25. As of Neo4j 2025.06, all new Cypher features are exclusively added to Cypher 25, while Cypher 5 is frozen. As of Neo4j 2026.02, new databases explicitly set Cypher 25 as their query language in their configuration file. For information about how to how to use Cypher 25, see Select Cypher version . For information about new features added to Cypher 25, see Additions, deprecations, removals, and compatibility .

The Cypher Manual aims to be as instructive as possible to readers from a variety of backgrounds and professions, such as developers, administrators, and academic researchers.

If you are new to Cypher and Neo4j, you can visit the Getting Started Guide → Cypher chapter. Additionally, Neo4j GraphAcademy has a variety of free courses tailored for all levels of experience.

For a reference of all available Cypher features, see the Cypher Cheat Sheet .

For a downloadable PDF version of the Cypher Manual, visit the Neo4j documentation archive .

This introduction will cover the following topics:

-
Overview

-
Cypher and Neo4j

-
Cypher and Aura

License: Creative Commons 4.0

Overview

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
