"""Probe only a configured trusted LAN interface; never infer API health from a port."""
import http.client
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import stat
import subprocess
import threading
import time

POLICY = Path('/etc/argos/lan-access.json')
PRIVATE = tuple(map(ipaddress.ip_network, ('10.0.0.0/8','172.16.0.0/12','192.168.0.0/16')))


def bound_health(host, port, interface):
    connection = http.client.HTTPConnection(host, port, timeout=2)
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.settimeout(2)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, interface.encode()+b'\0')
    def abort():
        try: transport.shutdown(socket.SHUT_RDWR)
        except OSError: pass
        transport.close()
    watchdog=threading.Timer(2,abort);watchdog.daemon=True
    started=time.monotonic()
    try:
        watchdog.start();transport.connect((host,port));connection.sock=transport
        connection.request('GET','/health',headers={'Accept':'application/json','Connection':'close'})
        response=connection.getresponse();raw=response.read(65537)
        if response.status!=200 or len(raw)>65536 or time.monotonic()-started>=2:raise ValueError('Invalid health')
        return json.loads(raw)
    finally:
        watchdog.cancel()
        if watchdog.ident is not None:watchdog.join(timeout=.1)
        connection.close();transport.close()


def probe_lan(path=POLICY, *, addresses=None, health=bound_health):
    result={'url':'','state':'unavailable','last_verified':0,'observed_at':time.time(),
            'provenance':'trusted_interface+bound_http_health:argos'}
    try:
        fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    except FileNotFoundError:
        return None
    except OSError:
        return {**result,'reason':'invalid_lan_policy'}
    try:
        with os.fdopen(fd,'rb') as stream:
            info=os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_uid!=0 or info.st_mode&0o022 or info.st_size>8192:raise ValueError('Invalid policy')
            policy=json.loads(stream.read(8193))
        interface=policy['interface'];network=ipaddress.ip_network(policy['trusted_subnet']);port=policy['lan_port']
        if (not isinstance(interface,str) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,32}',interface)
                or network.version!=4 or not any(network.subnet_of(n) for n in PRIVATE)
                or type(port) is not int or not 1024<=port<=65535):raise ValueError('Invalid policy')
        if addresses is None:
            proc=subprocess.run(['ip','-json','addr','show','dev',interface],capture_output=True,text=True,check=True,timeout=2)
            if len(proc.stdout)>65536:raise ValueError('Invalid interface data')
            addresses=json.loads(proc.stdout)
        candidates=[]
        for device in addresses[:8]:
            if device.get('ifname')!=interface:continue
            for row in device.get('addr_info',[])[:16]:
                if row.get('family')!='inet' or row.get('scope')!='global':continue
                address=ipaddress.ip_address(row['local'])
                if address in network and address not in (network.network_address,network.broadcast_address):candidates.append(str(address))
        if not candidates:return {**result,'reason':'no_address_on_trusted_lan'}
        # One interface's bounded primary address; no scanning or stale fallback.
        host=candidates[0];result['url']=f'http://{host}:{port}'
        body=health(host,port,interface)
        if not isinstance(body,dict) or body.get('ok') is not True or body.get('ready') is not True:raise ValueError('Protocol not ready')
        return {**result,'state':'available','last_verified':time.time()}
    except (OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError,http.client.HTTPException):
        return {**result,'reason':'lan_health_unavailable'}
