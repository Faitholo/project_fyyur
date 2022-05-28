"""empty message

Revision ID: 8d4616e79f02
Revises: 17ca14b64e3c
Create Date: 2022-05-28 10:37:55.700302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d4616e79f02'
down_revision = '17ca14b64e3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True, default = False))
    op.add_column('artist', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True, default=False))
    op.add_column('venue', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'seeking_description')
    op.drop_column('venue', 'seeking_talent')
    op.drop_column('venue', 'website_link')
    op.drop_column('venue', 'genres')
    op.drop_column('artist', 'seeking_description')
    op.drop_column('artist', 'seeking_venue')
    op.drop_column('artist', 'website_link')
    # ### end Alembic commands ###