from app.db.base import Base
from app.db.session import engine

# Register models
from app.models import user, company, statement, prediction, anomaly, report  # noqa


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
