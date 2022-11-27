from db import SingletonDatabase

db = SingletonDatabase.get_instance()


class Platform(db.Base):
    __tablename__ = "platforms"
    __table_args__ = {"autoload": True}

    def __repr__(self):
        return f"Platform(id={self.id}, name={self.name})"

    @staticmethod
    def get_by_id(id):
        return db.session.query(Platform).filter(Platform.id == id).first()

    @staticmethod
    def get_by_name(name):
        return db.session.query(Platform).filter(Platform.name == name).first()

    @staticmethod
    def get_all():
        return db.session.query(Platform).all()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            print(f"Error al crear la plataforma {self.name}")
