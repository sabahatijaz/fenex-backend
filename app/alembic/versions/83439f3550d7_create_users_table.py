"""create users table

Revision ID: 83439f3550d7
Revises: fa27151f0217
Create Date: 2024-10-23 15:59:50.521606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83439f3550d7'
down_revision: Union[str, None] = 'fa27151f0217'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pivot_table', 'width',
               existing_type=sa.INTEGER(),
               type_=sa.Numeric(),
               existing_nullable=False)
    op.alter_column('pivot_table', 'height',
               existing_type=sa.INTEGER(),
               type_=sa.Numeric(),
               existing_nullable=False)
    op.alter_column('pivot_table', 'positive_pressure',
               existing_type=sa.INTEGER(),
               type_=sa.Numeric(),
               existing_nullable=False)
    op.alter_column('pivot_table', 'negative_pressure',
               existing_type=sa.INTEGER(),
               type_=sa.Numeric(),
               existing_nullable=False)
    op.create_index(op.f('ix_pivot_table_id'), 'pivot_table', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_pivot_table_id'), table_name='pivot_table')
    op.alter_column('pivot_table', 'negative_pressure',
               existing_type=sa.Numeric(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('pivot_table', 'positive_pressure',
               existing_type=sa.Numeric(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('pivot_table', 'height',
               existing_type=sa.Numeric(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('pivot_table', 'width',
               existing_type=sa.Numeric(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###