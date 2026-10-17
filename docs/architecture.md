# FastAPI architecture — Phase 0.4

```text
app/main.py             composition: create_app + FastAPI instance
app/api/health.py       active public liveness route (non-sensitive)
app/api/v1/             reserved private backend-facing contract routing
app/schemas/            Pydantic HTTP transport models
app/core/               typed settings, future security wiring
app/services/           approved use-case orchestration
app/models/             model/inference interface definitions
app/providers/          private AI and data-provider adapters
app/pipelines/          future embeddings/recommendations processing
app/utils/              pure reusable helpers
tests/unit/             pure unit tests
tests/integration/      future mocked contracts/infrastructure tests
scripts/                reviewed CLI utilities
```

## Dependencies and authority

HTTP routes validate and delegate to services. Services depend on provider interfaces defined in models; adapters in providers implement those interfaces. Pipelines are explicit jobs, never hidden import/startup side effects. Schemas are Pydantic wire contracts and do not redefine commerce schema.

There is no AI inference, remote model download, vector embedding or scraping in Phase 0.4. All training/product/user data use requires approved D03 privacy/consent/security and D04 contracts. NestJS remains authoritative for checkout, stock, ledger, payments, orders and identity. AI responses are **advisory** and cannot write commerce truth.

Do not interpret `/health` as a signal of model/service authorization or readiness.

Status: foundation / In Review; pending D01–D06 and owner sign-off.
