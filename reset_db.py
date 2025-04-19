# reset_db.py

from dependencies.database import Database
from dependencies.database import Base
from models import restaurant, reservation, user, bookingslot  # import all models here
from models.common import Base

db = Database.get_instance()
engine = db.engine  # Access engine from the singleton instance

print("🔁 Dropping existing tables...")
Base.metadata.drop_all(engine)  # Drop all tables bound to this engine

print("🛠️ Creating tables from models...")
Base.metadata.create_all(engine)  # Create tables from the models

print("✅ DB reset complete.")
