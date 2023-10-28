"""weathers

Revision ID: 004d669eb6e6
Revises: f7dc30c79df3
Create Date: 2023-10-24 00:38:33.550728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004d669eb6e6'
down_revision: Union[str, None] = 'f7dc30c79df3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weathers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['city'], ['cities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weathers')
    # ### end Alembic commands ###