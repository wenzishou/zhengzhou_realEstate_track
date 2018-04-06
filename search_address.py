#-*- coding:utf-8 -*-

import sys, os
import datetime
import main_process
import json
import math
import heapq
reload(sys)
sys.setdefaultencoding("utf-8")
search_addr = " 郑东新区   平安大道东风南路向东1000米路南（东风渠熊耳河交汇处）" 
def loc_ip_dist(ip_dict1, ip_dict2):
    try:
        lat_abs = math.fabs(ip_dict1['lat'] - ip_dict2['lat'])
        lng_abs = math.fabs(ip_dict1['lng'] - ip_dict2['lng'])
        ip_abs = math.sqrt(math.pow(lat_abs,2) + math.pow(lng_abs,2))
        return ip_abs * 111
    except Exception as e:
        print(e)
        return 1000000000

if __name__ == '__main__':
    read_file = '20180406'
    file_obj = open(read_file)
    heap = [] 
    search_addr_ip = main_process.get_location(search_addr)
    print(search_addr_ip)
    for _i in file_obj.readlines():
        info_dict = eval(_i)
        try:
            cur_ip = info_dict['loc_ip'] 
            dist = loc_ip_dist(cur_ip, search_addr_ip)
            heapq.heappush(heap, (dist, _i))
        except:
            print(_i)
            continue
    
    while True:
        _pop_ele = heapq.heappop(heap)
        if _pop_ele[0] > 5:
            break
        print("%f\t%s" % (_pop_ele[0], _pop_ele[1]))
