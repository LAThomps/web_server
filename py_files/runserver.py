"""
Main module for running the web server
"""
import argparse
import socket
from socket import socket as Socket
from concurrent.futures import ThreadPoolExecutor
import time
import os
from dotenv import load_dotenv
from data import db
from typing import Literal
from route_requests import route_traffic

# make sure the username/password of your database, and 
# salt used for each password
load_dotenv("../.env")

# can change port if you want, will need sudo privileges on linux
HOST = "127.0.0.1"
PORT = 80

# change this to whatever you call the database the `users` table is stored
DATABASE_NAME = "mini_social"

# connection to the database
DB_CONN = db(
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PW"),
    database=DATABASE_NAME
)

# hash salt and path to where your server log should be
SALT = os.getenv("MINI_SOCIAL_SALT")
LOG_PATH = "../logs/server_log.txt"

def main():
    # parse the args
    parser = create_parser()
    args = parser.parse_args()

    # set number of threads for connections, log of requests
    global MAX_THREADS, EXECUTOR, log
    MAX_THREADS = int(args.threads)
    EXECUTOR = ThreadPoolExecutor(max_workers=MAX_THREADS)
    log = []

    # start up server for time passed as arg
    start_server(
        duration=int(args.timeout),
        unit=args.unit_of_time
    )

    # write server logs (modify handle_client function to add content to logs)
    if os.path.isfile(LOG_PATH):
        os.remove(LOG_PATH)
    with open(LOG_PATH, "w") as log_file:
        for req in log:
            log_file.write("\n__new_request__\n")
            for line in req:
                log_file.write(f"{line}\n")
    
    # end server run
    print("server down")

def handle_client(
        client_socket: Socket, 
        client_address: tuple
    ) -> None:
    """
    Function for handling the client request.

    Parameters
    ----------
    client_socket : Socket
        Socket object for client.
    client_address : tuple
        Address of client.
    """
    # could add this to the log, info is there already though
    print(f"Connection established with {client_address}")

    # turn bits to parsable text
    request = client_socket.recv(1024).decode("utf-8").split("\r\n")
    log.append(request)

    # read request, develop response and send
    response = parse_request(request)
    client_socket.sendall(response)
    client_socket.close()

def parse_request(request: str) -> bytes:
    """
    Parsing the client HTTP request.

    Parameters
    ----------
    request : str
        Client's request as string.

    Returns
    -------
    bytes
        Bytes to send back to client
    """
    # first element will tell you type of request
    action = request[0]
    actions = action.split()

    # to handle empty request (Chrome does this sometimes)
    if not actions:
        return "HTTP/1.1 404 Not Found\r\n\r\n"
    # typical GET request
    elif actions[0] == 'GET':
        # function for normal GET requests, send 404 for anything else
        response = route_traffic(actions[1], DB_CONN, SALT)
        if response:
            return response
        else:
            return f"{actions[-1]} 404 Not Found\r\n\r\n"
    else:
        return "HTTP/1.1 404 Not Found\r\n\r\n"


def start_server(
        duration: int, 
        unit: Literal['s', 'min']
    ) -> None:
    """
    Function for starting/running webserver

    Parameters
    ----------
    duration : int
        Length of time server is up per user input.
    unit : Literal['s', 'min']
        Unit of time for the duration, also per terminal argument.
    """
    # basic Berkeley sockets syntax per Python socket lib
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(20)
        print("server listening on port 80...")

        # keep track of time server is up
        start = time.time()
        interval = duration if unit == 's' else duration * 60
        end = start + interval

        # run until time is up, one thread for each request
        while True:
            if time.time() > end:
                break
            conn, addr = s.accept()
            future = EXECUTOR.submit(handle_client, conn, addr)
        
        # shut down all threads for server stop
        EXECUTOR.shutdown(wait=False)
        return

def create_parser():
    """
    Creating argument parser for module

    Returns
    -------
    ArgumentParser
        Parser object for module to use.
    """
    parser = argparse.ArgumentParser(description="Web Server")
    parser.add_argument('timeout', help="duration to run server")
    parser.add_argument(
        'unit_of_time',
        choices=['min','s'],
        default='s',
        help='server timeout'
    )
    parser.add_argument("threads", help="how many threads to run")
    return parser

if __name__ == '__main__':
    main()