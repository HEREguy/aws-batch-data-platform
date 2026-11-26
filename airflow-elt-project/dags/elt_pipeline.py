"""
ELT Pipeline DAG
Extracts data from a public API, loads to S3/Glue, transforms with dbt/Athena.
"""

from datetime import datetime, timedelta
from io import BytesIO

import pandas as pd  # type: ignore[import-untyped]
import yaml
from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.http.hooks.http import HttpHook
from botocore.exceptions import ClientError


# Load pipeline configuration
def load_pipeline_config():
    """Load and validate pipeline configuration."""
    config_path = "/opt/airflow/config/pipelines/sample_pipeline.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


# DAG-level constants (used only for DAG definition at import time;
# pipeline config is loaded lazily inside each task to avoid failing
# DAG parsing when the config file is unavailable)
PIPELINE_NAME = "sample_elt_pipeline"
PIPELINE_DESCRIPTION = "Extract from public API, load to S3/Glue, transform with dbt/Athena"
PIPELINE_SCHEDULE = "@daily"
PIPELINE_START_DATE = "2024-01-01"
PIPELINE_CATCHUP = False
PIPELINE_MAX_ACTIVE_RUNS = 1
PIPELINE_TAGS = ["elt", "portfolio", "aws"]

# Default arguments for the DAG
default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
    "email_on_retry": False,
}

with DAG(
    dag_id=PIPELINE_NAME,
    description=PIPELINE_DESCRIPTION,
    schedule_interval=PIPELINE_SCHEDULE,
    start_date=datetime.fromisoformat(PIPELINE_START_DATE),
    catchup=PIPELINE_CATCHUP,
    max_active_runs=PIPELINE_MAX_ACTIVE_RUNS,
    default_args=default_args,
    tags=PIPELINE_TAGS,
    doc_md=__doc__,
) as dag:

    @task(retries=3, retry_delay=timedelta(minutes=2))
    def extract_data(**context):
        """
        Extract data from the source API with pagination.
        Returns metadata about extracted data (not the data itself).
        """
        config = load_pipeline_config()
        source_config = config["source"]
        http_hook = HttpHook(
            method=source_config["method"],
            http_conn_id=source_config["connection_id"],
        )

        pagination = source_config["pagination"]
        all_records = []
        page = 0
        max_pages = pagination.get("max_pages", 10)

        while page < max_pages:
            params = dict(source_config.get("params", {}))

            if pagination["type"] == "offset":
                params[pagination["limit_param"]] = pagination["default_limit"]
                params[pagination["offset_param"]] = page * pagination["default_limit"]

            response = http_hook.run(
                endpoint=source_config["endpoint"],
                data=params,
                headers=source_config.get("headers", {}),
            )

            if response.status_code != 200:
                raise Exception(f"API request failed: {response.status_code} - {response.text}")

            data = response.json()
            records = data.get("data", [])

            if not records:
                break

            all_records.extend(records)
            page += 1

            # Check if there are more pages
            if pagination["type"] == "offset" and len(records) < pagination["default_limit"]:
                break

        # Write raw data to S3
        execution_date = context["ds"]
        raw_bucket = Variable.get("s3_raw_bucket")
        config = load_pipeline_config()
        raw_prefix = config["destination"]["s3"]["raw_prefix"].replace("{{ pipeline.name }}", PIPELINE_NAME).replace("{{ ds }}", execution_date)

        s3_hook = S3Hook(aws_conn_id="aws_default")

        # Convert to DataFrame and write as Parquet
        df = pd.DataFrame(all_records)
        if not df.empty:
            # Add partition columns
            dt = datetime.fromisoformat(execution_date)
            df["year"] = dt.year
            df["month"] = dt.month
            df["day"] = dt.day

            buffer = BytesIO()
            df.to_parquet(buffer, compression="snappy", index=False)
            buffer.seek(0)

            key = f"{raw_prefix}data.parquet"
            s3_hook.load_bytes(
                bytes_data=buffer.getvalue(),
                key=key,
                bucket_name=raw_bucket,
                replace=True,
            )

        return {
            "record_count": len(all_records),
            "raw_s3_key": f"s3://{raw_bucket}/{raw_prefix}data.parquet",
            "execution_date": execution_date,
        }

    @task
    def register_glue_table(extract_metadata, **context):
        """
        Register the curated data in AWS Glue Data Catalog.
        """
        from airflow.providers.amazon.aws.hooks.glue import GlueHook

        config = load_pipeline_config()
        glue_hook = GlueHook(aws_conn_id="aws_default")
        database = Variable.get("glue_database_staging")
        table_name = PIPELINE_NAME
        curated_bucket = Variable.get("s3_curated_bucket")
        curated_prefix = config["destination"]["s3"]["curated_prefix"].replace("{{ pipeline.name }}", PIPELINE_NAME)

        # For now, we'll create the table pointing to the curated location
        # In practice, this would run after the transform step
        table_input = {
            "Name": table_name,
            "StorageDescriptor": {
                "Location": f"s3://{curated_bucket}/{curated_prefix}",
                "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
                "OutputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
                "SerdeInfo": {
                    "SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe",
                },
                "Columns": [
                    {"Name": "id", "Type": "string"},
                    {"Name": "timestamp", "Type": "timestamp"},
                    {"Name": "value", "Type": "double"},
                    {"Name": "category", "Type": "string"},
                    {"Name": "year", "Type": "int"},
                    {"Name": "month", "Type": "int"},
                    {"Name": "day", "Type": "int"},
                ],
            },
            "PartitionKeys": [
                {"Name": "year", "Type": "int"},
                {"Name": "month", "Type": "int"},
                {"Name": "day", "Type": "int"},
            ],
            "TableType": "EXTERNAL_TABLE",
            "Parameters": {
                "classification": "parquet",
                "compressionType": "snappy",
            },
        }

        # Create database if not exists
        try:
            glue_hook.get_database(database)
        except ClientError as e:
            if e.response["Error"]["Code"] == "EntityNotFoundException":
                glue_hook.create_database({"Name": database})
            else:
                raise

        # Create or update table
        try:
            glue_hook.get_table(database, table_name)
            glue_hook.update_table(database, table_input)
        except ClientError as e:
            if e.response["Error"]["Code"] == "EntityNotFoundException":
                glue_hook.create_table(database, table_input)
            else:
                raise

        return {"database": database, "table": table_name}

    @task
    def transform_with_dbt(extract_metadata, **context):
        """
        Run dbt models to transform the data.
        """
        raise NotImplementedError(
            "dbt/Athena transform not yet implemented."
            "This task is a placeholder until Phase 2/3 integration is completed."
        )

    @task
    def data_quality_checks(extract_metadata, **context):
        """
        Run data quality checks on the transformed data.
        """
        raise NotImplementedError(
            "Data quality checks not yet implemented."
            "This task is a placeholder until Phase 3 integration is completed."
        )

    # Task dependencies
    extract_metadata = extract_data()
    glue_metadata = register_glue_table(extract_metadata)
    transform_result = transform_with_dbt(extract_metadata)
    dq_result = data_quality_checks(extract_metadata)

    # Set dependencies
    extract_metadata >> glue_metadata >> transform_result >> dq_result
