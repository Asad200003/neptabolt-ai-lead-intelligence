# GitHub Backlog & Risk Assessment Matrix

## GitHub Issues Tracker (Week 1 - Week 4)

| Issue ID | Priority | Title | Status |
| :--- | :--- | :--- | :--- |
| NBLI-001 | P0 | Confirm product workflow, scope, and initial ICPs | COMPLETED |
| NBLI-002 | P0 | Research candidate data sources and authorization compliance | COMPLETED |
| NBLI-003 | P0 | Approve architecture, DB schemas, and API contracts | COMPLETED |
| NBLI-004 | P0 | Create monorepo structure, Docker configuration, and CI pipeline | COMPLETED |
| NBLI-005 | P0 | Define ICP database models and initial migrations | COMPLETED |
| NBLI-008 | P0 | Implement CSV import and Deterministic Mock Connector | COMPLETED |
| NBLI-009 | P0 | Implement Discovery Job lifecycle tracking APIs | COMPLETED |
| NBLI-013 | P0 | Build LLM abstraction layer for AI enrichment (Week 2) | PLANNED |
| NBLI-015 | P0 | Implement Explainable Lead Scoring Engine (Week 2) | PLANNED |
| NBLI-020 | P0 | Next.js Frontend Dashboard Implementation (Week 3) | PLANNED |

## Project Risk & Dependency Matrix

1. **Risk: External Source Rate Limits & Paywalls**
   * **Mitigation**: Implement exponential backoff retries, CSV import fallback, and deterministic mock fallback. Never bypass access controls.
2. **Risk: AI Hallucinations in Lead Facts**
   * **Mitigation**: Require strict evidence citations and source provenance for every extracted fact.
3. **Risk: Duplicate Lead Entity Creation**
   * **Mitigation**: Conservative domain matching with manual review flagging for uncertain matches.