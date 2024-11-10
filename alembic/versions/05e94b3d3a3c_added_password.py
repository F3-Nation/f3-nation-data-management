"""Added password

Revision ID: 05e94b3d3a3c
Revises: 7503b21bd815
Create Date: 2024-11-02 08:22:00.503529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '05e94b3d3a3c'
down_revision: Union[str, None] = '7503b21bd815'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###