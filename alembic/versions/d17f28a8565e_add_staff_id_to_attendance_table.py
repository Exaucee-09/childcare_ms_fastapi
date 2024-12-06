"""Add staff_id to attendance table

Revision ID: d17f28a8565e
Revises: 
Create Date: 2024-11-25 15:11:11.662376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd17f28a8565e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attendance', sa.Column('staff_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'attendance', 'staff', ['staff_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'attendance', type_='foreignkey')
    op.drop_column('attendance', 'staff_id')
    # ### end Alembic commands ###
