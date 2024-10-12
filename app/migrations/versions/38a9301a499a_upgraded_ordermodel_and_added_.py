"""Upgraded OrderModel and added ProductModel, VendorModel and UserModel

Revision ID: 38a9301a499a
Revises: 6400839a219d
Create Date: 2024-09-28 13:36:05.541499

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '38a9301a499a'
down_revision = '6400839a219d'
branch_labels = None
depends_on = None


def upgrade():
    # Check if 'products' table exists, and create it if not
    if not op.get_bind().dialect.has_table(op.get_bind(), 'products'):
        op.create_table('products',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('description', sa.String(), nullable=True),
            sa.Column('price', sa.Float(), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)

    # Check if 'users' table exists, and create it if not
    if not op.get_bind().dialect.has_table(op.get_bind(), 'users'):
        op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
        )
        op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Check if 'vendors' table exists, and create it if not
    if not op.get_bind().dialect.has_table(op.get_bind(), 'vendors'):
        op.create_table('vendors',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('description', sa.String(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_vendors_id'), 'vendors', ['id'], unique=False)

    # Step 1: Add fulfillment_source_id and fulfillment_source_type as nullable
    op.add_column('orders', sa.Column('fulfillment_source_id', sa.Integer(), nullable=True))
    op.add_column('orders', sa.Column('fulfillment_source_type', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('is_backup_fulfillment', sa.Integer(), nullable=True))

    # Step 2: Write a data migration to set default values for existing rows
    # For example, setting 'fulfillment_source_type' to 'default' where NULL
    op.execute("UPDATE orders SET fulfillment_source_type = 'default' WHERE fulfillment_source_type IS NULL")
    op.execute("UPDATE orders SET fulfillment_source_id = 1 WHERE fulfillment_source_id IS NULL")

    # Step 3: Alter the columns to make them NOT NULL after updating data
    op.alter_column('orders', 'fulfillment_source_id', nullable=False)
    op.alter_column('orders', 'fulfillment_source_type', nullable=False)

    # Step 4: Create the 'orderstatusenum' type
    order_status_enum = postgresql.ENUM('PENDING', 'SHIPPED', 'DELIVERED', 'FAILED', name='orderstatusenum')
    order_status_enum.create(op.get_bind(), checkfirst=True)

    # Step 5: Alter the 'tracking_status' column to use 'orderstatusenum' with explicit casting
    op.execute("ALTER TABLE orders ALTER COLUMN tracking_status TYPE orderstatusenum USING tracking_status::orderstatusenum")

    # Foreign key constraints
    op.create_foreign_key(None, 'orders', 'products', ['product_id'], ['id'])
    op.create_foreign_key(None, 'orders', 'vendors', ['vendor_id'], ['id'])
    op.create_foreign_key(None, 'orders', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # Drop the foreign key constraints first
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='foreignkey')

    # Revert the 'tracking_status' column to its previous type (VARCHAR)
    op.alter_column('orders', 'tracking_status',
               existing_type=postgresql.ENUM('PENDING', 'SHIPPED', 'DELIVERED', 'FAILED', name='orderstatusenum'),
               type_=sa.VARCHAR(),
               existing_nullable=True,
               existing_server_default=sa.text("'Pending'::character varying"))

    # Drop the ENUM type 'orderstatusenum'
    order_status_enum = postgresql.ENUM('PENDING', 'SHIPPED', 'DELIVERED', 'FAILED', name='orderstatusenum')
    order_status_enum.drop(op.get_bind(), checkfirst=True)

    # Drop the columns
    op.drop_column('orders', 'is_backup_fulfillment')
    op.drop_column('orders', 'fulfillment_source_type')
    op.drop_column('orders', 'fulfillment_source_id')

    # Drop the created tables and indexes
    op.drop_index(op.f('ix_vendors_id'), table_name='vendors')
    op.drop_table('vendors')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    # ### end Alembic commands ###
