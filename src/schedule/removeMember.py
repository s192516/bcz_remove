
import threading
from src.config import Config
import sqlite3
from datetime import datetime, date
import time
from src.bcz import BCZ
from src.schedule.groupRules import GroupRules
from src.utility import safe_encode
from src.utility import print_function_name


groupRules = GroupRules()


class RemoveMember:

    @print_function_name
    def __init__(self, config: Config, sqlite: sqlite3, bcz: BCZ) -> None:

        self.config = config
        self.logger = config.logger
        self.sqlite = sqlite
        self.bcz = bcz
        self.remove_member()

    @print_function_name
    def read_pulil(self, group_info: dict) -> str:

        grades = group_info['pupil']
        res = ""
        for p in grades:
            if p == "一年级": res += "一年级, "
            if p == "二年级": res += "二年级, "
            if p == "三年级": res += "三年级, "
            if p == "四年级": res += "四年级, "
            if p == "五年级": res += "五年级, "
            if p == "六年级": res += "六年级, "
        return res

    @print_function_name
    def print_watch_groups_info(self, group_info: dict):

        self.logger.info(f"*************{datetime.now().strftime('%H:%M:%S')}开始扫描{group_info['name']}***************")
        print(f"*************{datetime.now().strftime('%H:%M:%S')}开始扫描{group_info['name']}***************")
        start = time.time()

        grades = self.read_pulil(group_info)


        self.logger.info(f' 监督班级: {group_info["name"]}, '
                         f'踢人标准满卡{group_info["completedTimes"]}天, '
                            f'晚卡时间{group_info["daka_time"]}点, '
                         f'拒绝{grades}小学生, '
                         f'每隔{self.config.remove_member_interval_seconds}秒执行一次' )

        print(f' 监督班级: {group_info["name"]}, '
                         f'踢人标准满卡{group_info["completedTimes"]}天, '
                         f'晚卡时间{group_info["daka_time"]}点, '
                         f'拒绝{grades}小学生, '
                         f'每隔{self.config.remove_member_interval_seconds}秒执行一次' )


    @print_function_name
    def check_pulil(self, member: dict, group_info) -> bool:
        # self.logger.debug(" 进入check_pulil函数")

        is_pulil = False

        for p in group_info["pupil"]:
            if p in member['bookName']:
                is_pulil = True

        return is_pulil

    @print_function_name
    def pre_check(self, member: dict, bcz_id: int, whitelist: set, blacklist: set, group_info: dict) -> bool:


        # 是否合格	小班名字	百词斩ID	用户名	日期	时间	备注	小班1	打卡数据	小班2	打卡数据	小班3	打卡数据	小班4	打卡数据	小班5	打卡数据	小班6	打卡数据


        groupname = group_info['name']
        need_continue_check = True
        if member['durationDays'] > 1:
            need_continue_check = False
        elif (bcz_id in whitelist.get(groupname, set() ) )or (bcz_id in whitelist.get("全部", set())):
            need_continue_check = False
        elif bcz_id in blacklist:
            need_continue_check = False
            reason = "黑名单"
            self.bcz.remove_member(group_info['share_key'], member['uniqueId'],  member['id'], member['nickname'], group_info['token'])

            data = ["删除", groupname, bcz_id, member['nickname'], date.today(), datetime.now().strftime('%H:%M:%S'), reason]
            self.sqlite.add_auto_purge(data)

        elif self.check_pulil(member, group_info):
            need_continue_check = False
            reason = "小学生"
            data = ["删除", groupname, bcz_id, member['nickname'], date.today(), datetime.now().strftime('%H:%M:%S'), reason]

            self.bcz.remove_member(group_info['share_key'], member['uniqueId'],  member['id'], member['nickname'], group_info['token'])
            self.sqlite.add_auto_purge(data)
        return need_continue_check

    def check_daka_result(self, memberlist: list, bcz_id: int, group_info: dict) -> tuple:

        is_qualified = False
        reason = ""
        complete_duration_days = ""
        for member in memberlist:
            if member['uniqueId'] == bcz_id: #
                max_completedTimes = member['completedTimes']
                max_durationDays = member['durationDays']
                daka_time = member['completedTime']
                is_daka = "是" if daka_time != 0 else "否"

                is_qualified, res = (eval(f"groupRules.check_{group_info['group_name']}")
                                     (max_completedTimes, max_durationDays, is_daka, group_info, daka_time))

                reason += res
                complete_duration_days = str(max_completedTimes) + r"/" + str(max_durationDays)

                if is_qualified == True:
                    reason = "符合要求保留"
                break
        return is_qualified, reason, complete_duration_days




    def check_from_bcz(self, bcz_id: int, group_info: dict) -> tuple:

        is_qualified = True
        reason = "符合要求保留"

        groups_member_info = self.bcz.get_share_keys(bcz_id)
        for info in groups_member_info:
            info['name'] = safe_encode(info['name'])


        complete_duration_info = []
        for info in groups_member_info:
            share_key = info["shareKey"]
            group_name = info["name"]

            members_list = self.bcz.get_member_list(share_key)

            for member in members_list:
                member['nickname'] = safe_encode(member['nickname'])


            is_qualified , reason, complete_duration_days = self.check_daka_result(members_list, bcz_id, group_info)
            complete_duration_info.append(group_name)
            complete_duration_info.append(complete_duration_days)
            if is_qualified: break

        return is_qualified, reason, complete_duration_info


    @print_function_name
    def check_each_member(self, group_members: list, group_info: dict, whitelist: set, blacklist: set):

        group_name = group_info["name"]


        for member in group_members:
            bcz_id = member['uniqueId']  # 查看类型, 今后统一为int
            member_id = member['id']
            nickname = member['nickname']

            need_next_check = self.pre_check(member, bcz_id, whitelist, blacklist, group_info)
            if not need_next_check:

                continue


            self.logger.info("正在审查: " + group_info['name'] +  "  " + safe_encode(nickname ))
            print("正在审查: " + group_info['name'] +  "  " + nickname )

            is_qualified, reason, complete_duration_info = self.check_from_bcz(bcz_id, group_info)

            if not is_qualified:

                s7 = time.time()
                self.bcz.remove_member(group_info['share_key'], bcz_id, member_id, nickname, group_info['token'])
                s8 = time.time()
                self.logger.info(f'删除成员耗时{s8 - s7:.2f}秒')
                print(f'删除成员耗时{s8 - s7:.2f}秒')

            if is_qualified:
                whitelist[group_name].add(bcz_id)
                data = [bcz_id, nickname, group_name, date.today()]
                self.sqlite.add_whitelist( data )
                self.config.logger.info( f"{nickname}审查结果合格" )
                print( f"{nickname}审查结果合格" )

            res = "保留" if is_qualified else "删除"
            data = [res, group_name, bcz_id, nickname, date.today(), datetime.now().strftime('%H:%M:%S'), reason] + complete_duration_info
            self.sqlite.add_auto_purge(data)


    @print_function_name
    def check_group(self, group_info: list, whitelist: set, blacklist: set):

        start = time.time()

        self.print_watch_groups_info(group_info)
        share_key = group_info["share_key"]

        self.logger.info(f"正在获取小班成员信息")
        print(f"正在获取小班成员信息")
        s1 = time.time()

        group_members = self.bcz.get_member_list( share_key)
        for member in group_members:
            member['nickname'] = safe_encode(member['nickname'])



        e1 = time.time()
        self.logger.info(f"获取小班成员信息耗时{e1-s1:.2f}秒")
        print(f"获取小班成员信息耗时{e1-s1:.2f}秒")

        self.check_each_member(group_members, group_info, whitelist, blacklist)

        end = time.time()
        self.logger.info(f'扫描一个班耗时{end - start:.2f}秒')
        print(f'扫描一个班耗时{end - start:.2f}秒')
        self.logger.info(f"*************{datetime.now().strftime('%H:%M:%S')} {group_info['name']}扫描完成***************")
        print(f"*************{datetime.now().strftime('%H:%M:%S')} {group_info['name']}扫描完成***************")




    @print_function_name
    def get_whitelist_blacklist(self):
        whitelist, whitelist_name = self.sqlite.get_whitelist()
        blacklist = self.config.get_blacklist()

        for groupname, username in whitelist_name.items():
            self.logger.info(f" {groupname} 白名单成员: {username}")
            print(f" {groupname} 白名单成员: {username}")

        self.logger.info(f"黑名单成员共{len(blacklist)}人")
        print(f"黑名单成员共{len(blacklist)}人")

        return whitelist, blacklist

    @print_function_name
    def start_remove_member(self):


        # watch_groups_info = self.config.watch_groups_info

        watch_groups_info = self.config.get_watch_groups_info()

        whitelist, blacklist = self.get_whitelist_blacklist()

        self.logger.info("开始新一轮扫描, 正在获取小班成员信息")
        print("开始新一轮扫描, 正在获取小班成员信息")

        for group_info in watch_groups_info:
            self.check_group(group_info, whitelist, blacklist)


    @print_function_name
    def remove_member(self):

        self.logger.info(f"-----------开始踢人----------")
        print(           f"-----------开始踢人----------")

        # change_setting = True
        # while change_setting:
        #     n = input(f"是否修改设置, 按1修改程序等待时间, 按2修改监督小班, 按3修改小班踢人标准, 按4添加白名单")
        #
        #     if n == "1":
        #         seconds = input("请输入秒数")
        #         try:
        #             seconds = int(seconds)
        #             self.config.remove_member_interval_seconds = seconds
        #         except:
        #             print(f"输入内容{seconds}有误, 请输入纯数字")
        #     elif n == "2":
        #         watch_groups = input("请输入监督小班, 用+号分隔")
        #         groups_info = split_group(watch_groups)
        #
        #     elif n == "4":
        #
        #         bczId = input("请输入白名单成员ID")
        #         try:
        #             bczId = int(bczId)
        #
        #             user_info = bcz.get_user_info(bczId)
        #             name = user_info.get("name", "")
        #
        #             print(f"是否添加{bczId} {name}到白名单, 按回车确定, 按esc取消")
        #             result = self.wait_for_keypress
        #             if result:
        #                 print(f"已添加{bczId} {name}到白名单")
        #
        #         except:
        #             print(f"输入内容{bczId}有误, 请输入纯数字")
        self.start_remove_member()

        remove_member_interval_seconds = self.config.remove_member_interval_seconds
        threading.Timer(interval = remove_member_interval_seconds, function=self.remove_member).start()
        self.logger.info(f"-----------运行结束, 等待{self.config.remove_member_interval_seconds}秒开始下一轮----------")
        print(f"-----------运行结束, 等待{self.config.remove_member_interval_seconds}秒开始下一轮----------")

