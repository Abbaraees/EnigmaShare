"""removed user_messages table

Revision ID: eaba665968f3
Revises: 71911bb113aa
Create Date: 2023-08-09 13:16:38.933483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eaba665968f3'
down_revision = '71911bb113aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_messages')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_messages',
    sa.Column('sender_id', sa.INTEGER(), nullable=True),
    sa.Column('receiver_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], )
    )
    # ### end Alembic commands ###