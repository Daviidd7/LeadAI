#!/usr/bin/env bash
set -euo pipefail

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
BACKUP_DIR="./backups"
mkdir -p "$BACKUP_DIR"

PGHOST=${PGHOST:-localhost}
PGPORT=${PGPORT:-5433}
PGUSER=${PGUSER:-postgres}
PGDATABASE=${PGDATABASE:-lead_qualifier}

pg_dump -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" "$PGDATABASE" > "$BACKUP_DIR/lead_qualifier_$TIMESTAMP.sql"

echo "Backup created at $BACKUP_DIR/lead_qualifier_$TIMESTAMP.sql"