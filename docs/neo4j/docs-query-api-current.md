# Introduction - Query API

Source: https://neo4j.com/docs/query-api/current/
Fetched: 2026-05-07T05:05:39.951099+00:00

Introduction - Query API

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

Theme

Light

Dark

Search

Skip to content

Query API

-
- Introduction

- Authorize requests

- Query the database

- Run transactions

- Route queries to read cluster members

- Retrieve query counters

- Profile queries

- Coordinate transactions and enforce causal consistency

- Run queries as a different user

- Stream results

- Reference

- Endpoints

- Headers

- Result formats & Data types
- Plain JSON

- Typed JSON

- Changelog

Is this page helpful?

- Query API

- Introduction

Raise an issue

# Introduction
Introduced in 5.19

The Query API is enabled by default. It was however disabled by default on self-managed instances versions < 5.25. To enable it on those deployments, add QUERY_API_ENDPOINTS
to the configuration setting server.http_enabled_modules
.

The Query API allows to execute Cypher statements against a Neo4j server through HTTP requests. This API supersedes the deprecated HTTP API .

The main use case of the API is for developing client applications in languages for which there is no supported library. If there exists an official library (driver) for the language you are using, consider using that instead — see Create applications .

On self-managed instances , the API uses port 7474 for HTTP and port 7473 for HTTPS by default. Ports can be altered via the configuration settings server.http.listen_address
and server.https.listen_address
.
Aura instances support only HTTPS through port 443.

This guide assumes that you have:

-
A running instance of Neo4j — If you don’t have one, install Neo4j locally or sign up for an Aura cloud instance .

-
Some familiarity with Cypher — If you are new to it, check out Getting started → Cypher .

The Query API supports HTTP/2 as well as HTTP/1.1, unless either is explicitly disabled in the server configuration setting server.http_enabled_transports
. It’s up to the client to initiate a connection with the preferred protocol.

## Glossary

Aura
Aura is Neo4j’s fully managed cloud service. It comes with both free and paid plans.
Cypher
Cypher is Neo4j’s graph query language that lets you retrieve data from the database. It is like SQL, but for graphs.
ACID
Atomicity, Consistency, Isolation, Durability (ACID) are properties guaranteeing that database transactions are processed reliably. An ACID-compliant DBMS ensures that the data in the database remains accurate and consistent despite failures.
causal consistency
A database is causally consistent if read and write queries are seen by every member of the cluster in the same order. This is stronger than eventual consistency.
transaction
A transaction is a unit of work that is either committed in its entirety or rolled back on failure. An example is a bank transfer: it involves multiple steps, but they must all succeed or be reverted, to avoid money being subtracted from one account but not added to the other.

Authorize requests

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
