'''
    Photo module
'''

from dataclasses import dataclass
from sqlalchemy import Integer, Column, String, ForeignKey
from databases.models.user import User
from config.db import db


@dataclass
class Photo(db.Model):  # pylint: disable=too-few-public-methods
    '''
        Photo model class
    '''
    id: int  # pylint: disable=C0103
    photo: str

    __tablename__ = 'User_Photo'

    id = Column(Integer, primary_key=True)
    photo = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
