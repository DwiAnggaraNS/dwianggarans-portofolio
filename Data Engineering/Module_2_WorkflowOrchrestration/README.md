## Data Engineering Module 2: Workflow Orchestration with Apache Airflow 🚀

**Self-Learning Data Engineering Zoomcamp Project**  
*Based on DataTalks.Club Data Engineering Zoomcamp*

Advanced workflow orchestration project implementing ELT pipelines using Apache Airflow for NYC Taxi data processing. This project demonstrates both local PostgreSQL and cloud-native GCP data engineering workflows. 📊

## Learning Context 📚

**Original Course:** [DataTalks.Club Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)  
**Personal Repository:** [DE-Zoomcamp-DwiANS-2025](https://github.com/DwiAnggaraNS/DE-Zoomcamp-DwiANS-2025)  
**Learning Method:** Self-study through official documentation and community resources  
**Module Focus:** Workflow Orchestration with Apache Airflow

## Project Architecture 🏗️

### Infrastructure Overview
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Source   │    │     Airflow      │    │   Target DB     │
│  (NYC TLC API)  │───▶│  Orchestration   │───▶│ PostgreSQL/GCP  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Technology Stack
- **Orchestration**: Apache Airflow 2.10.4
- **Containerization**: Docker & Docker Compose
- **Data Processing**: Pandas, PyArrow
- **Local Storage**: PostgreSQL
- **Cloud Platform**: Google Cloud Platform (GCS + BigQuery)
- **Data Format**: CSV → Parquet conversion

## Core Projects / Functionalities 🎯

### 1. ELT to Local PostgreSQL (Yellow Taxi Data)

**File:** `data_ingestion_local.py`

**Tech Stack:**
- **Orchestration**: Apache Airflow (workflow management)
- **Data Download**: `requests` + `gzip` + `shutil` (download & unzip)
- **Data Processing**: `pandas` (chunked reading + datetime conversion)
- **Database**: `SQLAlchemy` + `to_sql` (PostgreSQL insertion)

**Pipeline Flow:**
1. **Download**: Fetch gzipped CSV from NYC TLC API
2. **Decompress**: Extract CSV from gzip archive
3. **Process**: Chunked reading (100K rows) with datetime parsing
4. **Load**: Insert into PostgreSQL using SQLAlchemy

**Target Database:**
- PostgreSQL provided by `database_ny_taxi/docker-compose-lesson1.yaml`
- **Connection**: Host/service name in DAG must match network/compose setup
- **Credentials**: `user=root, password=root, host=pgdatabase, port=5432, db=ny_taxi`

### 2. ELT to GCP - Cloud-Native Pipeline (Green Taxi Data)

**File:** `data_ingestion_gcp_green.py` (also `data_ingestion_gcp_yellow.py` for Yellow taxi)

**Tech Stack:**
- **Orchestration**: Apache Airflow with GCP providers
- **Data Download**: `requests` + `gzip` (file retrieval)
- **Format Conversion**: `PyArrow` (CSV → Parquet optimization)
- **Cloud Storage**: `GCSHook` (upload to Google Cloud Storage)
- **Data Warehouse**: `BigQueryInsertJobOperator` (table operations)
- **Cleanup**: `BashOperator` (temporary file removal)

**Advanced Pipeline Architecture:**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────────┐
│  Download   │───▶│   Convert   │───▶│   Upload    │───▶│   BigQuery   │
│ CSV.GZ Data │    │ CSV→Parquet │    │   to GCS    │    │  Processing  │
└─────────────┘    └─────────────┘    └─────────────┘    └──────────────┘
```

**Detailed Workflow:**
1. **Download Task**: Fetch monthly taxi data (CSV.GZ format)
2. **Format Conversion**: CSV → Parquet using PyArrow for optimization
3. **Cloud Upload**: Store Parquet files in GCS bucket (data lake)
4. **External Table**: Create BigQuery external table pointing to GCS
5. **Temp Table**: Create native BigQuery table with unique row IDs
6. **Final Merge**: MERGE operation to consolidated yearly table
7. **Cleanup**: Remove temporary local files

**Cloud Infrastructure Requirements:**
- **GCS Bucket**: `zoomcamp_datalake_tsm` (data lake storage)
- **BigQuery Dataset**: `airflow2025_de_zoomcamp_tsm` (data warehouse)
- **Service Account**: `google/credentials.json` accessible to container
- **Airflow Connection**: GCP connection configured (`gcp-airflow` conn_id)

## Docker Infrastructure 🐳

### Services Architecture
```yaml
# docker-compose.yaml structure
services:
  postgres:        # Airflow metadata database
  init-airflow:    # Database initialization & user setup
  scheduler:       # Airflow scheduler service
  webserver:       # Airflow UI (port 8080)
```

### Container Configuration
```dockerfile
# Dockerfile
FROM apache/airflow:2.10.4-python3.8
# Custom requirements installation
# GCP credentials mounting
```

### Dependencies
```bash
# requirements.txt
apache-airflow-providers-google  # GCP integration
pyarrow                         # Parquet processing
pandas                          # Data manipulation
sqlalchemy                      # Database ORM
psycopg2-binary                # PostgreSQL adapter
requests                       # HTTP client
```

## DAG Configuration Details 📅

### Local Pipeline DAG
- **DAG ID**: `yellow_taxi_ingestion`
- **Schedule**: Manual trigger
- **Data Source**: Yellow taxi trip records
- **Target**: Local PostgreSQL database

### GCP Pipeline DAGs
- **Green Taxi DAG ID**: `GCP_ingestion_green`
- **Yellow Taxi DAG ID**: `yellow_taxi_ingestion` (GCP version)
- **Schedule**: `"0 6 2 * *"` (2nd day of each month at 6 AM)
- **Date Range**: 2019-01-01 to 2019-12-31
- **Catchup**: Enabled for historical data processing
- **Max Active Runs**: 1 (prevent parallel execution)

### Advanced Features
- **Dynamic Templating**: Date-based file naming
- **Error Handling**: Configurable retries (up to 10)
- **Data Quality**: Unique row ID generation using MD5 hashing
- **Schema Management**: Proper data type handling (e.g., ehail_fee → FLOAT64)

## Setup Instructions 🛠️

### Prerequisites
- Docker & Docker Compose installed
- GCP account with enabled APIs (if using cloud pipeline)
- Service account credentials (for GCP features)

### Local Development Setup
```bash
# 1. Clone repository
git clone https://github.com/DwiAnggaraNS/DE-Zoomcamp-DwiANS-2025
cd DE-Zoomcamp-DwiANS-2025/Module_2_WorkflowOrchrestration/Airflow

# 2. Build and start services
docker-compose up --build

# 3. Access Airflow UI
# URL: http://localhost:8080
# Username: admin / Password: admin
# OR Username: airflow / Password: airflow
```

### GCP Configuration (Cloud Pipeline)
```bash
# 1. Place service account credentials
# File: ./google/credentials.json

# 2. Update GCP variables in DAGs
PROJECT_ID = "your-project-id"
BUCKET = "your-gcs-bucket"
BIGQUERY_DATASET = "your-dataset"

# 3. Configure Airflow GCP connection
# Conn ID: gcp-airflow
# Connection Type: Google Cloud
# Keyfile Path: /opt/airflow/google/credentials.json
```

## Pipeline Monitoring 📊

### Airflow UI Features
- **DAG View**: Visual pipeline representation
- **Task Logs**: Detailed execution logs
- **Gantt Chart**: Task duration analysis
- **Tree View**: Historical run overview

### Log Analysis
```bash
# Access logs directory structure
logs/
├── dag_id=GCP_ingestion_green/
│   ├── run_id=scheduled__2019-01-02T060000+0000/
│   │   ├── task_id=download/
│   │   ├── task_id=format_to_parquet/
│   │   ├── task_id=upload_to_gcs/
│   │   └── task_id=create_final_table/
```

## Data Quality & Schema 📋

### Green Taxi Schema
```sql
CREATE TABLE green_taxi_YYYY (
    unique_row_id BYTES,           -- MD5 hash for deduplication
    filename STRING,               -- Source file tracking
    VendorID INT64,
    lpep_pickup_datetime TIMESTAMP,
    lpep_dropoff_datetime TIMESTAMP,
    store_and_fwd_flag STRING,
    RatecodeID INT64,
    PULocationID INT64,
    DOLocationID INT64,
    passenger_count INT64,
    trip_distance FLOAT64,
    fare_amount FLOAT64,
    -- ... additional fare components
    payment_type INT64,
    trip_type INT64,
    congestion_surcharge FLOAT64
)
```

### Data Processing Features
- **Deduplication**: MD5-based unique row identification
- **Data Type Optimization**: Proper numeric type casting
- **Incremental Loading**: MERGE-based upsert operations
- **File Tracking**: Source filename preservation

## Learning Outcomes 🎓

### Technical Skills Gained
- **Workflow Orchestration**: Apache Airflow DAG development
- **Cloud Engineering**: GCP integration (GCS + BigQuery)
- **Data Pipeline Design**: ELT pattern implementation
- **Containerization**: Docker-based deployment
- **Data Formats**: CSV to Parquet optimization
- **Error Handling**: Retry mechanisms and monitoring

### Best Practices Implemented
- **Infrastructure as Code**: Docker Compose configuration
- **Data Quality**: Schema validation and deduplication
- **Monitoring**: Comprehensive logging and alerting
- **Scalability**: Chunked processing and parallel execution
- **Security**: Service account management

## Troubleshooting 🔧

### Common Issues & Solutions

#### 1. GCP Authentication
```bash
# Ensure credentials.json is properly mounted
docker-compose exec webserver ls -la /opt/airflow/google/
```

#### 2. Connection Errors
```bash
# Check Airflow connections
# Admin → Connections → gcp-airflow
```

#### 3. Memory Issues
```bash
# Adjust chunk size in pandas processing
chunksize=100000  # Reduce if needed
```

#### 4. BigQuery Permissions
```bash
# Ensure service account has:
# - BigQuery Data Editor
# - BigQuery Job User
# - Storage Object Admin
```

## Future Enhancements 🔮

- [ ] **Data Quality Tests**: Great Expectations integration
- [ ] **Monitoring**: Custom metrics and alerting
- [ ] **Scaling**: Kubernetes deployment
- [ ] **CI/CD**: Automated DAG testing and deployment
- [ ] **Data Catalog**: Metadata management system
- [ ] **Real-time Processing**: Stream processing integration

## Files Structure 📁

```
Module_2_WorkflowOrchrestration/
├── Airflow/
│   ├── docker-compose.yaml          # Infrastructure setup
│   ├── Dockerfile                   # Custom Airflow image
│   ├── requirements.txt             # Python dependencies
│   ├── dags/
│   │   ├── data_ingestion_local.py     # PostgreSQL pipeline
│   │   ├── data_ingestion_gcp_green.py # GCP Green taxi pipeline
│   │   └── data_ingestion_gcp_yellow.py # GCP Yellow taxi pipeline
│   ├── google/
│   │   └── credentials.json         # GCP service account key
│   └── logs/                        # Execution logs
```

## Learning Resources 📖

- **Primary**: [DataTalks.Club DE Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- **Documentation**: [Apache Airflow Docs](https://airflow.apache.org/docs/)
- **Community**: DataTalks.Club Slack workspace
- **Datasets**: [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

---

*This project demonstrates practical application of modern data engineering principles through self-directed learning, showcasing the ability to build production-ready data pipelines using industry-standard tools and cloud platforms.* ✨

## License 📄

Educational and Learning Purpose
