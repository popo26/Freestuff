"""reply added in Message

Revision ID: 5c02a1ae2f20
Revises: 0983ca517bec
Create Date: 2022-07-01 09:28:41.822196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c02a1ae2f20'
down_revision = '0983ca517bec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reply', sa.Boolean(), nullable=True))
        batch_op.drop_column('title')

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_roles_name'), ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_roles_name'), type_='unique')

    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.VARCHAR(length=254), nullable=True))
        batch_op.drop_column('reply')

    # ### end Alembic commands ###
