#-*- coding:utf-8 -*-
import os
import urllib.request
import json
import requests
import re
import sys


def tracert(ip):
    a='tracert '+ip
    r=os.popen(a).readlines()
    ip_list=[]
    b = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    r = [  b.findall(x) for x in r ]
    for x in r:
        if x != []:
            ip_list.append(''.join(x))
    del ip_list[0]
    print (ip_list)
    return ip_list


def pingtest(ip):

    a = 'ping -n 20 '+ip
    r = os.popen(a)
    str = r.read()
    str1 =str.split('%')[0]
    packet_loss = str1.split('(')[1]
    num = str.rfind('=')
    delay = str[num+2:-1]
    if packet_loss == '100':
        delay = '>=9999ms'

    print ("The packet loss is %s%%" % packet_loss)
    print ('The average delay is %s' % delay)


def ippostion(ip):

    url = 'http://ip-api.com/json/'+ip
    position_raw = urllib.request.urlopen(url)
    position_raw1 = position_raw.read()
    position = json.loads(position_raw1)
    if position['status'] == 'fail':
        print ("This IP %s can't be located" % ip)
        return False
    else:
        latitude = position['lat']
        longtitude = position['lon']
        result = "{long},{lat}".format(long=longtitude, lat=latitude)
        return result


def textposition(location):
    param = {'location': location, 'key': 'f2b9b398253662afbfa0da1278f5e864'}
    url = 'http://restapi.amap.com/v3/geocode/regeo'
    res = requests.get(url,param)
    response = res.json()
    print (response['regeocode']['formatted_address'])

# def visualposition(location):


if __name__=='__main__':
    t_ip=sys.argv[1]
    #pingtest(t_ip)
    iplist=tracert(t_ip)
    la_lo_position = []
    text_pos = []
    for ip in iplist:
        if ippostion(ip) != 0:
            la_lo_position.append(ippostion(ip))
    '''for ip_p in la_lo_position:
        text_pos.append(text_pos(ip_p))
    for ip in range(len(iplist)):
        print (iplist[ip],text_pos[ip])'''

