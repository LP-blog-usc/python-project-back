"""create credit accounts and purchases tables

Revision ID: daa8bd1f00ba
Revises: 0599aefe54a8
Create Date: 2024-11-11 21:52:01.516331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'daa8bd1f00ba'
down_revision: Union[str, None] = '0599aefe54a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('credit_accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_name', sa.String(length=100), nullable=False),
    sa.Column('total_credit', sa.Float(), nullable=False),
    sa.Column('pending_balance', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_credit_accounts_id'), 'credit_accounts', ['id'], unique=False)
    op.create_table('credit_purchases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['credit_accounts.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_credit_purchases_id'), 'credit_purchases', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_credit_purchases_id'), table_name='credit_purchases')
    op.drop_table('credit_purchases')
    op.drop_index(op.f('ix_credit_accounts_id'), table_name='credit_accounts')
    op.drop_table('credit_accounts')
    # ### end Alembic commands ###
