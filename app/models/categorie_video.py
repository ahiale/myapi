
from sqlalchemy import Table, Column, String, ForeignKey
from database import metadata

categorie_video = Table(
    'categorie_video',
    metadata,
    Column('categorie_id', String, ForeignKey('categories.id')),
    Column('video_id', String, ForeignKey('videos.id')),
    primary_key=['categorie_id', 'video_id']
)
