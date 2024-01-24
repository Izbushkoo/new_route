"""initial

Revision ID: 10af9ae36d9e
Revises: 
Create Date: 2024-01-24 19:30:33.318689

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '10af9ae36d9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tools',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tools_id'), 'tools', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('message_threads',
    sa.Column('thread_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('thread_id')
    )
    op.create_table('user_settings',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('voice_answer', sa.Boolean(), nullable=False),
    sa.Column('voice_sound', sa.Enum('alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer', name='voicesound'), nullable=True),
    sa.Column('audio_speed', sa.Float(), nullable=True),
    sa.Column('current_assistant', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('gpt_model', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('current_message_thread', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('usersettingstoolslink',
    sa.Column('user_settings_id', sa.Integer(), nullable=False),
    sa.Column('tool_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tool_id'], ['tools.id'], ),
    sa.ForeignKeyConstraint(['user_settings_id'], ['user_settings.user_id'], ),
    sa.PrimaryKeyConstraint('user_settings_id', 'tool_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usersettingstoolslink')
    op.drop_table('user_settings')
    op.drop_table('message_threads')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_tools_id'), table_name='tools')
    op.drop_table('tools')
    # ### end Alembic commands ###