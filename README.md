
# Project Title:
# monitoring_cpu_usage

## Description
A simple project using InfluxDB to demonstrate its core functionalities
- such as writing data
- querying
- managing time series data.
This example focuses on monitoring CPU usage over time, a typical use case for InfluxDB.

## Project Overview
The project will:
- write CPU usage data to an InfluxDB bucket
- query the data to calculate average CPU usage
- demonstrate retention policy and organization basics

## Requirements
InfluxDB installed or running via Docker.
Python installed, with the influxdb-client library.

## Installation notes
Step 1: Start InfluxDB using Docker:
`docker run -d -p 8086:8086 --name=influxdb -e INFLUXDB_ADMIN_USER=admin -e INFLUXDB_ADMIN_PASSWORD=password influxdb:latest`
Step 2: Install Required Library
`pip install influxdb-client`
Step 3: Set Up InfluxDB Token and Organization
Open the InfluxDB UI at http://localhost:8086.
Log in using the credentials you set (admin/password).
Set up your organization and bucket in the UI.
Generate an API Token and replace INFLUXDB_TOKEN in the script with it.

## Usage - How to Run the Project
Start the InfluxDB instance (e.g., via Docker).
Run the Python script:
`python influxdb_example.py`
Observe data writing and querying in the terminal.
This example introduces time-series concepts, InfluxDB's strengths, and real-world usage in monitoring scenarios.

## Basic Additional Info
InfluxDB Client: The influxdb-client library provides APIs for writing, querying, and managing data.
Data Structure: Data is stored as points with fields, tags, and a timestamp.
Flux Queries: InfluxDB uses Flux, a powerful query language.
Retention Policies: Data in InfluxDB can be automatically removed after a specified period using retention policies.