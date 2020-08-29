import os


class Config:
    LOG_LEVEL = os.environ['LOG_LEVEL']


config = Config()
