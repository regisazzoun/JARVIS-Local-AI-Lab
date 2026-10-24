"""The existing durable engine in its own systemd resource slice."""
import argparse
import fcntl
import json
import os
import signal
import time
from contextlib import contextmanager
from .core import Core,ROOT
from .memory import Memory
from .missions import Missions


@contextmanager
def worker_locks(root,slot=None):
    if slot is not None and slot<1:raise ValueError('Worker slot must be positive')
    runtime=root/'runtime';runtime.mkdir(parents=True,exist_ok=True)
    with (runtime/'mission-worker-mode.lock').open('a') as mode:
        fcntl.flock(mode, (fcntl.LOCK_SH if slot else fcntl.LOCK_EX)|fcntl.LOCK_NB)
        path=runtime/('mission-worker-'+str(slot)+'.lock' if slot else 'mission-worker.lock')
        with path.open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            yield


def run(config_path,slot):
    os.environ['JARVIS_WORKLOAD_CLASS']='mission'
    config=json.loads(open(config_path).read());config['compute_role']='mission'
    memory=Memory(ROOT/'runtime/memory.sqlite');core=Core(config,memory)
    # Parallel slots never reset another live worker's mission. SQLite claims and
    # heartbeats arbitrate tasks; slot1 owns the single publication loop.
    missions=Missions(core,ROOT,start_worker=True,recover_exclusive=slot is None,start_publisher=slot in (None,1))
    def stop(signum,frame):missions.stop.set()
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    while not missions.stop.wait(1):pass
    # Stop dispatch, let a current bounded inference/tool finish its receipt.
    while core.missions.execution_core.lock.locked():time.sleep(.2)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--config',required=True);parser.add_argument('--slot',type=int);args=parser.parse_args()
    with worker_locks(ROOT,args.slot):run(args.config,args.slot)

if __name__=='__main__':main()
