"""
Deciding what content to render based on GET request
"""
import re
from data import db
from typing import Literal
from fetch import check_login_credentials

OK_HEADER = "HTTP/1.1 200 OK\r\n\r\n"
USR_PW_FMT = r"/?username=(\S*)&password=(\S*)"

def route_traffic(path: str, db_conn: db, salt: str):
    """
    Routing GET requests

    Parameters
    ----------
    path : str
        Path desired from GET request.
    db_conn : db
        Connection to server database
    salt : str
        Salt string for when login is attempted

    Returns
    -------
    bytes
        To return for request.
    """
    # login attempt will be this format
    login = re.findall(USR_PW_FMT, path)

    # main landing page
    if path in ["/", "/index"]:
        with open('../pages/index.html', 'r', encoding='utf-8') as file:
            content = file.read()
        return (OK_HEADER + content).encode("utf-8")
    # landing page css file
    elif path == "/styles.css":
        with open("../styles/styles.css", "rb") as css_file:
            content = css_file.read()
        header = make_content_header("text/css", len(content))
        return header + content
    # icon for browser tab
    elif path == "/favicon.ico":
        with open("../png_files/icon_sn.png", "rb") as icon:
            content = icon.read()
        header = make_content_header("image/png", len(content))
        return header + content
    # login not empty means this request is a login attempt
    elif login:
        items = login[0]
        result = check_login_credentials(items[0], items[1], db_conn, salt)
        # return home page if valid, failed login if not
        if result == 'valid':
            next_page = "../pages/home_page.html"
        else:
            next_page = "../pages/failed_login.html"
        # send bytes of proper page
        with open(next_page, "r", encoding='utf-8') as file:
            content = file.read()
        return (OK_HEADER + content).encode('utf-8')
    else:
        return

def make_content_header(
        content_type: Literal['text/css','image/png'],
        content_length: int
    ) -> str: 
    """
    Creates header for image/css content.

    Parameters
    ----------
    content_type : Literal['text/css','image/png']
        Type of content to render
    content_length : int
        Size of data in bytes.

    Returns
    -------
    bytes
        To send in request.
    """
    binary_header = (
        f"{OK_HEADER[:-2]}"
        f"Content-Type: {content_type}\r\n" 
        f"Content-Length: {content_length}"
        "Connection: close\r\n\r\n"
    ).encode("utf-8")
    return binary_header