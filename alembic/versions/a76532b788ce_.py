"""empty message

Revision ID: a76532b788ce
Revises: ef51bdc24b20
Create Date: 2024-09-07 18:07:03.990167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a76532b788ce'
down_revision: Union[str, None] = 'ef51bdc24b20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts' , sa.Column('content' , sa.String() , nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts' , 'content')
    pass
