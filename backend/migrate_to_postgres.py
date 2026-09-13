"""Migrate existing SQLite data to PostgreSQL."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models import user, company, statement, prediction, anomaly, report  # noqa

SQLITE_URL = "sqlite:///./finsight.db"
POSTGRES_URL = "postgresql+psycopg://finsight:Chandra_77@localhost:5432/finsight"

sqlite_engine = create_engine(SQLITE_URL)
pg_engine = create_engine(POSTGRES_URL)

Base.metadata.create_all(bind=pg_engine)
print("✅ Tables created in PostgreSQL")

sqlite_session = sessionmaker(bind=sqlite_engine)()
pg_session = sessionmaker(bind=pg_engine)()

models = [
    ("User", user.User),
    ("Company", company.Company),
    ("FinancialStatement", statement.FinancialStatement),
    ("Prediction", prediction.Prediction),
    ("Anomaly", anomaly.Anomaly),
    ("Report", report.Report),
]

total = 0
for name, Model in models:
    try:
        rows = sqlite_session.query(Model).all()
        for r in rows:
            data = {c.name: getattr(r, c.name) for c in r.__table__.columns}
            pg_session.merge(Model(**data))
        pg_session.commit()
        print(f"  Migrated {len(rows)} rows: {name}")
        total += len(rows)
    except Exception as e:
        print(f"  Skipped {name}: {e}")

print(f"\n🎉 Migration complete ({total} rows)")