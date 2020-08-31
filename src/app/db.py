from databases import Database
import sqlalchemy

from src.app.config import config

db = Database(config.PG_DSN, force_rollback=(config.ENVIRONMENT == 'TESTING'))
metadata = sqlalchemy.MetaData()
