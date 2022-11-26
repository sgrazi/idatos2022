from db import SingletonDatabase

db = SingletonDatabase.get_instance()

class Movie(db.Base):
    __tablename__ = "movies"
    __table_args__ = {'autoload':True}
    def __repr__(self):
        return f"Movie(id={self.id}, title={self.title}, director={self.director})"