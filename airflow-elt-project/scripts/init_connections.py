#!/usr/bin/env python3
"""
Initialize Airflow connections from config/connections.yaml

This script reads the YAML configuration and creates/updates Airflow connections.
Run it after Airflow starts: `make init-connections`
"""

import os
import sys
import yaml
from airflow.models.connection import Connection
from airflow.settings import Session


def load_connections_config(config_path: str) -> dict:
    """Load connections configuration from YAML file."""
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config.get("connections", [])


def create_or_update_connection(session: Session, conn_config: dict) -> Connection:
    """Create or update an Airflow connection."""
    conn_id = conn_config["conn_id"]
    
    # Check if connection already exists
    existing = session.query(Connection).filter(Connection.conn_id == conn_id).first()
    
    if existing:
        print(f"Updating existing connection: {conn_id}")
        conn = existing
    else:
        print(f"Creating new connection: {conn_id}")
        conn = Connection(conn_id=conn_id)
    
    # Update connection fields
    conn.conn_type = conn_config.get("conn_type", "")
    conn.description = conn_config.get("description", "")
    conn.host = conn_config.get("host", "")
    conn.port = conn_config.get("port")
    conn.login = conn_config.get("login", "")
    conn.password = conn_config.get("password", "")
    conn.schema = conn_config.get("schema", "")
    
    # Handle extra fields (JSON)
    extra = conn_config.get("extra", {})
    if extra:
        import json
        conn.extra = json.dumps(extra)
    
    session.add(conn)
    return conn


def main():
    config_path = "/opt/airflow/config/connections.yaml"
    
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        sys.exit(1)
    
    connections = load_connections_config(config_path)
    
    session = Session()
    try:
        for conn_config in connections:
            create_or_update_connection(session, conn_config)
        session.commit()
        print(f"\nSuccessfully initialized {len(connections)} connection(s)")
    except Exception as e:
        session.rollback()
        print(f"Error initializing connections: {e}")
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()