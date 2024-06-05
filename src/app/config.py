import os


class Config:
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    EXPLAIN_TEMPLATE_LOADING = True
