# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) 
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.3.0 2017-02-23]
### Added
- basic gene page 
- basic gene information loaded from standard JSON schema, loaded into ES and displayed on gene page dynamically.
- DIOPT data produced in JSON format, also loaded into a PostgreSQL database loader written but not automatically pulling in data with this loader yet as a result of memory issues.
- hardcoded example data disease and orthology tables on the gene page
- jbrowse integration on the gene page
- search mapping updated to use basic gene information JSON schema and data.
- autocomplete of search functions with symbols and names.
- implemented class architecture for load scripts.
- loading BGI data comes from an S3 bucket now.
- upgraded to ElasticSearch 5

### Deprecated
- removed panther data and loads and ui components
- removed omim data and loads and ui components

