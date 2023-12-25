"""Add user unit

Revision ID: e5bcd2dc80de
Revises: 9f5a7abbe1fc
Create Date: 2023-12-24 00:08:30.544905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5bcd2dc80de'
down_revision: Union[str, None] = '9f5a7abbe1fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('unit', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'unit')
    # ### end Alembic commands ###