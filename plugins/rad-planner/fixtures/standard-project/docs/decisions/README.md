# Architecture Decision Records

This directory captures non-trivial architecture, tooling, scope, or interface decisions with their context, rationale, and consequences.

## How to read these

Each ADR is a single file: `NNNN-short-slug.md` where NNNN is sequential starting at 0001. Decisions are append-only — when a decision is superseded by a later one, the old ADR's status changes to `Superseded by NNNN` and the new ADR's body references the old one (`Supersedes 0007`).

## Index

- [0001 — Use TypeScript strict mode](./0001-use-typescript-strict.md)
