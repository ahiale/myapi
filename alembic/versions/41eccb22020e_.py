"""empty message

Revision ID: 41eccb22020e
Revises: 40196625db7d
Create Date: 2024-07-03 16:31:07.248092

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41eccb22020e'
down_revision: Union[str, None] = '40196625db7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Crée la table enfant_video
    op.create_table(
        'enfant_video',
        sa.Column('enfant_id', sa.String(), nullable=False),
        sa.Column('video_id', sa.String(length=255), nullable=False),
        sa.Column('like', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ['enfant_id'], ['enfants.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['video_id'], ['videos.id'], ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('enfant_id', 'video_id')
    )

    # Crée la table categorie_video
    op.create_table(
        'categorie_video',
        sa.Column('categorie_id', sa.String(), nullable=False),
        sa.Column('video_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ['categorie_id'], ['categories.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['video_id'], ['videos.id'], ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('categorie_id', 'video_id')
    )

    # ### end Alembic commands ###

def downgrade():
    # Supprime les tables d'association
    op.drop_table('enfant_video')
    op.drop_table('categorie_video')
    # ### end Alembic commands ###
