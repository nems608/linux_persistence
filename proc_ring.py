#!/usr/bin/python
import os
import time
from multiprocessing import Process, Array
import psutil
from setproctitle import *
import random

def proc_exists(pid):
    try:
        p = psutil.Process(pid)
        dead = p.status() in ['zombie', 'stopped', 'dead']
        return not dead
    except:
        return False

def get_proc_titles():
    names = [p.name() for p in psutil.process_iter()]
    return names

def watch_and_write(idx, arr):
    arr[idx] = os.getpid()
    names = get_proc_titles()
    name = random.choice(names)
    setproctitle(name)
    print(arr[idx], name)

    # Wait for other procs
    next_idx = (idx+1) % len(arr)
    while arr[next_idx] == 0:
        pass

    while True:
        if idx == 0:
            pass # TODO do something

        next_pid = arr[next_idx]
        if not proc_exists(next_pid):
            p = Process(target=watch_and_write, args=(next_idx, arr))
            p.start()

        time.sleep(0.5)

if __name__ == '__main__':
    arr = Array('i', [0]*5)
    for i in range(len(arr)):
        p = Process(target=watch_and_write, args=(i, arr))
        p.start()
    os.kill(os.getpid(), 15)
