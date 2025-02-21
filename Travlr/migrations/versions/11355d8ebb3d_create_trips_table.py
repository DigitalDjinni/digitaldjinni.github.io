"""Create trips table

Revision ID: 11355d8ebb3d
Revises: c99f8e584452
Create Date: 2025-01-23 10:19:20.360755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11355d8ebb3d'
down_revision = 'c99f8e584452'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trips', schema=None) as batch_op:
        batch_op.alter_column('length',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('start',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('resort',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('per_person',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
        batch_op.alter_column('image',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=100),
               existing_nullable=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.drop_column('role')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.drop_column('is_admin')

    with op.batch_alter_table('trips', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=200),
               existing_nullable=True)
        batch_op.alter_column('per_person',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
        batch_op.alter_column('resort',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('start',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.alter_column('length',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###
