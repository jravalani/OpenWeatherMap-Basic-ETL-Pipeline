# OpenWeatherMap-Basic-ETL-Pipeline

## Overview

This project implements a basic ETL (Extract, Transform, Load) pipeline that collects weather information for a particular city using the OpenWeatherMap API. The pipeline transforms the JSON data into a Pandas dictionary and loads the resulting CSV file into an Amazon S3 bucket. The entire process is orchestrated using Apache Airflow with Directed Acyclic Graphs (DAGs) to ensure a smooth and automated workflow.

## Features

- **Data Extraction**: Utilizes the OpenWeatherMap API to gather real-time weather data for a specified city.
- **Data Transformation**: Converts the JSON data into a Pandas dictionary for easy manipulation and analysis.
- **Data Loading**: Uploads the transformed data in CSV format to an Amazon S3 bucket for storage and further accessibility.

## Prerequisites

Ensure you have the following components installed:

- [Amazon EC2](https://aws.amazon.com/ec2/) for hosting the project.
- [Apache Airflow](https://airflow.apache.org/) for orchestrating the ETL pipeline.


Great! Based on the commands you provided, here's an updated section for the README, including the setup and installation steps:

## Setup and Installation

### 1. Update and Install Dependencies

```bash
sudo apt update
sudo apt install python3-pip
sudo apt install python3.10-venv
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv env_name
source env_name/bin/activate
```

### 3. Install Required Python Packages

```bash
pip install pandas
pip install apache-airflow
pip install Flask-Session==0.5
```

### 4. Configure AWS CLI

Make sure you have your AWS credentials ready. Run the following command to configure AWS CLI:

```bash
aws configure
```

### 5. Start Apache Airflow

```bash
airflow standalone
```

Now, your environment is set up, and Apache Airflow is ready to use.

Make sure to replace `env_name` with your desired virtual environment name.

## Acknowledgments

- OpenWeatherMap for providing the weather data API.
- Apache Airflow for enabling efficient DAG orchestration.
