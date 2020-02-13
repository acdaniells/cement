"""
Cement Ibis extension module.
"""

import os
import sys
import time

from abc import abstractmethod
from collections import namedtuple

from cement.core import exc, meta
from cement.core.handler import Handler
from cement.core.interface import Interface
from cement.utils.misc import minimal_logger

import urllib3

urllib3.disable_warnings()

LOG = minimal_logger(__name__)


class IbisInterface(Interface):

    """
    This class defines the Ibis Interface. Handlers that implement this
    interface must provide the methods and attributes defined below. In
    general, most implementations should sub-class from the provided
    :class:`IbisHandler` base class as a starting point.
    """

    class Meta:

        """Handler meta-data."""

        #: The string identifier of the interface
        interface = "ibis"

    @abstractmethod
    def connect(self):
        pass  # pragma: nocover

    @abstractmethod
    def close(self):
        pass  # pragma: nocover

    @property
    @abstractmethod
    def client(self):
        pass  # pragma: nocover


class IbisHandler(IbisInterface, Handler):

    """Ibis handler implementation."""

    class Meta:
        name = NotImplemented

    @property
    def name(self):
        return self._meta.name


class IbisPandasHandler(IbisHandler):

    """
    Handler class for the Ibis Hive client.
    """

    class Meta:
        label = "pandas"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._client = None

    def connect(self, dataframes):
        import ibis

        self._client = ibis.pandas.connect(dataframes)

    def close(self):
        pass

    @property
    def client(self):
        return self._client

    def from_dataframe(self, df, name="df"):
        if self.client is None:
            return self.connect({name: df}).table(name)

        self.client.dictionary[name] = df

        return self.client.table(name)


class IbisHDFSHandler(IbisHandler):

    """
    Handler class for the Ibis HDFS client.
    """

    class Meta:

        """
        Handler meta-data.
        """

        label = "hdfs"
        """The string identifier for the command."""

        env = None

        # The default configuration dictionary to populate the ``client`` section.
        config_defaults = dict(
            host="localhost",
            port=14000,
            auth_mechanism="GSSAPI",
            use_https=True,
            verify=False,
            timeout=60,
        )

        env_defaults = {
            "ibis.hdfs.sandbox": {"host": "us1salxhpm0009.corpnet2.com"},
            "ibis.hdfs.mcc-dev": {"host": "us1salxhpm0026.corpnet2.com"},
            "ibis.hdfs.mcc-prd": {"host": "us1salxhpm0031.corpnet2.com"},
            "ibis.hdfs.scc-dev": {"host": "us1salxhpm0012.corpnet2.com"},
            "ibis.hdfs.scc-tst": {"host": "us1salxhpm0017.corpnet2.com"},
            "ibis.hdfs.scc-prd": {"host": "us1salxhpm0001.corpnet2.com"},
        }

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.section = None
        self._client = None

    def _setup(self, app_obj):
        super()._setup(app_obj)

        self.section = f"{self._meta.config_section}.{self._meta.env}"

        dict_obj = {}
        dict_obj[self.section] = self._meta.env_defaults[self.section]

        self.app.config.merge(dict_obj)

        dict_obj = {}
        dict_obj[self.section] = self.app.config.get_section_dict(
            self._meta.config_section
        )

        self.app.config.merge(dict_obj, override=False)

    def connect(self):
        import ibis

        kw = self.app.config.get_section_dict(self.section)
        self._client = ibis.hdfs_connect(**kw)

    def close(self):
        pass

    @property
    def client(self):
        return self._client

    @property
    def env(self):
        return self._meta.env


