"""billing data model

Revision ID: b91acebfca48
Revises: 
Create Date: 2020-08-30 21:31:44.548322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import CheckConstraint

revision = 'b91acebfca48'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'clients',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('login', sa.String(256), unique=True, nullable=False),
        sa.Column('name', sa.String(256), nullable=False),
    )

    op.create_table(
        'wallets',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('client_id', sa.BigInteger, sa.ForeignKey('clients.id'), nullable=False),
        sa.Column('balance', sa.Numeric, nullable=False),
        CheckConstraint('balance >= 0', name='check_positive_balance')
    )

    op.create_table(
        'transactions',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('number', sa.String(36), nullable=False),
    )

    op.create_table(
        'wallets_operations',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('wallet_id', sa.BigInteger, sa.ForeignKey('wallets.id'), nullable=False),
        sa.Column('transaction_id', sa.BigInteger, sa.ForeignKey('transactions.id'), nullable=False),
        sa.Column('amount', sa.Numeric, nullable=False),
        sa.Column('operation_date', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table('wallets_operations')
    op.drop_table('transactions')
    op.drop_table('wallets')
    op.drop_table('clients')
