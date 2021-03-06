"""initial schema

Revision ID: 45f092ba791c
Revises: 
Create Date: 2018-10-14 18:49:28.557236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45f092ba791c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('github_users',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=False),
    sa.Column('profile_image', sa.String(), nullable=False),
    sa.Column('profile_link', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=100), nullable=True),
    sa.Column('current_login_ip', sa.String(length=100), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['github_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )


def downgrade():
    op.drop_table('roles_users')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('github_users')
