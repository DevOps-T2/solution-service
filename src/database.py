from sqlalchemy import Column, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
Session = sessionmaker()


class Solution(Base):
    __tablename__: str = 'solutions'

    user_id = Column(String, primary_key=True)
    computation_id = Column(String, primary_key=True)
    url = Column(String)
    file_uuid = Column(String)

    def __repr__(self):
        return "<Solution(user_id='{}', solution_id='{}', url='{}')>".format(
                                self.user_id, self.solution_id, self.url)
