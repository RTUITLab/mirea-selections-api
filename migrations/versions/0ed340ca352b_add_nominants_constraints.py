"""Add nominants constraints

Revision ID: 0ed340ca352b
Revises: e02b25a1aa3d
Create Date: 2023-12-03 13:43:28.443294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ed340ca352b'
down_revision: Union[str, None] = 'e02b25a1aa3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('nominants_nomination_id_fkey', 'nominants', type_='foreignkey')
    op.create_foreign_key(None, 'nominants', 'nominations', ['nomination_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'nominants', type_='foreignkey')
    op.create_foreign_key('nominants_nomination_id_fkey', 'nominants', 'nominations', ['nomination_id'], ['id'])
    # ### end Alembic commands ###
