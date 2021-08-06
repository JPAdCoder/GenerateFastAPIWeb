from config import *
from peewee import *
from uuid import uuid1
from playhouse.pool import PooledPostgresqlDatabase
from playhouse.shortcuts import ReconnectMixin
import datetime
import time


class RetryPgDevDB(ReconnectMixin, PooledPostgresqlDatabase):
    _instance = None

    @staticmethod
    def get_db_instance():
        if not RetryPgDevDB._instance:
            RetryPgDevDB._instance = RetryPgDevDB(
                DevelopmentConfig.DATABASE,
                max_connections=8,
                stale_timeout=300,
                host=DevelopmentConfig.PG_HOST,
                user=DevelopmentConfig.PG_USER,
                password=DevelopmentConfig.PG_PASSWORD,
                port=DevelopmentConfig.PG_PORT
            )
        return RetryPgDevDB._instance


class RetryPgTestDB(ReconnectMixin, PooledPostgresqlDatabase):
    _instance = None

    @staticmethod
    def get_db_instance():
        if not RetryPgTestDB._instance:
            RetryPgTestDB._instance = RetryPgTestDB(
                TestConfig.DATABASE,
                max_connections=8,
                stale_timeout=300,
                host=TestConfig.PG_HOST,
                user=TestConfig.PG_USER,
                password=TestConfig.PG_PASSWORD,
                port=TestConfig.PG_PORT
            )
        return RetryPgTestDB._instance


# dev_db = PostgresqlDatabase(DevelopmentConfig.DATABASE, user=DevelopmentConfig.PG_USER,
#                             password=DevelopmentConfig.PG_PASSWORD, host=DevelopmentConfig.PG_HOST,
#                             port=DevelopmentConfig.PG_PORT)

# test_db = PostgresqlDatabase(TestConfig.DATABASE, user=TestConfig.PG_USER,
#                              password=TestConfig.PG_PASSWORD, host=TestConfig.PG_HOST,
#                              port=TestConfig.PG_PORT)

mode = 1

if mode == 0:
    # db = dev_db
    db = RetryPgDevDB.get_db_instance()
else:
    # db = test_db
    db = RetryPgTestDB.get_db_instance()


class User(Model):
    id = CharField(max_length=32, primary_key=True)
    name = CharField(max_length=16, null=True)
    add_datetime = DateTimeField(default=datetime.datetime.now, formats=['%Y-%m-%d %H:%M:%S', ])

    class Meta:
        table_name = 'T_User'


class Role(Model):
    pass
