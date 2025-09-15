# init_db.py

from app.database import Base, engine
import app.models  # make sure models are imported

print("📦 Creating tables in the database...")

Base.metadata.create_all(bind=engine)

print("✅ Done. Tables created.")
