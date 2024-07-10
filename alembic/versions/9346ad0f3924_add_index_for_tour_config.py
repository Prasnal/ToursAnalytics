"""Add index for tour config

Revision ID: 9346ad0f3924
Revises: 06e24459645c
Create Date: 2024-06-23 13:04:52.647520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9346ad0f3924'
down_revision: Union[str, None] = '06e24459645c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('tour_configs_index', 'tour_config', ['tour_length', 'start_tour_date', 'start_location', 'location_additional_cost', 'end_tour_date', 'tour_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('tour_configs_index', table_name='tour_config')
    # ### end Alembic commands ###