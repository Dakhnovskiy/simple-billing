from src.app.config import config
import alembic.config
import alembic.command


def make_migrations():
    alembic_cfg = alembic.config.Config()
    alembic_cfg.set_main_option('script_location', 'alembic')
    alembic_cfg.set_main_option('sqlalchemy.url', config.PG_DSN)
    alembic.command.upgrade(alembic_cfg, 'head')


if __name__ == '__main__':
    make_migrations()
