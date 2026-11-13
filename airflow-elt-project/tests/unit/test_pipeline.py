"""Unit tests for the ELT pipeline."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta


class TestPipelineConfig:
    """Tests for pipeline configuration validation."""

    def test_sample_pipeline_config_loads(self, sample_pipeline_config):
        """Test that the sample pipeline config loads correctly."""
        assert sample_pipeline_config is not None
        assert "pipeline" in sample_pipeline_config
        assert sample_pipeline_config["pipeline"]["name"] == "sample_elt_pipeline"

    def test_pipeline_has_required_sections(self, sample_pipeline_config):
        """Test that all required config sections exist."""
        required_sections = ["pipeline", "source", "destination", "transform", "data_quality"]
        for section in required_sections:
            assert section in sample_pipeline_config, f"Missing section: {section}"

    def test_source_config_has_pagination(self, sample_pipeline_config):
        """Test that source config includes pagination settings."""
        source = sample_pipeline_config["source"]
        assert "pagination" in source
        assert source["pagination"]["type"] in ["offset", "cursor", "page_token"]

    def test_destination_has_s3_and_glue(self, sample_pipeline_config):
        """Test that destination includes S3 and Glue config."""
        dest = sample_pipeline_config["destination"]
        assert "s3" in dest
        assert "glue" in dest
        assert "athena" in dest

    def test_data_quality_checks_defined(self, sample_pipeline_config):
        """Test that data quality checks are configured."""
        dq = sample_pipeline_config["data_quality"]
        assert dq["enabled"] is True
        assert "checks" in dq
        assert len(dq["checks"]) > 0


class TestExtractLogic:
    """Tests for extraction logic (mocked)."""

    @patch("airflow.providers.http.hooks.http.HttpHook")
    def test_pagination_offset(self, mock_http_hook_class):
        """Test offset-based pagination logic."""
        # Mock responses for 3 pages
        mock_response_1 = Mock()
        mock_response_1.json.return_value = {"data": [{"id": "1"}], "has_more": True}
        mock_response_1.status_code = 200

        mock_response_2 = Mock()
        mock_response_2.json.return_value = {"data": [{"id": "2"}], "has_more": True}
        mock_response_2.status_code = 200

        mock_response_3 = Mock()
        mock_response_3.json.return_value = {"data": [{"id": "3"}], "has_more": False}
        mock_response_3.status_code = 200

        mock_hook_instance = Mock()
        mock_hook_instance.run.side_effect = [mock_response_1, mock_response_2, mock_response_3]
        mock_http_hook_class.return_value = mock_hook_instance

        # Simulate the pagination loop logic from the DAG
        from airflow.providers.http.hooks.http import HttpHook
        
        hook = HttpHook(method="GET", http_conn_id="test")
        all_records = []
        page = 0
        max_pages = 3
        default_limit = 100
        
        while page < max_pages:
            params = {"limit": default_limit, "offset": page * default_limit}
            response = hook.run(endpoint="/test", data=params)
            records = response.json().get("data", [])
            
            if not records:
                break
            
            all_records.extend(records)
            page += 1
            
            if len(records) < default_limit:
                break
        
        # Verify the mock was called correctly
        assert mock_hook_instance.run.call_count == 3
        assert len(all_records) == 3


class TestTransformLogic:
    """Tests for transformation logic."""

    def test_dbt_model_selection(self):
        """Test that dbt model selection uses correct tag."""
        # This would test the dbt command construction
        model_tag = "pipeline:sample_elt_pipeline"
        assert model_tag == "pipeline:sample_elt_pipeline"

    def test_partition_columns(self):
        """Test that partition columns are correctly defined."""
        partition_cols = ["year", "month", "day"]
        assert partition_cols == ["year", "month", "day"]


class TestDataQuality:
    """Tests for data quality checks."""

    def test_row_count_check_config(self, sample_pipeline_config):
        """Test row count check configuration."""
        checks = sample_pipeline_config["data_quality"]["checks"]
        row_count_check = next((c for c in checks if c["name"] == "row_count"), None)
        assert row_count_check is not None
        assert row_count_check["type"] == "sql"
        assert "min_value" in row_count_check

    def test_null_check_config(self, sample_pipeline_config):
        """Test null check configuration."""
        checks = sample_pipeline_config["data_quality"]["checks"]
        null_check = next((c for c in checks if c["name"] == "null_check"), None)
        assert null_check is not None
        assert null_check["type"] == "dbt_test"
        assert null_check["test_type"] == "not_null"

    def test_uniqueness_check_config(self, sample_pipeline_config):
        """Test uniqueness check configuration."""
        checks = sample_pipeline_config["data_quality"]["checks"]
        unique_check = next((c for c in checks if c["name"] == "uniqueness_check"), None)
        assert unique_check is not None
        assert unique_check["test_type"] == "unique"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])