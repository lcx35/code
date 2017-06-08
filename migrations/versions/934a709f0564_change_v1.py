"""change_v1

Revision ID: 934a709f0564
Revises: 
Create Date: 2017-05-11 17:52:35.686214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '934a709f0564'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('user_id', table_name='log')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('user_id', 'log', ['user_id'], unique=True)
    # ### end Alembic commands ###
