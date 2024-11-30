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
    """
    Checking login credentials

    Parameters
    ----------
    user_name: str
        User input on login page.
    password: str
        User input on login page.
    db_obj: db
        Database object to query.
    salt: str
        String used to make passwords even more secure. This must be the same
        string used to hash any passwords in the database on insert.
    
    Returns
    -------
    Literal['valid', 'no_user', 'invalid']
        String that shows result of user validation
    """
    # query database
    user_info = db_obj.qry(f"""
        SELECT
            Password
        FROM
            users
        WHERE
            UserName = '{user_name}'
    """)

    # for users not in the database yet
    if user_info.empty:
        return 'no_user'
    
    # hash input password
    entry_hashed = hashlib.sha256(bytes(salt + password, 'utf-8')).hexdigest()

    # grab what the password should hash to
    pw = user_info['Password'][0]

    # compare, return proper result
    valid = pw == entry_hashed
    if valid:
        return 'valid'
    else:
        return 'invalid'
