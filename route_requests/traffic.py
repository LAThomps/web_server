import os
import re
from data import db
from fetch import check_login_credentials

OK_HEADER = "HTTP/1.1 200 OK\r\n\r\n"
USR_PW_FMT = r"/?username=([A-Za-z_0-9+]+)&password=([A-Za-z_0-9+]+)"

def route_traffic(path: str, db_conn: db):
    login = re.findall(USR_PW_FMT, path)
    if path in ["/", "/index"]:
        with open('index.html', 'r', encoding='utf-8') as file:
            content = file.read()
        return (OK_HEADER + content).encode("utf-8")
    elif path == "/styles.css":
        with open("styles.css", "rb") as css_file:
            content = css_file.read()
        header = make_content_header("text/css", len(content))
        return header + content
    elif path == "/favicon.ico":
        with open("icon_sn.png", "rb") as icon:
            content = icon.read()
        header = make_content_header("image/png", len(content))
        return header + content
    elif login:
        items = login[0]
        result = check_login_credentials(items[0], items[1], db_conn)
        print(f"login result: {result}")
        if result == 'valid':
            next_page = "home_page.html"
        else:
            next_page = "failed_login.html"
        with open(next_page, "r", encoding='utf-8') as file:
            content = file.read()
        return (OK_HEADER + content).encode('utf-8')
    else:
        return

def make_content_header(
        content_type: str,
        content_length: int
    ) -> str: 
    binary_header = (
        f"{OK_HEADER[:-2]}"
        f"Content-Type: {content_type}\r\n" 
        f"Content-Length: {content_length}"
        "Connection: close\r\n\r\n"
    ).encode("utf-8")
    return binary_header