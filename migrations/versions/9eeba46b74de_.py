"""empty message

Revision ID: 9eeba46b74de
Revises: 
Create Date: 2024-11-07 13:48:20.451455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9eeba46b74de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instruktor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('navn', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('telefon', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('lokation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('navn', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dansehold',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stilart', sa.String(length=50), nullable=False),
    sa.Column('instruktor', sa.String(length=100), nullable=True),
    sa.Column('beskrivelse', sa.String(length=200), nullable=True),
    sa.Column('lokation_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lokation_id'], ['lokation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('elev',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('navn', sa.String(length=100), nullable=False),
    sa.Column('fodselsdato', sa.String(length=10), nullable=False),
    sa.Column('lokation_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lokation_id'], ['lokation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('danselektion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dato', sa.Date(), nullable=False),
    sa.Column('tidspunkt', sa.Time(), nullable=False),
    sa.Column('dansehold_id', sa.Integer(), nullable=True),
    sa.Column('elev_id', sa.Integer(), nullable=True),
    sa.Column('lokation_id', sa.Integer(), nullable=True),
    sa.Column('instruktor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dansehold_id'], ['dansehold.id'], ),
    sa.ForeignKeyConstraint(['elev_id'], ['elev.id'], ),
    sa.ForeignKeyConstraint(['instruktor_id'], ['instruktor.id'], ),
    sa.ForeignKeyConstraint(['lokation_id'], ['lokation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attendance',
    sa.Column('elev_id', sa.Integer(), nullable=True),
    sa.Column('danselektion_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['danselektion_id'], ['danselektion.id'], ),
    sa.ForeignKeyConstraint(['elev_id'], ['elev.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attendance')
    op.drop_table('danselektion')
    op.drop_table('elev')
    op.drop_table('dansehold')
    op.drop_table('lokation')
    op.drop_table('instruktor')
    # ### end Alembic commands ###