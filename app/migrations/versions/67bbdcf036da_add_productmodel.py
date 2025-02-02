"""Add ProductModel and Drop SellerModel, UserModel

Revision ID: 67bbdcf036da
Revises: 38a9301a499a
Create Date: 2024-09-28 15:47:11.911444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67bbdcf036da'
down_revision = '38a9301a499a'
branch_labels = None
depends_on = None


def upgrade():
    # Drop sellers, users, and products tables if they exist
    if op.get_bind().dialect.has_table(op.get_bind(), 'sellers'):
        op.drop_table('sellers')

    if op.get_bind().dialect.has_table(op.get_bind(), 'users'):
        op.drop_table('users')

    if op.get_bind().dialect.has_table(op.get_bind(), 'products'):
        op.drop_table('products')

    # Recreate products table
    op.create_table('products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)


def downgrade():
    # Drop the products table
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    
    # Recreate sellers and users tables if they were dropped
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
    )
    
    op.create_table('sellers',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
    )
