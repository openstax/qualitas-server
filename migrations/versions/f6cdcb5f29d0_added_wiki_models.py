"""added wiki models

Revision ID: f6cdcb5f29d0
Revises: 45f092ba791c
Create Date: 2018-10-15 10:22:40.271440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6cdcb5f29d0'
down_revision = '45f092ba791c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('wiki_page',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=False),
    sa.Column('draft', sa.Boolean(), nullable=False),
    sa.Column('redirect_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['redirect_id'], ['wiki_page.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('title')
    )


def downgrade():
    op.drop_table('wiki_page')
