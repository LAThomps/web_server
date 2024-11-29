"""
Module for accessing back end data
"""
from typing import Literal
from data import db
import hashlib 

def check_login_credentials(
        user_name: str,
        password: str,
        db_obj: db,
        salt: str
    ) -> Literal['valid', 'no_user', 'invalid']:
    # print(f"checking creds of {user_name, password}")
    user_info = db_obj.qry(f"""
        SELECT
            Password
        FROM
            mini_social.users
        WHERE
            UserName = '{user_name}'
    """)
    if user_info.empty:
        return 'no_user'
    pw = user_info['Password'][0]
    entry_hashed = hashlib.sha256(bytes(salt + password, 'utf-8')).hexdigest()
    valid = pw == entry_hashed
    if valid:
        return 'valid'
    else:
        return 'invalid'
