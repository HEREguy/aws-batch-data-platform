"""Pytest configuration and fixtures for Airflow tests."""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Create a temporary SQLite database for testing
TEST_DB_PATH = Path(tempfile.gettempdir()) / "airflow_test.db"

# Set Airflow home for testing
os.environ.setdefault("AIRFLOW_HOME", str(PROJECT_ROOT / "airflow_test_home"))
os.environ.setdefault("AIRFLOW__CORE__UNIT_TEST_MODE", "True")
os.environ.setdefault("AIRFLOW__CORE__LOAD_EXAMPLES", "False")
os.environ.setdefault("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN", f"sqlite:///{TEST_DB_PATH}")


@pytest.fixture(scope="session")
def dag_bag():
    """Load all DAGs for structure testing."""
    from airflow.models.dagbag import DagBag
    
    dag_folder = PROJECT_ROOT / "dags"
    dag_bag = DagBag(dag_folder=str(dag_folder), include_examples=False)
    return dag_bag


@pytest.fixture
def sample_pipeline_config():
    """Load sample pipeline configuration."""
    import yaml
    
    config_path = PROJECT_ROOT / "config" / "pipelines" / "sample_pipeline.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


@pytest.fixture
def mock_aws_credentials():
    """Mock AWS credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    yield
    # Cleanup
    for key in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SECURITY_TOKEN", "AWS_SESSION_TOKEN", "AWS_DEFAULT_REGION"]:
        os.environ.pop(key, None)