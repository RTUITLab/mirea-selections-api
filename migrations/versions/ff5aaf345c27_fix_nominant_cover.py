"""Fix nominant cover

Revision ID: ff5aaf345c27
Revises: 0ed340ca352b
Create Date: 2023-12-03 14:30:03.840402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff5aaf345c27'
down_revision: Union[str, None] = '0ed340ca352b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nominants', sa.Column('cover_url', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('nominants', 'cover_url')
    # ### end Alembic commands ###
