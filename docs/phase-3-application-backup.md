# Phase 3: Application and Backup

## Objective

Deploy a small internal inventory API backed by PostgreSQL, then create and test a repeatable backup and restore procedure.

## Architecture

```text
Nginx :80
  → Gunicorn :8080 (localhost only)
    → Flask inventory API
      → PostgreSQL raitbyne_inventory
