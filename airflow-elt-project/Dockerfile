# Custom Airflow image with AWS providers and dbt-athena
# Base image: pinned Airflow version with Python 3.11
FROM apache/airflow:2.9.1-python3.11

# Switch to root to install system dependencies
USER root

# Install system dependencies for psycopg2 and other compiled packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Install Airflow providers and dbt-athena
# Using constraints from the base image to ensure compatibility
RUN pip install --no-cache-dir \
    "apache-airflow-providers-amazon==8.16.0" \
    "apache-airflow-providers-common-sql==1.7.0" \
    "apache-airflow-providers-http==4.8.0" \
    "dbt-athena-community==1.8.1" \
    "dbt-core==1.8.0"

# Set Airflow home (already set in base image, but explicit for clarity)
ENV AIRFLOW_HOME=/opt/airflow