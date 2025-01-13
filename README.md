# AI-Driven Database Workflow Automation

Harnessing the power of AI agents, this project demonstrates how artificial intelligence can redefine database management, particularly in ensuring data integrity, security, and consistency across workflows. Each AI agent specializes in a specific role, collectively ensuring a seamless, secure, and efficient pipeline from validation to migration, with actionable insights and advanced machine learning techniques.

---

## Table of Contents
- [Introduction](#introduction)
- [Core Features](#core-features)
- [Technologies Used](#technologies-used)
- [Architecture Overview](#architecture-overview)
- [Installation and Setup](#installation-and-setup)
- [How It Works](#how-it-works)
- [Agents and Their Responsibilities](#agents-and-their-responsibilities)
- [Workflow Phases](#workflow-phases)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

The increasing complexity of database management demands intelligent solutions to mitigate risks, validate data, and maintain schema consistency. This project introduces AI-driven agents as a robust data security layer, ensuring database integrity through advanced validations, schema consistency checks, and machine learning-powered anomaly detection. By modularizing workflows and assigning specialized responsibilities to AI agents, this system addresses critical challenges in database management with efficiency and precision.

---

## Core Features

- **AI-Driven Validation**: Replace manual validation processes with AI agents capable of executing SQL queries, analyzing schemas, and detecting data inconsistencies.
- **Machine Learning Integration**: Leverage Isolation Forest and other algorithms for real-time anomaly and outlier detection.
- **Automated Workflow Orchestration**: Modular workflows for landing zone creation, validation, migration, and machine learning checks.
- **Data Security**: Enforce strict integrity checks at every stage of the pipeline to prevent data corruption and unauthorized access.
- **Seamless Database Migration**: Effortlessly migrate validated data into new databases while maintaining schema fidelity.
- **Extensible Configuration**: YAML-driven configuration for defining tasks and agent responsibilities, allowing rapid customization.

---

## Technologies Used

- **Programming Language**: Python
- **Framework**: Chainlit
- **Database Interaction**: SQLAlchemy, MySQL
- **Machine Learning**: Scikit-learn (Isolation Forest)
- **LLM Integration**: OpenAI's GPT via Azure APIs

---

## Architecture Overview

```
project/
├── app/
│   ├── main.py           # Main workflow orchestration
│   ├── landing_zone.py   # Data landing zone pipeline
│   ├── newdb.py          # New database creation pipeline
│   ├── ml_checks.py      # Machine learning checks workflow
├── tools/                # Custom tools for validation and processing
├── config.py             # Core configuration (API keys, database URIs)
├── config.yaml           # Task descriptions and agent roles
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Installation and Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- Virtual Environment (recommended)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/ai-database-workflow.git
   cd ai-database-workflow
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database connection in `config.py`**:
   ```python
   DB_URI = "mysql+mysqlconnector://<username>:<password>@localhost/<database_name>"
   ```

5. **Set your API key for LLM integration**:
   ```bash
   export GROQ_API_KEY="your_api_key"
   ```

6. **Start the application**:
   ```bash
   chainlit run app/main.py --headless --port 8000
   ```

---

## How It Works

1. **Landing Zone Creation**:
   - Automatically exports all database tables to a secure landing zone for analysis.

2. **Schema and Data Validation**:
   - Prompts users for inputs and validates schema relationships and data integrity.

3. **Machine Learning-Based Checks**:
   - Detects outliers and inconsistencies in numerical data using Isolation Forest.

4. **Database Migration**:
   - Copies validated tables to a new database with schema fidelity.

5. **Dynamic Agent Collaboration**:
   - AI agents interact and combine functionalities to ensure a secure and validated pipeline.

---

## Agents and Their Responsibilities

1. **SQL Developer**:
   - Constructs and validates SQL queries.
   - Ensures compliance with schema integrity using provided metadata.

2. **Data Quality Specialist**:
   - Identifies anomalies, missing values, and duplicates.
   - Generates actionable reports for improving data reliability.

3. **Schema Validator**:
   - Checks for circular references, unused foreign keys, and orphaned rows.
   - Ensures schema relationships align with business rules.

4. **Machine Learning Validator**:
   - Detects outliers in numerical data using Isolation Forest.
   - Validates numerical trends for unexpected anomalies.

5. **Report Writer**:
   - Summarizes validation findings into structured, actionable reports.

6. **Database Migration Expert**:
   - Fixes schema and data issues.
   - Migrates data into a new database while ensuring compliance with integrity constraints.

---

## Workflow Phases

### Phase 1: **Data Landing Zone**
- Export all tables from the source database to CSV for inspection.
- Format and prepare data for validation workflows.

### Phase 2: **Schema and Data Validation**
- Validate schema relationships, keys, and structural consistency.
- Detect and report data issues like missing values and duplicates.

### Phase 3: **Machine Learning Checks**
- Use Isolation Forest to detect outliers in numerical columns.
- Validate numerical trends for unexpected anomalies.

### Phase 4: **New Database Migration**
- Create a new database and migrate validated data into it.
- Ensure schema fidelity and resolve any detected issues.

---

## Contributing

Contributions are welcome to make this project even more robust and scalable. Here's how you can contribute:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## Acknowledgments

- **OpenAI GPT via Azure APIs** for advanced natural language capabilities.
- **Scikit-learn** for machine learning-driven validation.
- **SQLAlchemy** for seamless database interaction.
- **Chainlit** for building intuitive AI workflows.

---

This project exemplifies how AI can transform database workflows, ensuring data integrity and security while minimizing human intervention.
