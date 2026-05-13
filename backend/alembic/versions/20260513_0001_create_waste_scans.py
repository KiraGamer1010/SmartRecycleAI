"""create waste scans table

Revision ID: 20260513_0001
Revises:
Create Date: 2026-05-13 13:10:00.000000
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260513_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "waste_scans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("material_type", sa.String(length=120), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("recyclable", sa.Boolean(), nullable=False),
        sa.Column("image_reference", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_waste_scans_id"), "waste_scans", ["id"], unique=False)
    op.create_index(
        op.f("ix_waste_scans_material_type"),
        "waste_scans",
        ["material_type"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_waste_scans_material_type"), table_name="waste_scans")
    op.drop_index(op.f("ix_waste_scans_id"), table_name="waste_scans")
    op.drop_table("waste_scans")
