# Plan: AWS ELT Portfolio Project for Data Engineer and Analyst Applications

## TL;DR
Build a reproducible batch ELT pipeline that downloads data from a selected public Internet API or dataset, writes partitioned Parquet to Amazon S3, registers tables in the AWS Glue Data Catalog, and queries/transforms them with Athena and dbt. Run Airflow locally with Docker Compose to avoid managed-orchestration charges. Use uv for Python dependency management. Focus on one end-to-end pipeline, data quality, idempotency, cost controls, tests, and clear portfolio documentation rather than implementing every Airflow extension point.

---

## Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Public API  │────▶│     S3      │────▶│ Glue Catalog│────▶│ Athena/dbt  │
│  (Source)   │     │ Parquet lake│     │   (Tables)  │     │  Analytics  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                           ▲
                           │
                    ┌─────────────┐
                    │   Airflow   │
                    │ local Docker│
                    └─────────────┘
```

---

## Project Structure

```
airflow-elt-project/
├── docker-compose.yaml          # Local Airflow + Postgres
├── Dockerfile                   # Custom Airflow image with providers
├── pyproject.toml               # Project and dependency configuration
├── uv.lock                      # Reproducible dependency lock
├── config/
│   ├── airflow.cfg              # Airflow configuration
│   ├── connections.yaml         # Connection definitions (templated)
│   ├── variables.yaml           # Airflow variables
│   └── pipelines/               # Validated config for the selected pipeline
├── dags/
│   ├── __init__.py
│   └── elt_pipeline.py          # One clear, end-to-end batch pipeline
├── scripts/
│   ├── init_connections.py      # Initialize Airflow connections
│   ├── generate_sample_data.py  # Generate test CSV/JSON files
│   └── setup_aws.py             # Optional local AWS preflight checks
├── terraform/
│   ├── bootstrap/               # One-time remote Terraform state backend
│   ├── modules/data_lake/       # Reusable S3, Glue, Athena resources
│   └── environments/
│       ├── staging/             # Staging/preprod inputs and state key
│       └── production/          # Production inputs and state key
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures (Airflow DAG bag, etc.)
│   ├── unit/
│   │   └── test_pipeline.py
│   └── integration/
│       ├── test_dag_loading.py
│       └── test_elt_pipeline.py
├── data/
│   ├── sample/                  # Sample data files for testing
│   └── schemas/                 # JSON/Parquet schemas
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   └── contributing.md
├── .github/
│   └── workflows/
│       ├── ci.yaml              # Tests, lint, Terraform validation/plans
│       └── deploy.yaml          # Staging deploy and approved production promotion
├── .env.example                 # Environment variables template
├── Makefile                     # Common commands
└── README.md
```

---

## Implementation Phases

### Phase 1: Infrastructure & Foundation (Week 1)

#### Step 1.1: Docker Compose Setup
- **File**: `docker-compose.yaml`
- **Services**:
  - `postgres`: Airflow metadata DB (port 5432)
  - `airflow-webserver`: Airflow UI (port 8080)
  - `airflow-scheduler`: DAG scheduling
  - `airflow-init`: Database initialization
- **Networks**: `airflow-network`
- **Volumes**: Persistent storage for Postgres and Airflow logs
- AWS access: use a local AWS profile for development; never bake credentials into the image or commit them.

#### Step 1.2: Terraform-managed AWS resources
- Use Terraform to create environment-specific private S3 buckets, Glue databases/tables as appropriate, Athena workgroups and result locations, and narrowly scoped IAM permissions.
- Keep staging/preprod and production in the same AWS account for this low-cost portfolio, but isolate bucket names, Glue databases, Athena workgroups, IAM roles/policies, configuration, and Terraform state.
- Enable S3 public-access blocks, encryption, versioning for Terraform state, and lifecycle expiration for temporary/query results. Add production deletion protection where supported.
- Store Terraform state remotely in a dedicated, versioned, encrypted S3 bucket. Use a distinct state key per environment and S3 native lock files with a pinned modern Terraform version. Bootstrap the state bucket separately before normal environment applies.
- Pin the AWS provider and Terraform CLI versions, and commit Terraform dependency lock files.
- Never commit Terraform state, credentials, or real `.tfvars` files. Commit safe examples and pass environment-specific values through reviewed CI configuration.
- Scope each environment's deployment role to its state key and its own resources. Restrict GitHub's OIDC trust policy to this repository, protected branch, and intended GitHub Environment.

#### Step 1.3: Custom Airflow Docker Image
- **File**: `Dockerfile`
- **Base**: A currently supported Apache Airflow image version, pinned with compatible dependencies
- **Providers to install**:
  - `apache-airflow-providers-amazon` (S3, Glue, and Athena integrations)
  - `apache-airflow-providers-common-sql` as required by selected operators
  - `apache-airflow-providers-http`
  - dbt with the Athena adapter, if dbt is used
- **System deps**: `gcc`, `libpq-dev` for psycopg2

#### Step 1.4: Airflow Configuration
- **File**: `config/airflow.cfg`
- **Key settings**:
  - `executor = LocalExecutor` (or CeleryExecutor for scale demo)
  - `load_examples = False`
  - `dagbag_import_timeout = 60`
  - Logging to stdout for Docker

#### Step 1.5: Requirements & Environment
- **Files**: `pyproject.toml` and `uv.lock` - dependencies and reproducible lock
- **Commands**: `uv sync --locked` for development and CI; use the same lock in the Docker image
- Keep Airflow and provider versions compatible with the selected Airflow image and its constraints; validate the resolved environment before building.
- **File**: `.env.example` - template for secrets
- **File**: `Makefile` - common commands (up, down, logs, test, lint)

---

### Phase 2: Integrations (Week 1-2)

Prefer maintained Airflow provider integrations and TaskFlow tasks. Add custom plugins only when the project demonstrates a real reusable need.

#### Step 2.1: Source and AWS access
| Hook | Purpose | Key Methods |
|------|---------|-------------|
| HTTP client/provider | Fetch and paginate source data with timeouts and bounded retries |
| AWS provider hooks | S3, Glue, and Athena access | Use provider implementations; avoid duplicating their clients |

#### Step 2.2: Pipeline configuration
- Keep the initial pipeline configuration small and validate it at startup.
- Include source settings, S3 prefix, Parquet schema/partitioning, Glue database/table, and Athena workgroup.
- Do not add a dynamic DAG factory until there are multiple genuinely different pipelines to generate.

#### Step 2.3: Transformations
- Use dbt with the Athena adapter if its models and tests improve the project; otherwise use version-controlled SQL.
- Keep orchestration tasks thin and pass object paths or metadata through XCom, not large datasets.

---

### Phase 3: End-to-End Pipeline (Week 2)

Implement one idempotent pipeline with explicit extraction, S3 write, Glue catalog, Athena/dbt transform, and data-quality steps. Document how reruns handle the same data interval and how schema changes are detected.

---

### Phase 4: ELT Pipeline Implementation (Week 2-3)

#### Step 4.1: Extract Tasks (TaskFlow API)
- **Pattern**: `@task(retries=3, retry_delay=timedelta(minutes=2))`
- **Logic**:
  1. Call `ApiHook` for each endpoint
  2. Handle pagination (cursor, offset, page tokens)
  3. Write raw JSON and curated, partitioned Parquet to S3
  4. Return S3 object keys and basic counts/metadata (not the dataset itself)
  5. Emit `Dataset` event for raw data arrival

#### Step 4.2: Catalog and Query
- Register curated S3 datasets in the Glue Data Catalog using provider operators or explicit SQL/SDK calls.
- Query with Athena; use partition projection or partition registration appropriate to the chosen layout.
- Configure an Athena workgroup with a query result location, encryption, and a bytes-scanned limit.
- Keep S3 and Athena in the same AWS region. Use a dedicated, non-public bucket and least-privilege IAM permissions.

#### Step 4.3: Transform Tasks
- **Option A**: dbt with the Athena adapter for versioned models and tests
- **Option B**: SQL files executed with the Athena provider hook/operator
- **Pattern**: Models tagged by pipeline, select via `--select tag:pipeline_name`
- **Output**: Publish transformed datasets as `Dataset` outlets

#### Step 4.4: Data Quality Checks
- **Integrated**: dbt tests (unique, not_null, relationships)
- **Custom**: Great Expectations or Soda Core checks as separate tasks
- **Alerting**: Slack/email on failure via `on_failure_callback`

---

### Phase 5: Testing Strategy (Week 3)

#### Step 5.1: Unit Tests (`tests/unit/`)
| Target | Approach |
|--------|----------|
| Extraction/transform logic | Test pagination, schema handling, and data-quality rules |
| AWS tasks | Mock provider interactions; verify S3 paths, Glue/Athena parameters, and retries |
| DAG | Test import, task dependencies, and configuration validation |

**Fixtures** (`conftest.py`):
- `dag_bag`: Loaded DAGs for structure tests
- Moto for supported S3 unit tests; mock Glue/Athena provider interactions
- `sample_pipeline_config`: Validated pipeline config

#### Step 5.2: Integration Tests (`tests/integration/`)
- **DAG Loading**: `test_dag_loading.py` - verify all DAGs parse without errors
- **Task Execution**: `test_elt_pipeline.py` - run tasks with `DagRunner` or `TaskInstance`
- **Data Flow**: Optional end-to-end run against a small isolated AWS test bucket/database with strict query-scan limits; keep cloud integration out of default CI to avoid charges.

#### Step 5.3: CI/CD Pipeline
- **File**: `.github/workflows/ci.yaml`
- **Jobs**:
  - `lint`: ruff, mypy, hadolint (Dockerfile)
  - `unit-tests`: pytest unit with coverage
  - `integration-tests`: local tests by default; AWS tests opt-in and cost-limited
  - `dag-validation`: `airflow dags list-import-errors`
  - `terraform-check`: format, validate, and produce a plan for pull requests; do not apply on pull requests
  - `build`: package/version the pipeline artifact if deployment packaging is used

#### Step 5.4: Environment promotion and deployment
- Use GitHub Actions OpenID Connect (OIDC) to assume a narrowly scoped AWS deployment role; do not store long-lived AWS access keys in GitHub.
- Run static Terraform checks on all pull requests; only trusted workflow contexts may request AWS-backed plans. Never grant AWS credentials to untrusted fork pull requests.
- On merge to the protected default branch, deploy Terraform and pipeline configuration/artifacts to **staging/preprod** first.
- Promote the exact same commit/artifact to **production** only after successful staging validation and a required approval through a protected GitHub Environment. Do not rebuild a different artifact for production.
- Generate a separate Terraform plan for each environment because resource inputs and state differ, and require the production plan to be reviewed before apply.
- Pass the target environment explicitly; prevent concurrent applies to the same environment and retain apply logs. Treat saved Terraform plans as sensitive and restrict access and retention.
- Use separate deployment roles or tightly scoped role policies per environment. Limit production applies to the protected branch and approved workflow.
- Make rollback practical: retain versioned release artifacts and document how to revert a release and clean up resources safely.
- **Runtime boundary:** Airflow remains local in this cost-conscious plan. CI/CD provisions the AWS environments and publishes/promotes versioned SQL/dbt assets and configuration; Airflow is manually run against the selected environment. A continuously running production Airflow service is not included. Running the scheduled DAG in AWS would require a separately chosen and costed Airflow hosting option.

---

### Phase 6: Documentation & Polish (Week 3-4)

#### Step 6.1: Documentation
- **README.md**: Recruiter-friendly overview, architecture, demo screenshots/results, quickstart, costs, and limitations
- **docs/architecture.md**: Data flow, partitioning, schema evolution, IAM boundaries, and design decisions
- **docs/deployment.md**: Local Airflow setup and AWS resource setup/cleanup
- **docs/contributing.md**: Code style, testing, PR process

#### Step 6.2: Sample Data & Demo
- **Data**: Use a documented public dataset or API and include a tiny sanitized fixture for local tests
- **Demo**: Show the Airflow task graph, query/results, data-quality output, and cost-safety measures
- **Screenshots**: Airflow UI and Athena/analysis results, with credentials and sensitive identifiers removed

#### Step 6.3: Interview Talking Points
Document key decisions for interviews:
- Why ELT over ETL?
- Why S3 + Glue + Athena for this workload?
- How are retries, reruns, and duplicate data handled?
- How are partitions and schema changes managed?
- What controls keep AWS query and storage costs predictable?
- Testing strategy for data pipelines
- Handling schema evolution
- Idempotency and replayability

---

## Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| **TaskFlow API** | Clear task boundaries and testable orchestration |
| **Local Docker Compose Airflow** | Avoids managed-Airflow cost; AWS storage and queries can still incur charges |
| **S3 + Glue + Athena** | A coherent AWS-native lake, catalog, and query path |
| **Terraform** | Reproducible, reviewed AWS infrastructure with isolated staging/preprod and production configuration/state |
| **GitHub Actions OIDC** | Short-lived AWS credentials and gated staging-to-production promotion |
| **dbt for transforms** | Version-controlled SQL models and built-in data tests, if it fits the project |
| **AWS provider integrations** | Prefer maintained S3, Glue, and Athena integrations over unnecessary custom plugins |

---

## Scope Boundaries

### IN SCOPE
- ✅ A focused Airflow batch pipeline using TaskFlow
- ✅ Amazon S3 data lake with partitioned Parquet
- ✅ AWS Glue Data Catalog and Athena
- ✅ Terraform-managed AWS resources with staging/preprod and production environments
- ✅ GitHub Actions CI and gated environment promotion using OIDC
- ✅ dbt for transformations
- ✅ Comprehensive unit + integration tests
- ✅ Local Docker Compose Airflow with cost-controlled AWS integration

### OUT OF SCOPE
- ❌ Kubernetes deployment (Helm charts) - documented but not implemented
- ❌ Cloud managed Airflow (MWAA/Composer) - documented only
- ❌ Real-time streaming (Kafka/Flink) - batch ELT only
- ❌ Additional data catalog (DataHub, Amundsen) - Glue is the catalog for this project
- ❌ Advanced security (Kerberos, OAuth) - basic auth only
- ❌ Multi-tenancy - single team demo

---

## Verification Checklist

### Automated Verification
- [ ] `make up` starts local services healthy
- [ ] `make test-unit` passes with >80% coverage
- [ ] `make test-integration` passes (requires services)
- [ ] `make lint` passes (ruff, mypy, hadolint)
- [ ] Terraform formatting/validation succeeds and pull-request plans require no AWS credentials in source
- [ ] Staging deploy succeeds; production promotion requires approval and uses the same commit/artifact
- [ ] Environment IAM roles cannot write to the other environment's data paths
- [ ] `airflow dags list-import-errors` returns empty
- [ ] All DAGs parse and appear in UI

### Manual Verification
- [ ] Airflow UI accessible at localhost:8080
- [ ] Trigger DAG manually → completes successfully
- [ ] S3 objects follow the documented Parquet schema and partition layout
- [ ] Glue tables are queryable in Athena
- [ ] Athena workgroup scan limits and AWS cleanup steps are verified

### Interview Demo Script
1. Show project structure and architecture diagram
2. Run `make up` → services start in <2 min
3. Open Airflow UI → show the DAG and task graph
4. Trigger the pipeline → watch extraction, catalog, and transformation tasks
5. Show task logs and small XCom metadata values
6. Show the S3 object layout and Glue table metadata without exposing credentials or public bucket access
7. Run a small Athena query and show the dbt/SQL models and data-quality results
8. Run tests → show coverage report
9. Show Terraform plan and GitHub Actions staging deployment, then explain the production approval gate
10. Demonstrate AWS resource cleanup and cost-control settings

---

## Estimated Timeline

| Phase | Duration | Effort |
|-------|----------|--------|
| Phase 1: Local/AWS foundation and Terraform | 3-4 days | 12-16 hrs |
| Phase 2: Integrations and configuration | 2-3 days | 8-12 hrs |
| Phase 3: End-to-end pipeline | 3-4 days | 12-16 hrs |
| Phase 4: Tests, CI/CD promotion, and cost controls | 3-4 days | 12-16 hrs |
| Phase 5: Documentation and demo | 2-3 days | 8-12 hrs |
| **Total** | **3-4 weeks** | **52-72 hrs** |

---

## Next Steps

1. **Create new repository** from this plan
2. **Initialize with Phase 1** (Docker Compose, Dockerfile, config)
3. **Iterate through phases** - each phase is independently verifiable
4. **Push to GitHub** early for CI/CD feedback
5. **Record a short demo** for portfolio/LinkedIn (optional)

### Portfolio Accessibility
- Publish the source repository publicly with a recruiter-friendly README, architecture diagram, setup/cleanup instructions, and sample query/results.
- Include screenshots or a short demo video so reviewers can assess the work without AWS access or incurring query costs.
- Do not publish AWS credentials, state files, account identifiers, private data, or links granting access to the AWS console. Keep the S3 bucket private; reviewers should not need access to the live AWS account.
- Publish only Terraform examples and plans with sensitive values redacted; never publish state or environment secrets. Document that staging and production resources are separate and how deployments are gated.
- If hosting a dashboard, publish sanitized/sample outputs through an appropriate free hosting option. Do not expose Airflow, Athena credentials, or the bucket publicly.
- Add a license for the code and cite the source and license for any dataset.

### Cost Controls
- Set AWS Budgets alerts and configure S3 lifecycle expiration for demo data and Athena query results. Alerts notify; they do not cap spend.
- Use an Athena workgroup scan limit, run small queries, and avoid managed Airflow or always-on compute for this portfolio project.
- Keep staging data small and short-lived. Deploy resources only when needed and destroy temporary environments when finished; do not use automation that can destroy production data without an explicit review.
- Document which resources are billable and include cleanup commands/checklist.

---

## Resources & References

- [Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/)
- [TaskFlow API Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html)
- [Amazon Provider Documentation](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/)
- [Amazon Athena User Guide](https://docs.aws.amazon.com/athena/latest/ug/)
- [AWS Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [GitHub Actions OpenID Connect in AWS](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [Testing Airflow DAGs](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#testing)