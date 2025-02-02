"""Add ForeignKeys and new fields to OrderModel

Revision ID: a83132464282
Revises: 289893062975
Create Date: 2024-09-28 16:17:22.603103

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'a83132464282'
down_revision = '289893062975'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to the orders table with default values for existing rows
    op.add_column('orders', sa.Column('fulfillment_source_id', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('orders', sa.Column('fulfillment_source_type', sa.String(), nullable=False, server_default='default_source'))
    op.add_column('orders', sa.Column('is_backup_fulfillment', sa.Integer(), nullable=True, server_default='0'))

    # Create the enum type for orderstatusenum
    order_status_enum = postgresql.ENUM('PENDING', 'SHIPPED', 'DELIVERED', 'FAILED', name='orderstatusenum')
    order_status_enum.create(op.get_bind(), checkfirst=True)

    # Normalize the existing values in tracking_status
    op.execute(
        """
        UPDATE orders
        SET tracking_status = CASE
            WHEN tracking_status = 'Pending' THEN 'PENDING'
            WHEN tracking_status = 'Shipped' THEN 'SHIPPED'
            WHEN tracking_status = 'Delivered' THEN 'DELIVERED'
            WHEN tracking_status = 'Failed' THEN 'FAILED'
            ELSE tracking_status
        END
        """
    )

    # Remove the default value temporarily to avoid the casting issue
    op.alter_column('orders', 'tracking_status', server_default=None)

    # Alter tracking_status to use Enum with the USING clause to convert existing values
    op.execute(
        """
        ALTER TABLE orders 
        ALTER COLUMN tracking_status 
        TYPE orderstatusenum 
        USING (CASE 
            WHEN tracking_status = 'PENDING' THEN 'PENDING'::orderstatusenum
            WHEN tracking_status = 'SHIPPED' THEN 'SHIPPED'::orderstatusenum
            WHEN tracking_status = 'DELIVERED' THEN 'DELIVERED'::orderstatusenum
            WHEN tracking_status = 'FAILED' THEN 'FAILED'::orderstatusenum
        END)
        """
    )

    # Reapply the default value after changing the column type
    op.alter_column('orders', 'tracking_status', server_default=sa.text("'PENDING'::orderstatusenum"))

    # Add ForeignKey constraints
    op.create_foreign_key(None, 'orders', 'products', ['product_id'], ['id'])
    op.create_foreign_key(None, 'orders', 'sellers', ['seller_id'], ['id'])
    op.create_foreign_key(None, 'orders', 'users', ['user_id'], ['id'])


def downgrade():
    # Drop ForeignKey constraints
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='foreignkey')

    # Revert tracking_status back to VARCHAR
    order_status_enum = postgresql.ENUM('PENDING', 'SHIPPED', 'DELIVERED', 'FAILED', name='orderstatusenum')
    op.alter_column('orders', 'tracking_status',
               existing_type=order_status_enum,
               type_=sa.VARCHAR(),
               existing_nullable=True,
               existing_server_default=sa.text("'Pending'::character varying"))

    # Drop the enum type
    order_status_enum.drop(op.get_bind(), checkfirst=True)

    # Drop the newly added columns
    op.drop_column('orders', 'is_backup_fulfillment')
    op.drop_column('orders', 'fulfillment_source_type')
    op.drop_column('orders', 'fulfillment_source_id')
