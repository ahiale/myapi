
from sqlalchemy import Table, Column, String, ForeignKey
from database import Base

categorie_video = Table(
    'categorie_video',
    Base.metadata,
    Column('categorie_id', String, ForeignKey('categories.id'),primary_key=True),
    Column('video_id', String, ForeignKey('videos.id'),primary_key=True),
)
