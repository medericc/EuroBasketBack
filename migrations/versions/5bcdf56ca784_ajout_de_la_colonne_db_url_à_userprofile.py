"""Ajout de la colonne db_url à UserProfile

Revision ID: 5bcdf56ca784
Revises: c6d5a3fa936e
Create Date: 2024-12-23 05:16:29.850066

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bcdf56ca784'
down_revision: Union[str, None] = 'c6d5a3fa936e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'event', 'players', ['player_id'], ['id'])
    op.create_foreign_key(None, 'game_stats', 'players', ['player_id'], ['id'])
    op.create_foreign_key(None, 'player_events', 'players', ['player_id'], ['id'])
    op.create_foreign_key(None, 'player_positions', 'players', ['player_id'], ['id'])
    op.create_foreign_key(None, 'player_stats', 'players', ['player_id'], ['id'])
    op.alter_column('players', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.alter_column('players', 'first_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('players', 'last_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('players', 'position',
               existing_type=sa.VARCHAR(length=2),
               nullable=False)
    op.alter_column('players', 'height',
               existing_type=sa.NUMERIC(precision=5, scale=2),
               nullable=False)
    op.alter_column('players', 'weight',
               existing_type=sa.NUMERIC(precision=5, scale=2),
               nullable=False)
    op.alter_column('players', 'birth_date',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('players', 'market_value',
               existing_type=sa.NUMERIC(precision=15, scale=2),
               nullable=False)
    op.create_foreign_key(None, 'players', 'teams', ['team_id'], ['id'])
    op.create_foreign_key(None, 'transfers', 'players', ['player_id'], ['id'])
    op.add_column('user_profile', sa.Column('db_url', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profile', 'db_url')
    op.drop_constraint(None, 'transfers', type_='foreignkey')
    op.drop_constraint(None, 'players', type_='foreignkey')
    op.alter_column('players', 'market_value',
               existing_type=sa.NUMERIC(precision=15, scale=2),
               nullable=True)
    op.alter_column('players', 'birth_date',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('players', 'weight',
               existing_type=sa.NUMERIC(precision=5, scale=2),
               nullable=True)
    op.alter_column('players', 'height',
               existing_type=sa.NUMERIC(precision=5, scale=2),
               nullable=True)
    op.alter_column('players', 'position',
               existing_type=sa.VARCHAR(length=2),
               nullable=True)
    op.alter_column('players', 'last_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('players', 'first_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('players', 'id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    op.drop_constraint(None, 'player_stats', type_='foreignkey')
    op.drop_constraint(None, 'player_positions', type_='foreignkey')
    op.drop_constraint(None, 'player_events', type_='foreignkey')
    op.drop_constraint(None, 'game_stats', type_='foreignkey')
    op.drop_constraint(None, 'event', type_='foreignkey')
    # ### end Alembic commands ###
