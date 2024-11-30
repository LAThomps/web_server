"""
Database connection abtraction for server
"""
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError, ResourceClosedError
import pandas as pd
from typing import Literal
import importlib

class db:
    """
    Database connection object
    """
    def __init__(
            self,
            user: str = 'root',
            password: str | None = None,
            dialect: Literal['mysql', 'sqlite'] = 'mysql',
            driver: Literal['pymysql'] = 'pymysql',
            host: str = 'localhost',
            port: int = 3306,
            database: str | None = None,
            filepath: str | None = None
        ):
        """
        Parameters
        ----------
        user: str
            Username for database. The default is `root`.
        password: str | None
            Password for said user. Default is None.
        dialect: Literal['mysql','sqlite']
            DB dialect, only built for mysql/sqlite now. The default is `mysql`.
        driver: Literal['pymysql']
            Driver for dialect. The defualt is `pymysql`.
        host: str
            IP for where database is being served. The default is `localhost`.
        port: int
            Port for where database is being served. The default is 3306.
        database: str | None
            Database in program you want to use. The default is None.
        filepath: str | None
            Filepath to SQLite file if specified. The default is None.
        """
        # url for sqlalchemy connection
        if dialect == 'sqlite':
            self.url = rf"sqlite:///{filepath}"
        elif dialect == 'mysql':
            self.url = rf"{dialect}+{driver}://{user}:{password}@{host}:{port}{f'/{database}' if database else ''}"
        else:
            print(f"""
invalid dialect `{dialect}` parameter must be one of ['mysql','sqlite']
            """)
            self = None 
            return
        # check packages 
        try:
            for lib in ['pymysql']:
                test = importlib.import_module(lib)
        except ModuleNotFoundError:
            print(f"""
{lib} not installed in runtime environment, not connecting to db
            """)
            return
        # attempt database connection
        try:
            # sqlalchemy engine object
            self.engine = create_engine(self.url)

            # test connection
            temp_conn = self.engine.connect()
            temp_conn.close()
        # exceptions here can be for an error in one of the inputs. Recommend
        # troubleshooting separately to get correct problems.
        except Exception as e:
            print(f"""
unable to connect to database based on inputs:
dialect:\t{dialect}
driver:\t\t{driver}
user:\t\t{user}
password:\t***** (always hidden)
host:\t\t{host}
port:\t\t{port}

error:{e}
**verify your application data matches your input args**
            """)
           
    def qry(self, sql_str: str):
        """
        General query abstraction method.

        Parameters
        ----------
        sql_str : str
            Query as python string.

        Returns
        -------
        DataFrame | None
            Result of query. Empty dataframe if nothing returned, and None if
            the query did not execute.
        """
        with self.engine.connect() as connection:
            try:
                result = connection.execute(text(sql_str))
                connection.commit()
                try:
                    columns = list(result.keys())
                    data = result.fetchall()
                    df = pd.DataFrame(data=data, columns=columns)
                    return df 
                except ResourceClosedError:
                    return pd.DataFrame()
            except ProgrammingError as pe:
                print(pe)
    
    