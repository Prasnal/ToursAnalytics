"""Add scrape datetime to tour prices

Revision ID: 0c2d42e31022
Revises: 41078e811b74
Create Date: 2024-02-12 09:59:15.343005

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c2d42e31022'
down_revision: Union[str, None] = '41078e811b74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tour_price', sa.Column('scraped_time', sa.Time(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tour_price', 'scraped_time')
    # ### end Alembic commands ###
