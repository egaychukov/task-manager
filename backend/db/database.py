from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker

from core.config import settings


engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(engine)
