"""The existing durable engine in its own systemd resource slice."""
import argparse
import fcntl
import json
import os
import signal
import time
from .core import Core,ROOT
from .memory import Memory
from .missions import Missions


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--config',required=True);args=parser.parse_args()
    lock=open(ROOT/'runtime/mission-worker.lock','w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    os.environ['JARVIS_WORKLOAD_CLASS']='mission'
    config=json.loads(open(args.config).read());config['compute_role']='mission'
    memory=Memory(ROOT/'runtime/memory.sqlite');core=Core(config,memory)
    missions=Missions(core,ROOT,start_worker=True,recover_exclusive=True)
    def stop(signum,frame):missions.stop.set()
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    while not missions.stop.wait(1):pass
    # Stop dispatch, let a current bounded inference/tool finish its receipt.
    while core.missions.execution_core.lock.locked():time.sleep(.2)
    lock.close()

if __name__=='__main__':main()
