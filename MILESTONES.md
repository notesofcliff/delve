# Milestones

Each milestone after M0 is a tracer round: one thin, working, end-to-end
slice through all eight lanes (business logic, interface, data,
packaging, automation, tests, docs, security). Tracer code is kept, not
thrown away, once it lands. A milestone counts as reached only when every
lane reads `OK` for it in `PROJECT_STATUS.md`.

## M0 - Walking Skeleton (fixed)

Goal: connect all eight lanes end to end. The system does almost nothing
useful yet, but every lane is real and wired together - nothing here is a
mock or a placeholder that later needs replacing, just a thin version of
the real thing.

Definition of Done for M0:

- [ ] The system installs and runs; `--version` and `--help` (or their
      equivalents) work.
- [ ] CI builds the system and publishes `0.0.x`.
- [ ] One smoke test exists and runs in CI.
- [ ] A README exists.
- [ ] The data storage location is decided and documented - the storage
      itself can be a stub, but the decision can't be.
- [ ] Security floor is in place:
  - [ ] No secret is hardcoded; every secret loads from an environment
        variable or a secret store.
  - [ ] Dependencies are pinned.
  - [ ] CI runs one automated dependency-vulnerability scan.
  - [ ] Transport and TLS assumptions are stated somewhere findable.
  - [ ] `SECURITY.md` exists, with a reporting path and a first
        threat-model note.

## M1 - Security and Supply-Chain Baseline

Goal: make release artifacts verifiably secure and reproducible without
changing user-facing functionality.
Why this slice: it retires high-leverage risk (supply chain + CI trust)
before shipping additional feature work on top of unsigned/unscanned
artifacts.

| Lane | Target state at this milestone |
|------|--------------------------------|
| Business logic | No net-new features; only small compatibility updates needed for security tooling integration. |
| Interface | Existing UI/API/CLI behavior unchanged; security controls do not break ingress and auth flows. |
| Data | Existing migrations still apply cleanly; storage/TLS assumptions documented in one canonical place. |
| Packaging | Python and Node dependency inputs are pinned/locked; release artifacts include SBOM metadata. |
| Automation | CI runs dependency scan, secret scan, and SAST; release job blocks on critical findings. |
| Tests | Add at least one CI smoke test proving install -> migrate -> run -> basic endpoint access. |
| Docs | Add changelog and a release/security runbook section that explains new gates and failure handling. |
| Security | Root `SECURITY.md` exists with reporting path + initial threat model; artifact signing enabled in publish pipeline. |

Exit criteria: all eight lanes read `OK` for M1 in `PROJECT_STATUS.md`.

## M2 - Ingestion Reliability Tracer

Goal: harden one end-to-end ingestion path (shipper -> API ingress -> stored event -> searchable query result).
Why this slice: this is the core product value path, and hardening one path completely gives fast feedback on scale, correctness, and operability.

| Lane | Target state at this milestone |
|------|--------------------------------|
| Business logic | One ingestion path has explicit validation/error handling and deterministic behavior under malformed input. |
| Interface | Documented and testable ingress contract for that path (request shape, auth mode, response semantics). |
| Data | Add/adjust one migration (if needed) and index strategy to support reliable ingest/search for the selected path. |
| Packaging | Container/package versions for this slice are tagged and reproducible from CI outputs. |
| Automation | Add a scheduled integration check or canary flow for the chosen ingestion path. |
| Tests | Add end-to-end test that posts sample payload, verifies DB record(s), and confirms query API retrieval. |
| Docs | Add a focused how-to for operating this ingestion path in local and containerized deployments. |
| Security | Enforce issuer/audience checks and transport expectations for this path; add negative auth tests. |

Exit criteria: all eight lanes read `OK` for M2 in `PROJECT_STATUS.md`.

## M3 - Operability and Restore Confidence

Goal: prove Delve can be operated and recovered safely in production-like conditions.
Why this slice: backup/restore and runtime observability are common late-stage gaps; clearing them early reduces outage and recovery risk.

| Lane | Target state at this milestone |
|------|--------------------------------|
| Business logic | Critical workflows remain functional after backup/restore and restart cycles. |
| Interface | Health/ready behavior is documented and exposed consistently for operators and automation. |
| Data | Backup procedure and restore procedure are scripted, versioned, and validated against real project data. |
| Packaging | Release artifacts embed provenance/SBOM references in release notes or metadata. |
| Automation | CI or scheduled pipeline executes backup -> restore verification path and records outcome. |
| Tests | Add disaster-recovery integration test covering backup/restore of representative data. |
| Docs | Publish recovery runbook and operator checklist for monitoring, backup cadence, and restore validation. |
| Security | Backup artifacts have access controls/encryption expectations documented and validated in workflow. |

Exit criteria: all eight lanes read `OK` for M3 in `PROJECT_STATUS.md`.
