"""add more columns to posts table

Revision ID: c72c8016fcbd
Revises: 0b29500a7f6c
Create Date: 2024-09-08 21:28:42.368975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c72c8016fcbd'
down_revision: Union[str, None] = '0b29500a7f6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts' , sa.Column('published' , sa.String() , nullable=False , server_default='True'))
    op.add_column('posts' , sa.Column('ceated_at' , sa.TIMESTAMP(timezone=True) , nullable=False , server_default=sa.text('NOW()')))      
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