class IbisImpalaHandler(IbisHandler):

    """
    Handler class for the Ibis Impala client.
    """

    class Meta:

        """
        Handler meta-data.
        """

        label = "impala"
        """The string identifier for the command."""

        env = None

        # The default configuration dictionary to populate the ``client`` section.
        config_defaults = dict(
            session_timeout=3600,
            pool_size=8,
            port=21050,
            database="default",
            timeout=0,
            use_ssl=True,
            ca_cert="/opt/cloudera/security/pki/ca-certs.pem",
            auth_mechanism="GSSAPI",
            kerberos_service_name="impala",
        )

        env_defaults = {
            "ibis.impala.sandbox": {"host": "impala-snd.rdip.gsk.com"},
            "ibis.impala.mcc-dev": {"host": "impala-dev-mcc.rdip.gsk.com"},
            "ibis.impala.mcc-prd": {"host": "impala-prd-mcc.rdip.gsk.com"},
            "ibis.impala.scc-dev": {"host": "impala-dev-scc.rdip.gsk.com"},
            "ibis.impala.scc-tst": {"host": "impala-tst-scc.rdip.gsk.com"},
            "ibis.impala.scc-prd": {"host": "impala-prd-scc.rdip.gsk.com"},
        }

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.connect_time = None
        self.section = None
        self._connection = None
        self._hdfs = None
        self._client = None

        import ibis
        import getpass

        ibis.options.impala.temp_db = getpass.getuser()
        ibis.options.impala.temp_hdfs_path = f"/user/{getpass.getuser()}/.ibis"

        properties = [
            "tag",
            "exists",
            "env",
            "database",
            "table",
            "name",
            "base_expr",
            "expr",
        ]

        self.Table = namedtuple("Table", properties)

    def _setup(self, app_obj):
        super()._setup(app_obj)

        self.section = f"{self._meta.config_section}.{self._meta.env}"

        dict_obj = {}
        dict_obj[self.section] = self._meta.env_defaults[self.section]

        self.app.config.merge(dict_obj)

        dict_obj = {}
        dict_obj[self.section] = self.app.config.get_section_dict(
            self._meta.config_section
        )

        self.app.config.merge(dict_obj, override=False)

    def connect(self, hdfs=None):
        import ibis
        from ibis.impala.client import ImpalaClient, ImpalaConnection

        kw = self.app.config.get_section_dict(self.section)
        kw.pop("session_timeout")

        connection = ImpalaConnection(**kw)

        if hdfs is not None:
            self._hdfs = hdfs.client

        try:
            client = ImpalaClient(connection, hdfs_client=self._hdfs)
        except Exception:
            connection.close()
            raise exc.FrameworkError("Failed to connect impala client")
        else:
            if ibis.config.options.default_backend is None:
                ibis.config.options.default_backend = client

        self.connect_time = time.time()
        self._connection = connection
        self._client = client

    def reconnect(self):
        self.close()
        self.connect()

    def close(self):
        self._client.close()

    @property
    def client(self):
        self._check_session()

        return self._client

    @property
    def hdfs(self):
        return self._hdfs

    @property
    def env(self):
        return self._meta.env

    def table(self, name):
        return self.client.table(self._safe_name(name))

    def namespace(self, name, tag="default", filter=None):
        database, table = self._qualify_name(name)
        name = self._safe_name(name)

        exists = self._exists_table(name)

        if exists:
            if filter is None:
                base_expr = self.client.table(name)
                expr = base_expr
            else:
                base_expr = self.client.table(name)
                expr = self.client.sql(f"SELECT * FROM {name} WHERE {filter}")
        else:
            base_expr = None
            expr = None

        return self.Table(
            tag, exists, self._meta.env, database, table, name, base_expr, expr
        )

    def compile(self, expr):
        import ibis

        return ibis.impala.compile(expr)

    def safe_expr(self, expr):
        # hack to remove window clause automatically added by Ibis when
        # aggregate functions are used in a non-aggregate context which causes
        # a massive performance problem in this case.
        return self.client.sql(self.compile(expr).replace(" OVER ()", ""))

    def get_column_type(self, table, column):
        table = self._safe_name(table)

        if self._exists_table(table):
            schema = dict(self.client.table(table).schema().items())
            if column in schema.keys():
                return str(schema[column])

    def cast_value(self, table, column, value):
        type = self.get_column_type(table, column)

        if type is None or value is None:
            pass
        elif type == "string":
            value = f"'{value}'"
        else:
            value = float(value)

        return value

    def _qualify_name(self, name):
        split = name.replace("`", "").split(".")

        if len(split) == 2:
            database = split[0]
            table = split[1]
        elif len(split) == 1:
            database = self.app.config.get(self.section, "database")
            table = split[0]
        else:
            raise exc.FrameworkError(f"Invalid table name '{name}'")

        return database, table

    def _safe_name(self, name):
        database, table = self._qualify_name(name)

        return f"{database}.`{table}`"

    def _exists_table(self, name):
        database, table = self._qualify_name(name)
        return self.client.exists_table(table, database)

    def _check_session(self):
        timeout = self.app.config.get(self.section, "session_timeout")
        now_time = time.time()
        if now_time - self.connect_time > timeout:
            self.connect_time = now_time
            self.reconnect()


