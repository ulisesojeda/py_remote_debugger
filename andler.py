import logging
import pdb
import socket

logging.basicConfig()


def retry(func, except_ls, retries=0):
    if retries < 0:
        return
    try:
        func()
    except Exception as e:
        if e in except_ls:
            retry(func, except_ls, retries=retries-1)

def retry(except_ls, retries=0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[LOG] {msg}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def debugger(sock):
    handler = sock.makefile("rw")
    db = pdb.Pdb(stdin=handler, stdout=handler)
    return db

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
def remote_pdb_reverse_proxy(addr: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info(f"Connecting to remote debugger by reverse proxy: {addr}:{port} ")
    sock.connect((addr, port))
    logging.info(f"Connected to remote debugger by reverse proxy: {addr}:{port} ")
    return debugger(sock)


def main():
    db = remote_pdb_reverse_proxy("10.30.12.18", 4444)
    db = remote_pdb_reverse_proxy("localhost", 4444)
    val = 10
    y = 22
    print(1)
    print(2)
    print(3)
    db.set_trace()
    print(4)
    db.set_trace()
    print("Done")


if __name__ == "__main__":
    main()
