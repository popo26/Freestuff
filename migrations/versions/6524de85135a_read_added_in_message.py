"""read added in Message

Revision ID: 6524de85135a
Revises: 448438eab9d7
Create Date: 2022-07-04 14:06:13.976461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6524de85135a'
down_revision = '448438eab9d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_users')
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('read', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_column('read')

    op.create_table('_alembic_tmp_users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('question_answered', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.Column('email', sa.VARCHAR(length=64), nullable=True),
    sa.Column('confirmed', sa.BOOLEAN(), nullable=True),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('location', sa.VARCHAR(length=64), nullable=True),
    sa.Column('bio', sa.TEXT(), nullable=True),
    sa.Column('last_seen', sa.DATETIME(), nullable=True),
    sa.Column('role_id', sa.INTEGER(), nullable=True),
    sa.Column('question_received', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='fk_users_role_id_roles'),
    sa.PrimaryKeyConstraint('id', name='pk_users')
    )
    # ### end Alembic commands ###