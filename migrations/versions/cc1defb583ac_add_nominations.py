"""Add nominations

Revision ID: cc1defb583ac
Revises: 2654d1fab0a0
Create Date: 2023-12-03 11:58:46.454232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc1defb583ac'
down_revision: Union[str, None] = '2654d1fab0a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nominations',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('voting_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['voting_id'], ['votings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('nominations')
    # ### end Alembic commands ###
