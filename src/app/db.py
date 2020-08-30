from databases import Database
import sqlalchemy

from src.app.config import config

db = Database(config.PG_DSN)
metadata = sqlalchemy.MetaData()
