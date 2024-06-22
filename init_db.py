from app.core.db import Base, engine
from app import models

Base.metadata.create_all(bind=engine)
