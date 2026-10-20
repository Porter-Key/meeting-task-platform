# Build applications with Neo4j and Python - Neo4j Python Driver Manual

Source: https://neo4j.com/docs/python-manual/current/
Fetched: 2026-05-07T05:05:38.413044+00:00

Build applications with Neo4j and Python - Neo4j Python Driver Manual

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

Cypher Query Language
- Cypher

- Cypher Cheat Sheet

- APOC Library

Generative AI
- Neo4j GraphRAG for Python

- Embeddings and vector indexes tutorial

- GenAI integrations

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
- Into to Graph Data Science

- Graph Data Science Fundamentals

- Path Finding

Generative AI Courses
- Neo4j & LLM Fundamentals

- Vector Indexes & Unstructured Data

- Build a Chatbot with Python

- Build a Chatbot with TypeScript

Neo4j Certification
- Neo4j Certified Professional

- Neo4j Graph Data Science Certification

Get Started Free

Search

Skip to content

Neo4j Python Driver Manual

Product Version Version 6 (Current) Version 5 Version 4.4

-
- Quickstart

- Regular workflow

- Installation

- Connect to the database

- Query the database

- Manipulate query results

- Advanced usage

- Run your own transactions

- Explore the query execution summary

- Coordinate parallel transactions

- Run concurrent transactions

- Further query mechanisms

- Performance recommendations

- Reference

- Advanced connection information

- Data types and mapping to Cypher types

- Upgrade from older versions

- API documentation

- GraphAcademy courses

- Graph Data Modeling Fundamentals

- Intermediate Cypher Queries

- Building Neo4j Applications with Python

Is this page helpful?

- Neo4j Python Driver Manual

- Quickstart

Raise an issue

# Build applications with Neo4j and Python

The Neo4j Python driver is the official library to interact with a Neo4j instance through a Python application.

At the hearth of Neo4j lies Cypher , the query language to interact with a Neo4j database. Although this guide does not require you to be a seasoned Cypher querier, it’s easier to focus on the Python-specific bits if you know some Cypher already. You will also get a gentle introduction to Cypher in these pages, but check out Getting started → Cypher for a more detailed walkthrough of graph databases modelling and querying if this is your first approach.

## Install

Install the Neo4j Python driver with pip
:

pip install neo4j

More info on installing the driver

## Connect to the database

Connect to a database by creating a Driver
object and providing a URL and an authentication token. Once you have a Driver
instance, use the .verify_connectivity()
method to ensure that a working connection can be established.

from neo4j import GraphDatabase # URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io" URI = "<database-uri>" AUTH = ("<username>", "<password>") with GraphDatabase.driver(URI, auth=AUTH) as driver: driver.verify_connectivity()

More info on connecting to a database

## Create an example graph

Run a Cypher query with the method Driver.execute_query()
. Do not hardcode or concatenate parameters: use placeholders and specify the parameters as keyword arguments.

Create two Person
nodes and a KNOWS
relationship between them

summary = driver.execute_query(""" CREATE (a:Person {name: $name}) CREATE (b:Person {name: $friendName}) CREATE (a)-[:KNOWS]->(b) """, name="Alice", friendName="David", database_="<database-name>", ).summary print("Created {nodes_created} nodes in {time} ms.".format( nodes_created=summary.counters.nodes_created, time=summary.result_available_after ))

More info on querying the database

## Query a graph

To retrieve information from the database, use the Cypher clause MATCH
:

Retrieve all Person
nodes who know other persons

records, summary, keys = driver.execute_query(""" MATCH (p:Person)-[:KNOWS]->(:Person) RETURN p.name AS name """, database_="<database-name>", ) # Loop through results and do something with them for record in records: print(record.data()) # obtain record as dict # Summary information print("The query `{query}` returned {records_count} records in {time} ms.".format( query=summary.query, records_count=len(records), time=summary.result_available_after ))

More info on querying the database

## Close connections and sessions

Unless you created them using the with
statement, call the .close()
method on all Driver
and Session
instances to release any resources still held by them.

from neo4j import GraphDatabase driver = GraphDatabase.driver(URI, auth=AUTH) session = driver.session(database="<database-name>") # session/driver usage session.close() driver.close()

## Glossary

LTS
A Long Term Support release is one guaranteed to be supported for a number of years. Neo4j 4.4 and 5.26 are LTS versions.
Aura
Aura is Neo4j’s fully managed cloud service. It comes with both free and paid plans.
Cypher
Cypher is Neo4j’s graph query language that lets you retrieve data from the database. It is like SQL, but for graphs.
APOC
Awesome Procedures On Cypher (APOC) is a library of (many) functions that can not be easily expressed in Cypher itself.
Bolt
Bolt is the protocol used for interaction between Neo4j instances and drivers. It listens on port 7687 by default.
ACID
Atomicity, Consistency, Isolation, Durability (ACID) are properties guaranteeing that database transactions are processed reliably. An ACID-compliant DBMS ensures that the data in the database remains accurate and consistent despite failures.
eventual consistency
A database is eventually consistent if it provides the guarantee that all cluster members will, at some point in time , store the latest version of the data.
causal consistency
A database is causally consistent if read and write queries are seen by every member of the cluster in the same order. This is stronger than eventual consistency .
NULL
The null marker is not a type but a placeholder for absence of value. For more information, see Cypher → Working with null
.
transaction
A transaction is a unit of work that is either committed in its entirety or rolled back on failure. An example is a bank transfer: it involves multiple steps, but they must all succeed or be reverted, to avoid money being subtracted from one account but not added to the other.
backpressure
Backpressure is a force opposing the flow of data. It ensures that the client is not being overwhelmed by data faster than it can handle.
bookmark
A bookmark is a token representing some state of the database. By passing one or multiple bookmarks along with a query, the server will make sure that the query does not get executed before the represented state(s) have been established.
transaction function
A transaction function is a callback executed by an execute_read
or execute_write
call. The driver automatically re-executes the callback in case of server failure.
Driver
A Driver
object holds the details required to establish connections with a Neo4j database.

Installation

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
