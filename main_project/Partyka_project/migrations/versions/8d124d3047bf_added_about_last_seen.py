"""Added(about, last_seen)

Revision ID: 8d124d3047bf
Revises: 7a1823d3fad8
Create Date: 2023-11-16 15:45:19.133393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d124d3047bf'
down_revision = '7a1823d3fad8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('about_me', sa.String(length=240), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('about_me')
        batch_op.drop_column('last_seen')

    # ### end Alembic commands ###
