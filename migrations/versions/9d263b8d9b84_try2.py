"""try2

Revision ID: 9d263b8d9b84
Revises: 5c02a1ae2f20
Create Date: 2022-07-01 15:53:27.362798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d263b8d9b84'
down_revision = '5c02a1ae2f20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_constraint('fk_messages_post_id_posts', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_messages_post_id_posts'), 'posts', ['post_id'], ['id'], ondelete='cascade')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_messages_post_id_posts'), type_='foreignkey')
        batch_op.create_foreign_key('fk_messages_post_id_posts', 'posts', ['post_id'], ['id'])

    # ### end Alembic commands ###
