AI-Driven Database Workflow Automation

This project leverages AI agents to automate workflows involving database schema validation, data quality checks, machine learning-based outlier detection, and database migration tasks. It integrates tools for efficient data processing and validation while ensuring results are transparent and actionable.

Table of Contents

Introduction

Features

Technologies Used

Project Structure

Installation

Usage

Agents and Tasks

Workflow Steps

Contributing

License

Introduction

This project automates critical database workflows using a combination of AI tools and SQL. By employing advanced schema validation, data quality analysis, and machine learning techniques, it ensures that database operations are streamlined and error-free. The system is built to run in distinct modular steps for ease of integration and debugging.

Features

Data Landing Zone Creation: Export tables from a source database into a landing zone for further analysis.

Database Validation: Validate data and schema consistency with AI agents.

Machine Learning Checks: Use Isolation Forest for outlier detection and schema analysis.

Database Migration: Migrate first five rows from all tables into a new database with the same schema.

Flexible Configuration: YAML-based configuration for task descriptions and backstories, allowing modularity.

Technologies Used

Programming Language: Python

Framework: Chainlit

Database: MySQL

Machine Learning: Scikit-learn (Isolation Forest, DBSCAN)

ORM: SQLAlchemy

LLM Integration: OpenAI's GPT via Azure

Project Structure

project/
├── app/
│   ├── main.py           # Main workflow logic
│   ├── landing_zone.py   # Data landing zone workflow
│   ├── newdb.py          # New database creation workflow
│   ├── ml_checks.py      # Machine learning checks workflow
├── tools/                # Custom tools for tasks
├── config.py             # Configuration file
├── config.yaml           # Task descriptions and agent backstories
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

Installation

Prerequisites

Python 3.8+

MySQL Server

Virtual Environment (optional but recommended)

Steps

Clone the repository:

git clone https://github.com/your-repo/ai-database-workflow.git
cd ai-database-workflow

Set up a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Configure the database connection in config.py:

DB_URI = "mysql+mysqlconnector://<username>:<password>@localhost/<database_name>"

Set your Azure/OpenAI API key in an environment variable:

export GROQ_API_KEY="your_api_key"

Usage

Running the Application

Start the Chainlit server:

chainlit run app/main.py

Interact with the workflows through the Chainlit interface.

Workflows

Data Landing Zone: Automatically triggered to export tables into a CSV-based landing zone.

Database Validation: Prompts the user to define actions for schema and data validation.

New Database Creation: Automatically migrates validated data into a new database.

ML Checks: Runs after validation to detect outliers using Isolation Forest.

Agents and Tasks

Agents

SQL Developer: Constructs and validates SQL queries.

Data Validator: Detects anomalies and inconsistencies in data.

Schema Validator: Ensures schema relationships are logical and consistent.

Report Writer: Summarizes validation findings.

Database Expert: Fixes database issues and creates a new database.

Prompt Modifier: Aligns validation tasks with user-provided schema updates.

Tasks

Generate SQL queries.

Validate schema for issues like circular references.

Run machine learning-based checks for outlier detection.

Save results in a structured format.

Workflow Steps

Step 1: Data Landing Zone

Exports all tables from the source database to CSV files.

Step 2: Validation Workflow

Prompts for user input and validates database schema and data.

Step 3: New Database Workflow

Creates a new database and copies validated tables into it.

Step 4: Machine Learning Checks

Detects outliers and validates schema relationships using advanced algorithms.

Contributing

Contributions are welcome! Please follow these steps:

Fork the repository.

Create a feature branch: git checkout -b feature-name

Commit your changes: git commit -m 'Add some feature'

Push to the branch: git push origin feature-name

Open a Pull Request.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments

OpenAI and Azure GPT for advanced natural language understanding.

Scikit-learn for ML-based data validation.

SQLAlchemy for database interactions.
