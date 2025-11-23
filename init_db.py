from infrastructure.db.base import Base, engine
from infrastructure.models import *  # This imports all models

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
