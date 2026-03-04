# Sensor Data ETL Pipeline (Airflow + Docker + PostgreSQL)

This project demonstrates a production-ready **Data Engineering Pipeline** for processing IoT sensor data. It focuses on modular code design, automated testing, and robust CI/CD practices.



## 🚀 Overview

The pipeline ingests raw sensor data, performs cleaning (outlier removal and missing value imputation), and loads the result into a PostgreSQL database.

### Key Features:
* **Orchestration:** Apache Airflow handles the workflow scheduling.
* **Containerization:** Full stack runs on Docker (Airflow, Postgres).
* **Modular Transformation:** Business logic is decoupled from I/O for high testability.
* **Automated Testing:** Implemented **Unit**, **Integration**, and **Data Quality** tests using `pytest`.
* **CI/CD:** Integrated with **GitHub Actions** for automated testing on every push.

---

## 🛠 Tech Stack
* **Language:** Python 3.8+
* **Orchestrator:** Apache Airflow
* **Data Processing:** Pandas
* **Database:** PostgreSQL
* **Testing:** Pytest / SQLAlchemy
* **CI/CD:** GitHub Actions

---

## 🏗 Project Structure
```text
.
├── dags/
│   └── sensor_processing.py    # Main ETL logic & DAG definition
├── .github/workflows/
│   └── data_pipeline_ci.yml    # CI/CD configuration
├── docker-compose.yaml         # Local environment setup
├── test_pipeline.py            # Comprehensive test suite
├── init-db.sql                 # Database schema initialization
└── .gitignore                  # Git exclusion rules
```

## 🚦 Getting Started

### 1. Prerequisites
* **Docker & Docker Compose**
* **Python 3.8+**

### 2. Run Local Environment
To spin up the entire stack (Airflow, Postgres, etc.), run:
```bash
docker-compose up -d
```

Access Airflow UI at http://localhost:8080 (Default credentials: airflow/airflow).

### 3\. Running Tests

To run the full test suite locally:

```bash
pytest test_pipeline.py -v
```

🧪 Testing Strategy
-------------------

In this project, I implemented a three-tier testing strategy:

1.  **Unit Tests:** Validating the transformation logic (Outlier detection & Imputation) with mock data.
    
2.  **Integration Tests:** Ensuring successful connectivity between the Python application and the PostgreSQL container.
    
3.  **Data Quality Tests:** Running SQL-level assertions to verify the final table state in the database.
    

> **Note:** Integration and Quality tests are automatically skipped in the GitHub Actions environment to ensure a clean CI flow without database dependencies.

👨‍💻 Author
------------

**Tima**
