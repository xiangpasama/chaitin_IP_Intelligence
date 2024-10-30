#!/usr/bin/python3

import requests
from datetime import datetime
import time

# 单独提取的 sk 参数
sk="**********"

def get_ip_info(ip):
    url = f"https://ip-0.rivers.chaitin.cn/api/share/s?sk={sk}&ip={ip}"
    response = requests.get(url)
    data = response.json()
    
    if data['success']:
        ip_info = data['data']['ip_info']
        events = data['data']['events']
        
        # 提取IP地理位置和ISP信息
        ip_location = f"{ip_info['ip']}, {ip_info['address']['country']}, {ip_info['address']['province']}, {ip_info['address']['city']}, {ip_info['address']['isp']}"
        
        # 提取IP情报标签
        ip_tags = ip_info['tags']
        
        # 提取最近一次攻击时间
        if events:
            latest_attack_time = events[0]['create_at']
            latest_attack_time_str = datetime.utcfromtimestamp(latest_attack_time).strftime('%Y-%m-%d %H:%M:%S')
        else:
            latest_attack_time_str = "N/A"
        
        # 返回结果
        result = {
            'ip_location': ip_location,
            'ip_tags': ip_tags,
            'latest_attack_time': latest_attack_time_str
        }
        return result
    else:
        return None

def process_ip_list(ip_list):
    results = []
    for ip in ip_list:
        ip_info = get_ip_info(ip)
        if ip_info:
            results.append(ip_info)
        # 每次请求后暂停60秒
        time.sleep(60)
    return results

# 示例IP清单
ip_list = [
    '61.189.159.186', 
    '61.158.236.41',
    '110.249.201.70'
]

# 处理IP清单
results = process_ip_list(ip_list)

# 打印结果
for result in results:
    print(f"IP地理位置: {result['ip_location']}")
    print(f"IP情报标签: {result['ip_tags']}")
    print(f"最近一次攻击时间: {result['latest_attack_time']}")
    print("-" * 40)