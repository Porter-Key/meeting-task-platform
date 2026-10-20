# Introduction - Neo4j GenAI Plugin

Source: https://neo4j.com/docs/genai/plugin/current/
Fetched: 2026-05-07T05:05:40.522671+00:00

Introduction - Neo4j GenAI Plugin

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

Neo4j GenAI Plugin

Product Version Version 25 (Current) Version 5

-
- Introduction

- Create and store embeddings

- Generate text & Chat

- Generate structured output

- Count tokens and chunk text by token length

- Reference

- Functions and procedures

- Configuration settings

- Changelog

Is this page helpful?

- Neo4j GenAI Plugin

- Introduction

Raise an issue

# Introduction

Neo4j’s GenAI plugin provides functions and procedures to interact with external AI providers through Cypher, such as for creating vector embeddings and generating text.

To use the plugin’s features, you need an account and API credentials from one of the supported external AI providers: (OpenAI, Azure OpenAI, VertexAI, Amazon Bedrock).

## Installation

In Neo4j Aura , the GenAI plugin is enabled by default.

On self-managed instances , you install the plugin by moving the neo4j-genai-plugin-<version>.jar
file from <NEO4J_HOME>/products
to <NEO4J_HOME>/plugins
, or, if you are using Docker, by starting the Docker container with the extra parameter --env NEO4J_PLUGINS='["genai"]'
. For more information, see Operations Manual → Configure plugins .

Most GenAI features are available only in Cypher 25. If your database’s default language is Cypher 5, prepend the query with CYPHER 25
to override the default for that query (see Cypher → Select Cypher version ).

## Environment setup

The examples in this manual use the Neo4j movie recommendations dataset, mostly focusing on the plot
and title
properties of Movie
nodes. There are 9083 Movie
nodes with a plot
and title
property.

To follow the examples in this manual, you need to import a dump file. The file to import depends on the edition/deployment of Neo4j you are using and which storage format is available:

-
Enterprise Edition or any Aura instance — Import the dump file in block format.

-
Community Edition — Import the dump file in aligned format.

For instructions on importing dump files, see Aura → Backup, export, restore, and upload or Operations manual → Restore a database dump .

Create and store embeddings

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
