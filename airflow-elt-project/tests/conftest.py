"""Pytest configuration and fixtures for Airflow tests."""

import os
import subprocess
import sys
import tempfile
import types
from pathlib import Path

import pytest

# fcntl is Unix-only; Airflow imports it via airflow.operators.python.
# On Windows, provide a stub so DAG loading can proceed in tests.
if os.name == "nt" and "fcntl" not in sys.modules:
    sys.modules["fcntl"] = types.ModuleType("fcntl")

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Create a temporary SQLite database for testing
TEST_DB_PATH = Path(tempfile.gettempdir()) / "airflow_test.db"

# Set Airflow home for testing
os.environ.setdefault("AIRFLOW_HOME", str(PROJECT_ROOT / "airflow_test_home"))
os.environ.setdefault("AIRFLOW__CORE__UNIT_TEST_MODE", "True")
os.environ.setdefault("AIRFLOW__CORE__LOAD_EXAMPLES", "False")
# Use as_posix() so SQLite URI uses forward slashes.
# Airflow requires 4 slashes for absolute paths (even on Windows).
_db_path = TEST_DB_PATH.as_posix()
os.environ.setdefault("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN", f"sqlite:////{_db_path}")



@pytest.fixture(scope="session")
def airflow_db():
    """Initialize the Airflow metadata database before DAG loading tests.

    Creates the required schema (e.g. the "dag" table) so that
    DagBag.get_dag() can query it on macOS, Linux, and Windows.
    """
    db_uri = f"sqlite:////{_db_path}"
    env = {**os.environ, "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN": db_uri}
    result = subprocess.run(
        ["airflow", "db", "init"],
        capture_output=True,
        text=True,
        env=env,
    )
    if result.returncode != 0:
        pytest.exit(f"airflow db init failed:\n{result.stderr}")
    yield

@pytest.fixture(scope="session")
def dag_bag(airflow_db):
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
    with open(config_path) as f:
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
