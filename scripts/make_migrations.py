from src.app.config import config
import alembic.config
import alembic.command


alembic_cfg = alembic.config.Config()
alembic_cfg.set_main_option('script_location', 'alembic')
alembic_cfg.set_main_option('sqlalchemy.url', config.PG_DSN)


def make_migrations():
    alembic.command.upgrade(alembic_cfg, 'head')


def rollback_all_migrations():
    alembic.command.downgrade(alembic_cfg, 'base')


if __name__ == '__main__':
    make_migrations()
