from db import SingletonDatabase


db = SingletonDatabase.get_instance()


class Genre(db.Base):
    __tablename__ = "genres"
    __table_args__ = {"autoload": True}

    def __repr__(self):
        return f"Genre(id={self.id}, name={self.name})"

    @staticmethod
    def get_by_id(id):
        return db.session.query(Genre).filter(Genre.id == id).first()

    @staticmethod
    def get_by_name(name):
        return db.session.query(Genre).filter(Genre.name == name).first()

    @staticmethod
    def get_all(cls):
        return db.session.query(Genre).all()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            print(f"Error al crear el género {self.name}")
