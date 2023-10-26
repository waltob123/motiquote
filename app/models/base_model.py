import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    '''Base model for all models in the app.'''

    id = Column(String(255), primary_key=True, default=uuid.uuid4,
                         unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow,
                                 nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                                 onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def __str__(self):
        '''String representation of base model.'''
        return f'<{self.__class__.__name__} {self.id}>'

    def __repr__(self):
        '''String representation of base model.'''
        return f'{self.__class__.__name__}()'
