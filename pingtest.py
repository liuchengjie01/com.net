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
    b = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')    # 正则表达式匹配出ip地址
    r = [  b.findall(x) for x in r ]
    for x in r:
        if x != []:
            ip_list.append(''.join(x))
    del ip_list[0]       # 删除第一个出现的ip，第一个是终点ip不需要
    return ip_list


def pingtest(ip):

    a = 'ping -n 100 '+ip
    r = os.popen(a)
    str = r.read()
    str1 =str.split('%')[0]      # 用%切片寻得丢包率
    packet_loss = str1.split('(')[1]      # 用（二次切片获得具体丢包率数值
    num = str.rfind('=')       # =最后一次出现的地方，找到平均延迟
    delay = str[num+2:-1]      # 取得具体延迟
    if packet_loss == '100':
        delay = '>=9999ms'

    print ("The packets loss is %s%%" % packet_loss)
    print ('The average delay is %s' % delay)


def ippostion(ip):

    url = 'http://ip-api.com/json/'+ip
    position_raw = urllib.request.urlopen(url)     # 拼接ip查询网址
    position_raw1 = position_raw.read()
    position = json.loads(position_raw1)       # 将返回序列化为一个json
    if position['status'] == 'fail':        # status为fail即查询失败，此ip无法定位
        print ("The IP %s can't be located" % ip)
        return 0
    else:
        latitude = position['lat']
        longtitude = position['lon']
        result = "{long},{lat}".format(long=longtitude, lat=latitude)    # 将经度，纬度用逗号分开保存
        return result


def textposition(location):
    param = {'location': location, 'key': 'f2b9b398253662afbfa0da1278f5e864'}
    url = 'http://restapi.amap.com/v3/geocode/regeo'
    res = requests.get(url,param)      # 拼接查询物理地名的网址
    response = res.json()
    if response['status'] == '1':      # status为1表示查询成功
        return response['regeocode']['formatted_address']   # 返回精确物理地址


def visualposition(la_lo_position = []):   # 接受ip对应经纬度地址的list作为参数
    key_str = ''
    for pos in range(len(la_lo_position)):
        key = "[{position}],".format(position=la_lo_position[pos])
        key_str = key_str + key         # 拼接成为html中的字段
    key_str = key_str.strip(',')        # 删除末尾多的一个逗号
    str1 = '''<!doctype html>
<html lang="zh-CN">

<head>
    <!-- 原始地址：//webapi.amap.com/ui/1.0/ui/misc/PathSimplifier/examples/expand-path.html -->
    <base href="http://webapi.amap.com/ui/1.0/ui/misc/PathSimplifier/examples/" />
    <meta charset="utf-8">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no, width=device-width">
    <title>动态延展路径</title>
    <style>
    html,
    body,
    #container {
        width: 100%;
        height: 100%;
        margin: 0px;
    }
    </style>
</head>

<body>
    <div id="container"></div>
    <script type="text/javascript" src='http://webapi.amap.com/maps?v=1.4.13&key=f2b9b398253662afbfa0da1278f5e864'></script>
    <!-- UI组件库 1.0 -->
    <script src="http://webapi.amap.com/ui/1.0/main.js?v=1.0.11"></script>
    <script type="text/javascript">
    //创建地图
    var map = new AMap.Map('container', {
        zoom: 4
    });

    AMapUI.load(['ui/misc/PathSimplifier', 'lib/$'], function(PathSimplifier, $) {

        if (!PathSimplifier.supportCanvas) {
            alert('当前环境不支持 Canvas！');
            return;
        }

        var pathSimplifierIns = new PathSimplifier({
            zIndex: 100,
            autoSetFitView: false,
            map: map, //所属的地图实例

            getPath: function(pathData, pathIndex) {

                return pathData.path;
            },
            getHoverTitle: function(pathData, pathIndex, pointIndex) {

                if (pointIndex >= 0) {
                    //point 
                    return pathData.name + '，点：' + pointIndex + '/' + pathData.path.length;
                }

                return pathData.name + '，点数量' + pathData.path.length;
            },
            renderOptions: {

                renderAllPointsIfNumberBelow: 100 //绘制路线节点，如不需要可设置为-1
            }
        });

        window.pathSimplifierIns = pathSimplifierIns;

        var myPath = ['''

    str2 = '''],
            endIdx = 0,
            data = [{
                name: '动态路线',
                path: myPath.slice(0, 1)
            }];

        pathSimplifierIns.setData(data);

        //对第一条线路（即索引 0）创建一个巡航器
        var navg1 = pathSimplifierIns.createPathNavigator(0, {
            loop: true, //循环播放
            speed: 1000 //巡航速度，单位千米/小时
        });

        function expandPath() {

            function doExpand() {

                endIdx++;

                if (endIdx >= myPath.length) {
                    return false;
                }

                var cursor = navg1.getCursor().clone(), //保存巡航器的位置
                    status = navg1.getNaviStatus();


                data[0].path = myPath.slice(0, endIdx + 1);
                pathSimplifierIns.setData(data); //延展路径


                //重新建立一个巡航器
                navg1 = pathSimplifierIns.createPathNavigator(0, {
                    //loop: true, //循环播放
                    speed: 600000 //巡航速度，单位千米/小时
                });

                if (status !== 'stop') {
                    navg1.start();
                }

                //恢复巡航器的位置
                if (cursor.idx >= 0) {
                    navg1.moveToPoint(cursor.idx, cursor.tail);
                }

                return true;
            }

            if (doExpand()) {

                setTimeout(expandPath, 1000);
            }
        }

        
        navg1.start();

        expandPath();
    });
    </script>
</body>

</html>'''
    htmltext = "{0}{1}{2}".format(str1, key_str, str2)  # 拼接三个字符串为一个完整的HTML
    return htmltext


if __name__=='__main__':
  # t_ip=sys.argv[1]
    t_ip=input("The test IP/domain name is ")

    iplist = []              # iplist保存追踪路由的ip地址列表
    la_lo_position = []      # la_lo_position保存ip对应经纬度列表（无空）
    la_lo_position1 = []     # la_lo_position1保存ip对应经纬度列表（有空）
    text_pos = []            # text_pos保存物理地址列表

    pingtest(t_ip)
    iplist = tracert(t_ip)

    for ip in iplist:
        la_lo_position1.append(ippostion(ip))

    for count in range(len(la_lo_position1)):       # 此步骤是为了剔除经纬度列表中的空，因为空在地图中无法显示
        if la_lo_position1[count] != 0:
            la_lo_position.append(la_lo_position1[count])   # 由ip得经纬度

    for ip_p in la_lo_position1:
        text_pos.append(textposition(ip_p))    # 由经纬度得物理地址

    fo = open("routermap.html", "w", encoding="utf-8")
    str = visualposition(la_lo_position)       # 将经纬度列表转化为高德地图路径显示
    fo.write(str)

    for ip in range(len(iplist)):
        print (iplist[ip],text_pos[ip])        # 将ip和对应位置输出




