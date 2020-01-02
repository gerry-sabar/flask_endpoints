"""empty message

Revision ID: a1daa6ac7c0e
Revises: e27df8c512f2
Create Date: 2020-01-01 13:42:51.614085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1daa6ac7c0e'
down_revision = 'e27df8c512f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_access_token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('revoked', sa.Integer(), nullable=False),
    sa.Column('access_token', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'revoked')
    )
    op.create_table('user_refresh_token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('revoked', sa.Integer(), nullable=False),
    sa.Column('refresh_token', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'revoked')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_refresh_token')
    op.drop_table('user_access_token')
    # ### end Alembic commands ###
