import logging
import pdb
import socket
from functools import wraps
import time
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def retry(except_ls, retries=0, delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cur_retries = retries
            while True:
                cur_retries -= 1
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if e.__class__ in except_ls and cur_retries >= 0:
                        logging.info("retrying...")
                        time.sleep(delay)
                    else:
                        raise

        return wrapper

    return decorator


def debugger(sock):
    os.dup2(sock.fileno(), sys.stdin.fileno())
    os.dup2(sock.fileno(), sys.stdout.fileno())
    os.dup2(sock.fileno(), sys.stderr.fileno())

    handler = sock.makefile("rw")
    rdb = pdb.Pdb(stdin=handler, stdout=handler)
    return rdb


def remote_pdb(addr: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.bind((addr, port))
    sock.listen(1)

    logging.info("Waiting for remote debugger to attach..")
    (clientsocket, address) = sock.accept()
    logging.info(f"Connected debugger from {address[0]}:{address[1]}")
    return debugger(clientsocket)


@retry(except_ls=[ConnectionRefusedError], retries=3)
def remote_pdb_reverse(addr: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info(f"Connecting to remote debugger by reverse proxy: {addr}:{port} ")
    sock.connect((addr, port))
    logging.info(f"Connected to remote debugger by reverse proxy: {addr}:{port} ")
    return debugger(sock)
