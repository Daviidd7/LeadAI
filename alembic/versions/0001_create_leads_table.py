from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_create_leads_table"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "leads",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, index=True),
        sa.Column("company", sa.String(length=255), nullable=True),
        sa.Column("website", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("budget", sa.String(length=255), nullable=True),
        sa.Column("timeline", sa.String(length=255), nullable=True),
        sa.Column("use_case", sa.Text(), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=True),
        sa.Column("ai_score", sa.Integer(), nullable=True),
        sa.Column("ai_priority", sa.String(length=20), nullable=True),
        sa.Column("ai_summary", sa.Text(), nullable=True),
        sa.Column("ai_disqualified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("ai_raw_response", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("crm_external_id", sa.String(length=255), nullable=True),
        sa.Column("crm_status", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="new"),
    )


def downgrade() -> None:
    op.drop_table("leads")