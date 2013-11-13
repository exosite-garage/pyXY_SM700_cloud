from datetime import datetime
import os      
import time
import binascii
import snaplib
import httplib
import urllib
import Queue
import threading
from  snapconnect import snap

server = "m2.exosite.com"

def exosite_write(cik,dp_alias,dp_val):
    if len(cik) == 40:
        print 'EXO WRITE: DATAPORT:'+str(dp_alias)+' VALUE:'+str(dp_val)+' DEVICE:'+str(cik)
        _exosite_data_write(cik,dp_alias,dp_val)
    else:
        log.warning('EXO WRITE: Improper CIK: %s' % cik)

def exosite_read(cik,dp_alias,source):
    if len(cik) == 40:
        src = binascii.hexlify('0x'+str(source))
        print 'EXO READ: DATAPORT: '+dp_alias+'  CIK: '+ cik+ '  DEVICE: '+str(src)
        
        result = _exosite_data_read(cik,dp_alias)
        value = urllib.unquote(result.split("=")[1])
        rpc(source,'exositeResponse', dp_alias, value)
        
    else:
        log.warning('EXO READ: Improper CIK: %s' % cik)


def _exosite_data_read(rcik,rdp_alias):
    url = '/api:v1/stack/alias?'+rdp_alias 
    headers = {'Accept':'application/x-www-form-urlencoded; charset=utf-8','X-Exosite-CIK':rcik}
    conn = httplib.HTTPConnection(server) 
    conn.request("GET",url,"",headers) 
    response = conn.getresponse(); 
    print 'response: ' + str(response.status) + str(response.reason)
    data = response.read() 
    end = data.find('<')
    if -1 == end: end = len(data)
    conn.close()
    print data
    return data

def _exosite_data_write(wcik,wdp_alias,wdp_val):
    url = '/api:v1/stack/alias' 
    params = urllib.urlencode({wdp_alias: str(wdp_val)})
    headers = {'X-Exosite-CIK': wcik, 'content-type': 'application/x-www-form-urlencoded; charset=utf-8'} 
    conn = httplib.HTTPConnection(server) 
    conn.request("POST",url,params,headers) 
    response = conn.getresponse(); 
    print 'response: ' + str(response.status) + str(response.reason)
    data = response.read() 
    end = data.find('<')
    if -1 == end: end = len(data)
    conn.close()
    
def nodeLogger(info):
    print(info)