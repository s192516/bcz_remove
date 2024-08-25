
import requests
import time
from typing import Union
from src.utility import print_function_name
class BCZ:

    @print_function_name
    def __init__(self, config):

        self.get_daka_info = "https://group.baicizhan.com/group/information?shareKey={}" # 小班打卡信息
        self.own_groups_info = "https://group.baicizhan.com/group/own_groups?uniqueId={}"
        self.remove_member_url = "https://group.baicizhan.com/group/remove_members"


        self.default_headers = {
            "Connection": "keep-alive",
            "User-Agent": "bcz_app_android/7060100 android_version/12 device_name/DCO-AL00 - HUAWEI",
            "Accept": "*/*",
            "Origin": "",
            "X-Requested-With": "",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        self.default_cookie = {
            "access_token": "",
            "client_time": "",
            "app_name": "7060100",
            "bcz_dmid": "2a16dfbb",
            "channel": "qq",
            # device_id 应根据access_token使用哈希唯一确定
            "device_id": "",
            "device_name": "android/DCO-AL00-HUAWEI",
            "device_version": "12",
            "Pay-Support-H5": "alipay_mob_client"
        }
        self.hash_rmb = {}
        self.config = config
        self.logger = config.logger





    @print_function_name
    def getHeaders(self, token: str = '') -> dict:
        '''获取请求头'''
        # TODO 实际上不同域名请求有细微差别，这里暂时只使用默认
        if (not token):
            token = self.config.main_token

        current_headers = self.default_headers.copy()

        if token not in self.hash_rmb:
            # 使用哈希函数计算字符串的哈希值
            hash_value = hash(token)
            # 将哈希值转换为unsigned long long值，然后取反，再转换为16进制字符串
            hex_string = format((~hash_value) & 0xFFFFFFFFFFFFFFFF, '016X')
            self.hash_rmb[token] = {'hex_string': hex_string }

        current_cookie = self.default_cookie.copy()
        current_cookie['device_id'] = f'{self.hash_rmb[token]["hex_string"]}'
        current_cookie['access_token'] = token
        current_cookie['client_time'] = str(int(time.time()))
        current_headers['Cookie'] = ''
        for key, value in current_cookie.items():
            key = key.replace(";","%3B").replace("=","%3D")
            value = value.replace(";","%3B").replace("=","%3D")
            current_headers['Cookie'] += f'{key}={value};'
        return current_headers



    @print_function_name
    def get_member_list(self, share_key: str) -> list:
        '''获取小班成员列表'''
        url = self.get_daka_info.format(share_key)
        headers = self.getHeaders()
        main_response = requests.get(url, headers=headers, timeout=5)

        # if main_response.status_code == 200:
        #     return response.json()['data']
        # else:
        #     self.logger.error(f'获取小班成员列表失败: {response.json()}')
        #     return []

        if main_response.status_code != 200 or main_response.json().get('code') != 1:
            msg = f'获取分享码为{share_key}的小班信息失败! 小班不存在或主授权令牌无效'
            self.logger.error(f'{msg}\n{main_response.text}')
            print(msg)
            return []
        res = main_response.json()
        data = res['data']['members']

        return data


    @print_function_name
    def get_share_keys(self, bcz_id: int) -> list:
        url = self.own_groups_info.format(bcz_id)
        headers = self.getHeaders()
        main_response = requests.get(url, headers=headers, timeout=5)
        if main_response.status_code != 200 or main_response.json().get('code') != 1:
            msg = f'使用主授权令牌获取{bcz_id}的小班信息失败! 小班不存在或id无效'
            self.logger.error(f'{msg}\n{main_response.text}')
            print(msg)
            return []
        res = main_response.json()
        data = res['data']['list']

        return data


    @print_function_name
    def remove_member(self, share_key: str, bcz_id, member_id, nickname: str, token: str) -> Union[dict, None]:
        url = self.remove_member_url
        headers = self.getHeaders(token)
        data = {
            "shareKey":share_key,
            "memberIds": [member_id ]
        }

        main_response = requests.post(url, headers=headers, json=data, timeout=5)

        if main_response.status_code != 200 or main_response.json().get('code') != 1:

            msg = f"移除用户{bcz_id},{nickname}失败!"
            self.logger.error(f'{msg}\n{main_response.text}')
            print(msg)
            return

        return
