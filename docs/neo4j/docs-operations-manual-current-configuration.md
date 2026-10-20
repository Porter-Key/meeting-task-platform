# Configuration - Operations Manual

Source: https://neo4j.com/docs/operations-manual/current/configuration/
Fetched: 2026-05-07T05:05:38.067469+00:00

Configuration - Operations Manual

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

Operations Manual

Product Version Version 2026.04 (Current) Version 5.26 (LTS) Version 4.4

-
- The Neo4j Operations Manual

- Introduction

- Installation
- System requirements

- Linux installation
- Debian-based distributions (.deb)

- Red Hat, CentOS, Fedora, and Amazon Linux (.rpm)

- Linux executable (.tar)

- Neo4j system service

- macOS installation

- Windows installation

- Neo4j Desktop

- Cloud deployments
- Neo4j on AWS

- Neo4j on GCP

- Docker
- Getting started with Neo4j in Docker

- Persisting data with Docker volumes

- Modify the default configuration

- Plugins

- Deploy a Neo4j standalone server using Docker Compose

- Deploy a Neo4j cluster on multiple Docker hosts

- Access Neo4j

- Docker-specific operations

- Dump and load a Neo4j database (offline)

- Back up and restore a Neo4j database (online)

- SSL encryption in a Neo4j Docker container

- Docker-specific configuration settings

- Kubernetes
- Introduction

- Configuring the Neo4j Helm chart repository

- Quickstart: Deploy a standalone instance
- Neo4j Helm chart for standalone server deployments

- Prerequisites

- Create a Helm deployment values.yaml file

- Install a Neo4j standalone instance

- Verify the installation

- Uninstall Neo4j and clean up the created resources

- Quickstart: Deploy a cluster
- Neo4j Helm chart for cluster deployments

- Prerequisites

- Create Helm deployment values files

- Install Neo4j cluster servers

- Verify the Neo4j cluster formation

- Access the Neo4j cluster from inside Kubernetes

- Access the Neo4j cluster from outside Kubernetes

- Uninstall Neo4j cluster and clean up resources

- Quickstart: Deploy a Neo4j cluster for analytic queries

- Volume mounts and persistent volumes

- Customizing a Neo4j Helm chart

- Configuring SSL

- Authentication and authorization

- Plugins

- Accessing Neo4j

- Accessing Neo4j using Kubernetes Ingress

- Importing data

- Monitoring

- Operations
- Maintenance modes

- Reset the neo4j
user password

- Restart a Neo4j pod after configuration change

- Dump and load databases (offline)

- Back up, aggregate, and restore (online)

- Upgrade Neo4j on Kubernetes

- Migrate Neo4j from Labs Helm to Neo4j Helm charts

- Scale a Neo4j deployment

- Use custom images from private registries

- Assign Neo4j pods to specific nodes

- Troubleshooting

- Configuration
- The neo4j.conf file

- Command expansion

- Default file locations

- Ports

- Configure the Cypher default version

- Configure network connectors

- Set an initial password

- Get initial memory recommendations

- Plugins

- Update dynamic settings

- Migrate configurations

- Validate configurations

- Configuration settings
- Checkpoint settings

- Cloud storage integration settings

- Cluster settings

- Connection settings

- Cypher settings

- Database settings

- DBMS settings

- Fleet Manager settings

- Import settings

- Index settings

- Logging settings

- Memory settings

- Metrics settings

- Neo4j Browser and client settings

- Kubernetes settings

- Security settings

- Server directories settings

- Server settings

- Transaction settings

- Transaction log settings

- Import

- Database administration
- Database management command syntax

- Standard databases
- Naming rules for databases

- Create databases

- Create a database from a URI

- List databases

- Alter databases

- Start and stop databases

- Recreate a database

- Delete databases

- Migrate a database

- Upload to Neo4j Aura

- WAIT
options

- Configuration parameters

- Error handling

- Database aliases
- Naming rules for database aliases

- Managing database aliases for standard databases

- Managing database aliases in composite databases

- Configuring remote database aliases

- Query routing decisions

- Clustering
- Introduction: Neo4j clustering architecture

- Setting up a cluster
- Deploy a basic cluster

- Deploy an analytics cluster

- Move from a standalone deployment to a cluster

- Reconciler

- Cluster server discovery

- Leadership, routing, and load balancing

- Intra-cluster encryption

- Managing servers in a cluster

- Unbind a server

- Managing databases in a cluster

- Unbind the system
database

- Replicating databases across clusters

- Monitoring
- Monitor servers

- Monitor databases

- Monitor cluster endpoints for status information

- Monitor replication status

- Resilient multi-region cluster deployment
- Designing a resilient multi-data center cluster

