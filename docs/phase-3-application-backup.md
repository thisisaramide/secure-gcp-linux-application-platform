# Phase 3: Application and Backup

## Objective

Deploy a small internal inventory API backed by PostgreSQL, then create and test a repeatable backup and restore procedure.

## Architecture

```text
Nginx :80
  → Gunicorn :8080 (localhost only)
    → Flask inventory API
      → PostgreSQL raitbyne_inventory
```

Public HTTP access was not enabled in the GCP firewall. Nginx and Gunicorn communicate only on the VM.

## Application

The Flask API provides:

- `GET /` — application information
- `GET /healthz` — health endpoint
- `GET /api/items` — list inventory items
- `POST /api/items` — create an inventory item

The application runs through a systemd service named:

```text
raitbyne-inventory.service
```

Gunicorn runs the application as the `secureway02` user and listens only on `127.0.0.1:8080`.

## Database

- Database: `raitbyne_inventory`
- Application role: `inventory_app`
- Table: `inventory_items`

The table stores an item ID, name, quantity, and creation timestamp.

Database credentials are stored only in:

```text
/etc/raitbyne-inventory.env
```

That file is owned by `root` with `600` permissions and is not committed to Git.

## Backup

The backup script is:

```text
/usr/local/sbin/raitbyne-inventory-backup
```

It creates PostgreSQL custom-format dumps in:

```text
/var/backups/raitbyne-inventory
```

The timer runs daily at 02:00 UTC:

```text
raitbyne-inventory-backup.timer
```

Backups older than seven days are removed.

## Restore Test

A restore script was created at:

```text
/usr/local/sbin/raitbyne-inventory-restore
```

The script refuses to restore over the live `raitbyne_inventory` database.

A backup was restored successfully into the separate database:

```text
raitbyne_inventory_restore_test
```

The restored database contained the `USB-C Adapter` test item with quantity `10`.

## Validation

- `raitbyne-inventory.service` is enabled and running.
- Nginx successfully proxies requests to the application.
- The API successfully created and listed inventory data.
- A timestamped PostgreSQL backup file was created.
- The backup was restored successfully into a separate test database.
