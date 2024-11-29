from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError, ResourceClosedError
import pandas as pd
from typing import Literal
import importlib

class db:
    # change these args to match your default db connection
    # TODO: modify to be able to handle sqlite connections (or others w/ url)
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
        except ModuleNotFoundError as mnfe:
            print(f"""
{lib} not installed in runtime environment, not connecting to db
            """)
            return
        try:
            self.engine = create_engine(self.url)
            # test connection
            temp_conn = self.engine.connect()
            temp_conn.close()
            self._dbs = tuple(self.qry("SHOW DATABASES;")['Database'])
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
           
    def qry(self, sql_str):
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
    
    # def show_dbs(self):
    #     return self._dbs

    # def table_info(self, table_str: str):
    #     try:
    #         result = self.qry(f"SHOW COLUMNS FROM {table_str};")
    #         return result
    #     except:
    #         return f"table '{table_str}' not found"
    