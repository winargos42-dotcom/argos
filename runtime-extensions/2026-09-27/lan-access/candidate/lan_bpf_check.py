"""Fail closed unless systemd's socket has directly attached ingress and egress BPF filters.

Read-only Linux BPF_PROG_QUERY; never creates or changes a firewall program.
"""
import ctypes
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

class Query(ctypes.Structure):
    _fields_=[('target_fd',ctypes.c_uint32),('attach_type',ctypes.c_uint32),
              ('query_flags',ctypes.c_uint32),('attach_flags',ctypes.c_uint32),
              ('prog_ids',ctypes.c_uint64),('prog_cnt',ctypes.c_uint32),('padding',ctypes.c_uint32),
              ('prog_attach_flags',ctypes.c_uint64),('link_ids',ctypes.c_uint64),
              ('link_attach_flags',ctypes.c_uint64),('revision',ctypes.c_uint64)]

def check(unit):
    if not re.fullmatch(r'[A-Za-z0-9_-]+\.socket',unit):raise ValueError('Invalid socket unit')
    result=subprocess.run(['systemctl','show',unit,'--property=ControlGroup','--value'],capture_output=True,text=True,check=True,timeout=3)
    group=result.stdout.strip()
    if not group.startswith('/system.slice/') or '..' in group:raise ValueError('Socket cgroup unavailable')
    path=Path('/sys/fs/cgroup')/group.lstrip('/')
    number={'x86_64':321,'aarch64':280}.get(platform.machine())
    if number is None:raise ValueError('Unsupported BPF query architecture')
    libc=ctypes.CDLL(None,use_errno=True)
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY)
    try:
        for attach in (0,1):  # BPF_CGROUP_INET_INGRESS / EGRESS
            programs=(ctypes.c_uint32*64)()
            query=Query(target_fd=fd,attach_type=attach,query_flags=0,
                        prog_ids=ctypes.addressof(programs),prog_cnt=64)
            result=libc.syscall(number,16,ctypes.byref(query),ctypes.sizeof(query))
            if result!=0 or query.prog_cnt<1:raise ValueError('Required socket IP filter unavailable')
    finally:os.close(fd)
    return True

if __name__=='__main__':
    try:check(sys.argv[1])
    except Exception:
        print('ARGOS LAN start refused: socket IP filters are not verified',file=sys.stderr)
        raise SystemExit(1)
