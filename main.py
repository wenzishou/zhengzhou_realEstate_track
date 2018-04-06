#-*- coding:utf-8 -*-

import sys, os
import datetime
import main_process
import json
start_url = 'http://www.mizhai.com/'
write_dir = ''
if __name__ == '__main__':
    left_url = set()
    visited_url = set()
    time_str = datetime.datetime.now().strftime('%Y%m%d')
    write_file = os.path.join(write_dir, time_str)
    file_obj = open(write_file, 'a')
    
    #生成种子
    seed = main_process.generate_seed_url(start_url)
    left_url = left_url | seed

    while len(left_url) > 0:
        to_url = left_url.pop()
        if to_url in visited_url:
            continue
        info, ref_url = main_process.collect_info(to_url)
        print(type(json.dumps(info, encoding="UTF-8", ensure_ascii=False).encode('utf-8')))
        file_obj.write((json.dumps(info, encoding="UTF-8", ensure_ascii=False).encode('utf-8')) + '\n')
        left_url = left_url | ref_url
        visited_url.add(to_url)
        print(len(left_url), len(visited_url))
