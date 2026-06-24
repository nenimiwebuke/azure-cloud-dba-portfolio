# Azure Cloud DBA Portfolio – Retail Sales Data Pipeline

## Overview

This project demonstrates an end-to-end cloud data engineering pipeline built on Azure using Infrastructure as Code (Terraform), Azure Data Lake Storage Gen2, and Azure Databricks.

The solution follows a Medallion Architecture pattern:

* Bronze Layer – Raw retail sales data
* Silver Layer – Cleaned and transformed sales data
* Gold Layer – Business-ready aggregated analytics

## Technologies Used

* Azure Resource Group
* Azure Data Lake Storage Gen2
* Azure Databricks
* Terraform
* PySpark
* Spark SQL
* GitHub

## Architecture

Raw CSV Files (Bronze)
↓
PySpark Transformations
↓
Silver Layer (Cleaned Parquet)
↓
Business Aggregations
↓
Gold Layer (Analytics Ready)
↓
Spark SQL Reporting

## Project Structure

terraform/

* Infrastructure deployment code

data/

* Sample retail sales dataset

notebooks/

* Bronze-Silver-Gold pipeline notebook
* Retail sales pipeline notebook
* SQL analytics notebook

## Business Use Case

A retail organization requires sales data to be ingested from source systems, transformed into standardized formats, and aggregated for business reporting.

The pipeline calculates revenue by state and stores analytics-ready datasets in the Gold layer.

## Sample Analytics Output

| State | Total Revenue |
| ----- | ------------- |
| NY    | 2300          |
| CA    | 1350          |
| TX    | 600           |
| FL    | 550           |
