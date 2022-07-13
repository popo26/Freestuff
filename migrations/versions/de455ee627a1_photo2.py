"""Photo2

Revision ID: de455ee627a1
Revises: 140381cc7215
Create Date: 2022-07-06 13:49:22.106144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de455ee627a1'
down_revision = '140381cc7215'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('post_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_photos_post_id_posts'), 'posts', ['post_id'], ['id'])

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint('fk_posts_photo_id_photos', type_='foreignkey')
        batch_op.drop_column('photo_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('photo_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_posts_photo_id_photos', 'photos', ['photo_id'], ['id'])

    with op.batch_alter_table('photos', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_photos_post_id_posts'), type_='foreignkey')
        batch_op.drop_column('post_id')

    # ### end Alembic commands ###
