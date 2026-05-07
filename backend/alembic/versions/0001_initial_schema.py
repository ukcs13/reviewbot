"""initial schema

Revision ID: 0001
Revises: 
Create Date: 2026-05-06 23:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create reviews table
    op.create_table(
        'reviews',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_github_login', sa.String(length=100), nullable=True),
        sa.Column('source_type', sa.Enum('github_url', 'zip_upload', name='sourcetype'), nullable=False),
        sa.Column('source_identifier', sa.String(length=500), nullable=False),
        sa.Column('project_name', sa.String(length=255), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('review_decision', sa.Enum('excellent', 'good', 'needs_work', 'critical', name='reviewdecision'), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('high_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('medium_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('low_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('info_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('file_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('focus_areas', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('agent_results', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('review_time_ms', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create issues table
    op.create_table(
        'issues',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('review_id', sa.UUID(), nullable=False),
        sa.Column('severity', sa.Enum('high', 'medium', 'low', 'info', name='severity'), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('fix_suggestion', sa.Text(), nullable=False),
        sa.Column('file_path', sa.String(length=512), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_issues_review_id_severity', 'issues', ['review_id', 'severity'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_issues_review_id_severity', table_name='issues')
    op.drop_table('issues')
    op.drop_table('reviews')
    # Note: Enums might need manual dropping depending on DB
    sa.Enum(name='sourcetype').drop(op.get_bind())
    sa.Enum(name='reviewdecision').drop(op.get_bind())
    sa.Enum(name='severity').drop(op.get_bind())