- Multi-data center routing

- Disaster recovery

- Settings reference

- Server management command syntax

- Clustering glossary

- Scalability
- Concepts

- Scaling with Neo4j

- Composite databases
- Concepts

- Create composite databases

- List composite databases

- Alter composite databases

- Start and stop composite databases

- Delete composite databases

- Set up and query composite databases

- Role-based access control (RBAC)

- Sharding data with the copy
command

- Property sharding (Infinigraph)
- Overview

- Planning and sizing

- System requirements and configuration

- Data import

- Creating sharded property databases

- Starting and stopping sharded property databases

- Listing sharded property databases

- Altering sharded property databases

- Resharding databases

- Deleting sharded property databases

- Role-based access control (RBAC)

- Admin operations

- Security

- Limitations and considerations

- Database internals and transactional behavior
- Transaction management

- Concurrent data access

- Transaction logging

- Checkpointing and log pruning

- Store formats

- Display store information

- Backup and restore
- Backup and restore planning

- Backup modes

- Back up an online database

- Aggregate a database backup chain

- Inspect the metadata of a backup file

- Validate a sharded property database backup

- Check database consistency

- Restore a database backup

- Back up an offline database

- Restore a database dump

- Copy a database store

- Authentication and authorization
- Manage users

- Manage roles

- Recover admin user and password

- Manage privileges
- Role-based access control

- Read privileges

- Property-based access control

- Attribute-based access control

- Write privileges

- Database privileges

- DBMS privileges
- Administrator role privileges

- The DBMS ROLE MANAGEMENT
privileges

- The DBMS USER MANAGEMENT
privileges

- The DBMS IMPERSONATE
privileges

- The DBMS AUTH RULE MANAGEMENT
privileges

- The DBMS DATABASE MANAGEMENT
privileges

- The DBMS ALIAS MANAGEMENT
privileges

- The DBMS SERVER MANAGEMENT
privileges

- The DBMS PRIVILEGE MANAGEMENT
privileges

- The DBMS EXECUTE
privileges

- The DBMS SETTING
privileges

- Load privileges

- Limitations

- Procedure and user-defined function privileges

- Built-in roles and privileges

- Immutable roles and privileges

- Integration with auth systems
- User auth providers

- LDAP integration

- Single sign-on integration

- Security
- Securing extensions

- SSL framework
- Configuring SSL for FIPS 140-2 compatibility

- Browser credentials handling

- Security checklist

- Performance
- Memory configuration

- Vector index memory configuration

- Index configuration

- Tuning of the garbage collector

- Bolt thread pool configuration

- Linux file system tuning

- Disks, RAM and other tips

- Statistics and execution plans

- Space reuse

- Monitoring
- Logging

- Metrics
- Essential metrics

- Enable metrics logging

- Expose metrics

- Metrics reference

- Manage queries

- Manage connections

- Manage background jobs

- Generate a report about the system

- Monitor your deployments using Fleet Manager

- Neo4j Admin and Neo4j CLI

- Cypher Shell

- Procedures

- Changes, deprecations, and removals
- Changes in Neo4j 2025-2026 series

- Current deprecations

- Breaking changes in Neo4j 2025.01

- Tutorials
- Importing data

- Setting up and using a composite database

- Fine-grained access control

- Configuring Neo4j Single Sign-On (SSO)

- Deploying a Neo4j cluster in a Docker container

Is this page helpful?

- Operations Manual

- Configuration

Raise an issue

# Configuration

The topics described are:

-
The neo4j.conf file — An introduction to the primary configuration file in Neo4j.

-
Command expansion — How to provide an additional capability to configure Neo4j by allowing to specify scripts that set values sourced from external files.

-
Default file locations — An overview of where files are stored in the different Neo4j distributions and the necessary file permissions for running Neo4j.

-
Ports — An overview of the ports relevant to a Neo4j installation.

-
Configure the Cypher default version — How to configure the Cypher version.

-
Configure network connectors — How to configure network connectors for Neo4j.

-
Set initial password — How to set an initial password.

-
Get initial memory recommendations — How to get initial memory recommendations for Neo4j.

-
Configure Neo4j plugins — How to load plugins into a Neo4j deployment.

-
Update dynamic settings — How to configure certain Neo4j parameters while Neo4j is running.

-
Migrate configurations — How to migrate configuration settings from a previous version of Neo4j to a new version.

-
Validate configurations — How to validate Neo4j and Log4j configurations.

-
Configuration settings — A complete reference of all configuration settings.

For a complete reference of Neo4j configuration settings, see All configuration settings .

Troubleshooting The neo4j.conf file

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