class IbisManager(meta.MetaMixin):
    class Meta:
        services = ["pandas", "hdfs", "impala"]

    def __init__(self, app, *args, **kw):
        super().__init__(*args, **kw)
        self.app = app
        self.__handlers__ = {}

        import ibis

        ibis.options.sql.default_limit = 10_000_000

    def close(self):
        for handler in self.__handlers__.values():
            handler.close()

        self.__handlers__ = {}

        LOG.debug("Ibis manager stopped")

    def add(
        self, service="impala", env=None, database=None, dataframes=None, number=None
    ):
        try:
            assert (
                service in self._meta.services
            ), f"The service '{service}' is not supported."
        except AssertionError as e:
            raise exc.FrameworkError(e)

        if self.app.handler.registered("platform", "rdip"):
            env = self.app.platform.qualify_env(env) or self.app.platform.qualified_env

        if database is not None:
            short_database = os.path.basename(database).split(".")[0].lower()
        else:
            short_database = None

        if dataframes is None:
            dataframes = {}

        if number is None:
            number = ""
        else:
            number = f".{number}"

        # get names
        if service in ("hdfs", "impala"):
            name = f"{service.lower()}.{env.lower()}{number}"
        else:
            # pandas
            name = f"{service.lower()}{number}"

        if self.__handlers__.get(name):
            LOG.debug(f"Ibis handler '{name}' already exists")

            if service == "pandas":
                LOG.debug(f"Updating IbisPandasHandler dataframes")

                handler = self.__handlers__.get(name)
                handler.client.dictionary.update(dataframes)

            return self.__handlers__.get(name)

        handler = self.app.handler.resolve(
            "ibis",
            service,
            setup=True,
            meta_defaults={"name": name, "env": env, "database": short_database},
        )

        # connect
        LOG.debug(f"Ibis handler '{name}' is connecting to {service}")

        if service == "pandas":
            handler.connect(dataframes)
        elif service == "impala":
            hdfs_name = name.replace("impala", "hdfs")
            hdfs = self.app.handler.resolve(
                "ibis",
                "hdfs",
                setup=True,
                meta_defaults={"name": hdfs_name, "env": env},
            )
            hdfs.connect()
            self.__handlers__[hdfs_name] = hdfs
            handler.connect(hdfs)
        else:
            handler.connect()

        self.__handlers__[name] = handler

        return handler

    def remove(self, name):
        name = name.lower()
        self.get(name).close()
        self.__handlers__.pop(name)

    def get(self, name):
        name = name.lower()
        handler = self.__handlers__.get(name)

        if handler is None:
            raise exc.FrameworkError(f"Ibis handler '{name}' does not exists")

        return handler


def ibis_extend_app(app):
    app.extend("ibis", IbisManager(app))


def ibis_cleanup(app):
    app.ibis.close()


def load(app):
    app.interface.define(IbisInterface)

    app.handler.register(IbisPandasHandler)
    app.handler.register(IbisHDFSHandler)
    app.handler.register(IbisImpalaHandler)

    app.hook.register("post_setup", ibis_extend_app)
    app.hook.register("pre_close", ibis_cleanup)
