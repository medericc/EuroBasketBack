"""Fix relationships in Player and PlayerEvent

Revision ID: ee6ba6805452
Revises: f3a15cdcccd3
Create Date: 2024-12-19 16:55:58.375493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee6ba6805452'
down_revision: Union[str, None] = 'f3a15cdcccd3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###