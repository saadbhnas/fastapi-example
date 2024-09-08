"""add forigen key to posts : owner_id

Revision ID: 0b29500a7f6c
Revises: f4e31751b2e8
Create Date: 2024-09-08 21:15:53.533501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b29500a7f6c'
down_revision: Union[str, None] = 'f4e31751b2e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts' , sa.Column('owner_id' , sa.Integer() , nullable=False))
    op.create_foreign_key('posts_users_fk' , source_table='posts' , referent_table='users' , local_cols=['owner_id'] , remote_cols=['id'] , ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk' , table_name='posts')
    op.drop_column('posts' , 'owner_id')
    pass
