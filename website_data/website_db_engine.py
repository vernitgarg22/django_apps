#!/usr/bin/env python

import json

from sshtunnel import SSHTunnelForwarder, create_logger
from sqlalchemy import create_engine
from sqlalchemy.sql import text


def get_secrets():

    with open("../django_apps/secrets.json") as input:

        secrets = input.read()
        return json.loads(secrets)


class WebsiteDBEngine():

    def __init__(self, dbname):

        self.dbname = dbname
        self.db_info = get_secrets()["DATABASES"][self.dbname]
        self.ssh_host = self.db_info["SSH_HOST"]
        self.db_name = self.db_info["NAME"]
        self.db_engine = self.db_info["SQLALCHEMY_ENGINE"]
        self.db_user = self.db_info["USER"]
        self.db_pass = self.db_info["PASSWORD"]

    def start(self):
        """
        Connect to server (ssh as well as database).
        """

        self.server = SSHTunnelForwarder(
                ssh_address_or_host=self.ssh_host,
                ssh_username=self.dbname,
                ssh_pkey='~/.ssh/id_rsa',
                remote_bind_address=('127.0.0.1', 3306),
                logger=create_logger(loglevel=0))

        self.server.start()

        local_port=str(self.server.local_bind_port)

        self.engine = create_engine('{}://{}:{}@127.0.0.1:{}/{}?charset=utf8mb4'.format(self.db_engine, self.db_user, self.db_pass, local_port, self.db_name))
        self.conn = self.engine.connect()

    def run(self, sql, **sql_args):
        """
        Run a sql query against the database.
        """

        self.engine.execute(text(sql), sql_args)

    def get(self, sql, **sql_args):
        """
        Get data from the database.
        """

        return self.conn.execute(text(sql), sql_args).fetchall()

    def table_names(self):

        return self.engine.table_names()

    def stop(self):
        """
        Disconnect and stop server and database connections.
        """

        self.conn.close()
        self.engine.dispose()
        self.server.stop()
