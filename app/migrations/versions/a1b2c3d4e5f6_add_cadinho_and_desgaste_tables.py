"""add_cadinho_and_desgaste_tables

Revision ID: a1b2c3d4e5f6
Revises: 98dc6b785c31
Create Date: 2026-07-26 09:30:00.000000

"""

import sqlalchemy as sa
import sqlmodel
from alembic import op

revision = "a1b2c3d4e5f6"
down_revision = "98dc6b785c31"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cadinho",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pirometro_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "codigo_identificador", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("espessura_inicial_mm", sa.Float(), nullable=False),
        sa.Column("espessura_atual_mm", sa.Float(), nullable=False),
        sa.Column("espessura_minima_seguranca_mm", sa.Float(), nullable=False),
        sa.Column("corridas_acumuladas", sa.Integer(), nullable=False),
        sa.Column("max_corridas_esperadas", sa.Integer(), nullable=True),
        sa.Column("data_instalacao", sa.DateTime(), nullable=False),
        sa.Column("data_substituicao", sa.DateTime(), nullable=True),
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("observacao", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["pirometro_id"],
            ["pirometro.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "registro_desgaste_cadinho",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cadinho_id", sa.Integer(), nullable=False),
        sa.Column("espessura_medida_mm", sa.Float(), nullable=False),
        sa.Column("corridas_no_momento", sa.Integer(), nullable=True),
        sa.Column("operador_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("observacao", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["cadinho_id"],
            ["cadinho.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("registro_desgaste_cadinho")
    op.drop_table("cadinho")
