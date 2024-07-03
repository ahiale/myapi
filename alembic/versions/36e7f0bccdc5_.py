"""empty message

Revision ID: 36e7f0bccdc5
Revises: 9c9946d3f7f4
Create Date: 2024-07-03 11:38:11.250345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36e7f0bccdc5'
down_revision: Union[str, None] = '9c9946d3f7f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Supprimer les clés primaires existantes si elles existent
    op.drop_constraint('enfant_video_pkey', 'enfant_video', type_='primary')

    # Ajouter les colonnes avec les contraintes de clé primaire composées
    op.create_primary_key(
        'enfant_video_pkey', 
        'enfant_video', 
        ['enfant_id', 'video_id']
    )

    # Optionnel : Assurer que les colonnes sont non-nullables
    op.alter_column('enfant_video', 'enfant_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('enfant_video', 'video_id',
               existing_type=sa.VARCHAR(),
               nullable=False)


def downgrade() -> None:
    # Supprimer les clés primaires composées
    op.drop_constraint('enfant_video_pkey', 'enfant_video', type_='primary')

    # Réajouter les contraintes de clé étrangère si nécessaire
    op.create_primary_key(
        'enfant_video_pkey', 
        'enfant_video', 
        ['video_id', 'enfant_id']
    )
    
    # Optionnel : Réajuster les colonnes pour les rendre nullables
    op.alter_column('enfant_video', 'video_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('enfant_video', 'enfant_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
