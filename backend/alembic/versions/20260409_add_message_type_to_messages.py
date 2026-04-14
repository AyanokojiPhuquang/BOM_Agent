"""add message_type and tool_name to conversation_messages

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-04-09
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("conversation_messages", sa.Column("message_type", sa.String(), nullable=True))
    op.add_column("conversation_messages", sa.Column("tool_name", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("conversation_messages", "tool_name")
    op.drop_column("conversation_messages", "message_type")
