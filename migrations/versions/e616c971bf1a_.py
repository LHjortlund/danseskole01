"""empty message

Revision ID: e616c971bf1a
Revises: 
Create Date: 2024-10-22 12:06:13.159607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e616c971bf1a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('elev',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('navn', sa.String(length=100), nullable=False),
    sa.Column('fodselsdato', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('elev')
    # ### end Alembic commands ###
