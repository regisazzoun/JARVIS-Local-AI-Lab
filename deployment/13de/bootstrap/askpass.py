#!/usr/bin/env python3
"""OpenSSH askpass: password through inherited environment FILE PATH, never argv."""
if not __debug__:
    raise RuntimeError('STOP: optimized Python disables safety assertions')
import os,pathlib,stat,sys
p=pathlib.Path(os.environ['JARVIS_BOOTSTRAP_SECRET'])
s=p.stat()
if not stat.S_ISREG(s.st_mode) or s.st_mode & 0o077 or s.st_uid != os.getuid():sys.exit(1)
sys.stdout.write(p.read_text().rstrip('\n')+'\n')
