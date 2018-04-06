#-*- coding:utf-8 -*-
import sys, os
import datetime
import requests
from bs4 import BeautifulSoup
import logging
import re

root_url = 'http://www.mizhai.com/'
ADDR = '河南省郑州市'
def get_id_info(url):
    """
    url, id
    """
    ret = {}
    ret['url'] = url
    id = url.split('/')[-1].split('.')[0]
    ret['id'] = id
    return ret

def get_key_info(root_tag):
    """
    楼盘名
    """
    ret = {}
    try:
        select_res = root_tag.select('h3')
        name = select_res[0].get_text().encode('utf-8').split('\n')[0]
        ret['name'] = name.strip()
    except:
        return None
    return ret

def get_next_url(root_tag):
    """
    取得外链接
    """
    ret_set = set()
    match_re = r'/loupan/\d{2,10}.html'
    maybe_list = root_tag.select('a')
    for _list in maybe_list:
        try:
            href = _list['href']
            if None != re.match(match_re, href):
                if href not in ret_set:
                    ret_set.add(href)
        except:
            continue
    return ret_set


def get_location(address):
    """
    获取坐标信息
    """
    try:
        address = address.encode('utf-8')
        full_addr = ADDR + address
        key = 'GjG3XAdmywz7CyETWqHwIuEC6ZExY6QT'
        url = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak=%s&address=' % (key)
        url += full_addr
        r = dict(requests.get(url).json())
        loc_ip = r['result']['location']
        return loc_ip
    except Exception as e:
        print(e)
    return {'lat':0, 'lng':0}

def get_base_info(root_tag):
    """
    获取楼盘基本信息
    #售价，价格说明，最新开盘，交房时间，地址，建筑类型，楼盘特色，主力户型，    
    #售价，交房时间，地址    
    input: 获取的原始网页html
    output: {}
    """
    loupan_info = root_tag.select('.loupan-info')
    if(1 != len(loupan_info)):
        logging.error("wrong loupan_info size. need 1, get %d" % len(loupan_info))
        return NULL
    ret = {}
    loupan_info = loupan_info[0]
    #得到具体的信息单元，如价格等
    sub_attri_tag = loupan_info.select('li')
    for _sub_tag in sub_attri_tag:
        sub_attri_key_tag = _sub_tag.select('b') #属性key
        if(1 != len(sub_attri_key_tag)):
            continue
        sub_attri_key_tag = sub_attri_key_tag[0]
        if ('售价') == sub_attri_key_tag.get_text().encode('utf-8'):
            if 'price' not in ret.keys():
                ret['price'] = {}
            sub_attr_val_ = _sub_tag.select('span')
            for _i in sub_attr_val_:
                var_str_list = _i.get_text().split() #高层或洋房，价格，单位
                house_type = var_str_list[0].strip()
                try:
                    house_price = int(var_str_list[1])
                    ret['price'][house_type] = house_price
                except:
                    house_price = -1
                    ret['price'][house_type] = -1 
        elif '地址' == sub_attri_key_tag.get_text().encode('utf-8'):
            if 'address' not in ret.keys():
                ret['address'] = ''
            sub_attr_val = _sub_tag.select('span')
            addr = sub_attr_val[0].get_text().strip()
            ret['address'] = addr 
            loc_ip = get_location(addr)
            ret['loc_ip'] = loc_ip
        else:
            continue
    return ret

def generate_seed_url(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text)
    seed = get_next_url(soup)
    return seed

def collect_info(url):
    result = dict()
    ref_url = set()
    des_url = root_url + url
    wb_data = requests.get(des_url)
    soup = BeautifulSoup(wb_data.text)
    #print(soup)
    try:
        ref_url = get_next_url(soup)
        result.update(get_id_info(des_url))  #url id
        result.update(get_key_info(soup)) #name ...
        result.update(get_base_info(soup)) #base info
    except:
        #print('* ' * 100)
        print("url", url)
        #print('soup', soup)
    return result, ref_url

if __name__ == '__main__':
    url = 'http://www.mizhai.com/loupan/1588.html'
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text)
    print(get_next_url(soup))
    ret = get_base_info(soup)
    for item in ret.keys():
        print(item)
        print(ret[item])
