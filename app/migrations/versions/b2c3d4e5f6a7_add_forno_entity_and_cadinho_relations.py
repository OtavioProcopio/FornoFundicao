"""add_forno_entity_and_cadinho_relations

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-07-26 11:18:00.000000

"""

import sqlalchemy as sa
import sqlmodel
from alembic import op

revision = "b2c3d4e5f6a7"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "forno",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "codigo_identificador", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("setor", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("capacidade_kg", sa.Float(), nullable=True),
        sa.Column("tipo_liga", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("max_cadinhos", sa.Integer(), nullable=False, server_default="4"),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("observacao", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("codigo_identificador"),
    )

    with op.batch_alter_table("pirometro") as batch_op:
        batch_op.add_column(sa.Column("forno_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key("fk_pirometro_forno", "forno", ["forno_id"], ["id"])

    with op.batch_alter_table("cadinho") as batch_op:
        batch_op.add_column(sa.Column("forno_id", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("posicao_no_forno", sa.Integer(), nullable=True))
        batch_op.alter_column("pirometro_id", existing_type=sa.String(), nullable=True)
        batch_op.create_foreign_key("fk_cadinho_forno", "forno", ["forno_id"], ["id"])


def downgrade() -> None:
    with op.batch_alter_table("cadinho") as batch_op:
        batch_op.drop_constraint("fk_cadinho_forno", type_="foreignkey")
        batch_op.drop_column("posicao_no_forno")
        batch_op.drop_column("forno_id")

    with op.batch_alter_table("pirometro") as batch_op:
        batch_op.drop_constraint("fk_pirometro_forno", type_="foreignkey")
        batch_op.drop_column("forno_id")

    op.drop_table("forno")
