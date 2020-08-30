import os


class Config:
    ENVIRONMENT = os.environ['ENVIRONMENT']
    LOG_LEVEL = os.environ['LOG_LEVEL']

    PG_HOST = os.environ['PG_HOST']
    PG_PORT = os.environ['PG_PORT']
    PG_DB_NAME = os.environ['PG_DB_NAME']
    PG_USER = os.environ['PG_USER']
    PG_PASSWORD = os.environ['PG_PASSWORD']

    @property
    def PG_DSN(self):
        return f'postgresql://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB_NAME}'


config = Config()
