"""creating post table

Revision ID: ef51bdc24b20
Revises: 
Create Date: 2024-09-07 17:34:57.882380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef51bdc24b20'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.create_table('posts' , sa.Column('id' , sa.Integer() , nullable=False , primary_key = True) ,
                    sa.Column('title' , sa.String() , nullable=False))
    pass


def downgrade() :
    op.drop_table('posts')
    pass
