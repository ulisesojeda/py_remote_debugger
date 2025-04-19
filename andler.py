import os
import socket
import logging

from retry import retry

logging.basicConfig()

def replace_file_descriptors(handler):
    os.close(0)
    os.close(1)
    os.close(2)
    os.dup(handler)
    os.dup(handler)
    os.dup(handler)


def remote_pdb(addr: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.bind((addr, port))
    sock.listen(1)

    print("Waiting for remote debugger to attach..")
    (clientsocket, address) = sock.accept()
    print(f"Connected debugger from {address[0]}:{address[1]}")
    handler = clientsocket.fileno()
    replace_file_descriptors(handler)


@retry(ConnectionRefusedError, tries=3, delay=7)
def remote_pdb_reverse_proxy(addr: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Connecting to remote debugger by reverse proxy: {addr}:{port} ")
    sock.connect((addr, port))
    print(f"Connected to remote debugger by reverse proxy: {addr}:{port} ")
    handler = sock.fileno()
    replace_file_descriptors(handler)


def main():
    val = 10
    y = 22
    print(1)
    print(2)
    print(3)
    breakpoint()
    print(4)
    breakpoint()
    print("Done")


if __name__ == "__main__":
    #remote_pdb("localhost", 4444)
    remote_pdb_reverse_proxy("10.30.0.38", 4444)
    main()
