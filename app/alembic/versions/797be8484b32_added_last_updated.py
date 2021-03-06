"""Added last_updated

Revision ID: 797be8484b32
Revises: 
Create Date: 2020-02-11 19:28:01.339447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '797be8484b32'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('packages', sa.Column('last_updated', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_packages_last_updated'), 'packages', ['last_updated'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_packages_last_updated'), table_name='packages')
    op.drop_column('packages', 'last_updated')
    # ### end Alembic commands ###
