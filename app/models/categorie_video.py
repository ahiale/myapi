
from sqlalchemy import Table, Column, String, ForeignKey
from database import Base


# class CategorieVideo(Base):
#     __tablename__ = 'categorie_video'
    
#     categorie_id = Column(String, ForeignKey('categories.id'), primary_key=True)
#     video_id = Column(String, ForeignKey('videos.id'), primary_key=True)

categorie_video = Table(
    'categorie_video',
    Base.metadata,
    Column('categorie_id', String, ForeignKey('categories.id'),primary_key=True),
    Column('video_id', String, ForeignKey('videos.id'),primary_key=True),
)
