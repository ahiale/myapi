from sqlalchemy import Table, Column, Integer, String, ForeignKey,Boolean
from database import Base

parent_video = Table(
    "parent_video",
    Base.metadata,
    Column("parent_id", String, ForeignKey("parents.id"), primary_key=True),
    Column("video_id", String(255), ForeignKey("videos.id"), primary_key=True),
    Column("interested", Boolean),
    Column("motifs", String)
)
