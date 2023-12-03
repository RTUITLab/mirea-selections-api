"""Add votings

Revision ID: 2654d1fab0a0
Revises: 
Create Date: 2023-12-03 10:54:21.247569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2654d1fab0a0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('votings',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('creation_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('finish_date', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_permissions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('voting_id', sa.UUID(), nullable=False),
    sa.Column('permission', sa.Enum('ADMIN', 'VOTING_ADMIN', 'VOTING_ANALYTICS', 'VOTING_EDITOR', 'USER_ADMIN', 'USER_VIEWER', name='permissionnames'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['voting_id'], ['votings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_permissions')
    op.drop_table('votings')
    op.drop_table('users')
    # ### end Alembic commands ###