"""question_answered

Revision ID: 448438eab9d7
Revises: 669fc3639cf4
Create Date: 2022-07-04 11:58:34.826276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '448438eab9d7'
down_revision = '669fc3639cf4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('question_answered', sa.Integer(), nullable=False))
        batch_op.drop_column('question_posted')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('question_posted', sa.INTEGER(), nullable=False))
        batch_op.drop_column('question_answered')

    # ### end Alembic commands ###