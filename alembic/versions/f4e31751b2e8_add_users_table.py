"""add users table

Revision ID: f4e31751b2e8
Revises: a76532b788ce
Create Date: 2024-09-08 16:45:03.128606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4e31751b2e8'
down_revision: Union[str, None] = 'a76532b788ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users" , 
                    sa.Column('id' , sa.Integer() , nullable=False ) , 
                    sa.Column('email' , sa.String() , nullable=False) , 
                    sa.Column('password' , sa.String() , nullable=False) , 
                    sa.Column('created_at' , sa.TIMESTAMP(timezone=True) , server_default=sa.text('NOW()') , nullable=False) , 
                    sa.PrimaryKeyConstraint('id') , 
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
