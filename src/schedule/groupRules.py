import time
from src.utility import print_function_name
class GroupRules:

    def __init__(self):


        pass

    @print_function_name
    def check_shujiang(self, max_completedTimes, max_durationDays, is_daka, group_info, daka_time):



        ruler_completedTimes = group_info['completedTimes']
        lasted_daka_time = group_info['daka_time'] if group_info['daka_time'] != -1 else 25

        # 将时间戳转换为时间元组
        time_tuple = time.localtime(daka_time)

        # 从时间元组中提取出小时
        daka_hour = time_tuple.tm_hour

        qualified = True
        reason = ""
        if max_completedTimes < ruler_completedTimes:
            qualified = False
            reason += "最长打卡天数不足, "
        if max_completedTimes / max_durationDays  < group_info['rate']:
            qualified = False
            reason += "打卡率不满足要求, "


        if daka_time == 0:
            # 没打卡并且超过最晚打卡时间
            qualified = False
            reason += "没打卡就进班, "
        elif  daka_hour >= lasted_daka_time:
            qualified = False
            reason += "打卡时间超过规定时间, "

        reason = reason.rstrip(", ")
        return qualified, reason


    @print_function_name
    def check_zaoqi(self, max_completedTimes, max_durationDays, is_daka, group_info, daka_time):



        ruler_completedTimes = group_info['completedTimes']
        lasted_daka_time = group_info['daka_time'] if group_info['daka_time'] != -1 else 25

        # 将时间戳转换为时间元组
        time_tuple = time.localtime(daka_time)

        # 从时间元组中提取出小时
        daka_hour = time_tuple.tm_hour

        qualified = True
        reason = ""
        if max_completedTimes < ruler_completedTimes:
            qualified = False
            reason += "最长打卡天数不足, "
        if max_completedTimes / max_durationDays  < group_info['rate']:
            qualified = False
            reason += "打卡率不满足要求, "


        if daka_time == 0:
            # 没打卡并且超过最晚打卡时间
            qualified = False
            reason += "没打卡就进班, "
        elif  daka_hour >= lasted_daka_time:
            qualified = False
            reason += "打卡时间超过规定时间, "

        reason = reason.rstrip(", ")
        return qualified, reason


    @print_function_name
    def check_little_duck(self, max_completedTimes, max_durationDays, is_daka, group_info, daka_time):



        ruler_completedTimes = group_info['completedTimes']
        lasted_daka_time = group_info['daka_time'] if group_info['daka_time'] != -1 else 25

        # 将时间戳转换为时间元组
        time_tuple = time.localtime(daka_time)

        # 从时间元组中提取出小时
        daka_hour = time_tuple.tm_hour

        qualified = True
        reason = ""
        if max_completedTimes < ruler_completedTimes:
            qualified = False
            reason += "最长打卡天数不足, "
        if max_completedTimes / max_durationDays  < group_info['rate']:
            qualified = False
            reason += "打卡率不满足要求, "


        if daka_time == 0:
            # 没打卡并且超过最晚打卡时间
            qualified = False
            reason += "没打卡就进班, "
        elif  daka_hour >= lasted_daka_time:
            qualified = False
            reason += "打卡时间超过规定时间, "

        reason = reason.rstrip(", ")
        return qualified, reason


    @print_function_name
    def check_chong(self, max_completedTimes, max_durationDays, is_daka, group_info, daka_time):



        ruler_completedTimes = group_info['completedTimes']
        lasted_daka_time = group_info['daka_time'] if group_info['daka_time'] != -1 else 25

        # 将时间戳转换为时间元组
        time_tuple = time.localtime(daka_time)

        # 从时间元组中提取出小时
        daka_hour = time_tuple.tm_hour

        qualified = True
        reason = ""
        if max_completedTimes < ruler_completedTimes:
            qualified = False
            reason += "最长打卡天数不足, "
        if max_completedTimes / max_durationDays  < group_info['rate']:
            qualified = False
            reason += "打卡率不满足要求, "


        if daka_time == 0:
            # 没打卡并且超过最晚打卡时间
            qualified = False
            reason += "没打卡就进班, "
        elif  daka_hour >= lasted_daka_time:
            qualified = False
            reason += "打卡时间超过规定时间, "

        reason = reason.rstrip(", ")
        return qualified, reason


    @print_function_name
    def check_bisheng(self, max_completedTimes, max_durationDays, is_daka, group_info, daka_time):



        ruler_completedTimes = group_info['completedTimes']
        lasted_daka_time = group_info['daka_time'] if group_info['daka_time'] != -1 else 25

        # 将时间戳转换为时间元组
        time_tuple = time.localtime(daka_time)

        # 从时间元组中提取出小时
        daka_hour = time_tuple.tm_hour

        qualified = True
        reason = ""
        if max_completedTimes < ruler_completedTimes:
            qualified = False
            reason += "最长打卡天数不足, "
        if max_completedTimes / max_durationDays  < group_info['rate']:
            qualified = False
            reason += "打卡率不满足要求, "


        if daka_time == 0:
            # 没打卡并且超过最晚打卡时间
            qualified = False
            reason += "没打卡就进班, "
        elif  daka_hour >= lasted_daka_time:
            qualified = False
            reason += "打卡时间超过规定时间, "

        reason = reason.rstrip(", ")
        return qualified, reason


    @print_function_name
    def check_dujiang(self, max_completedTimes, max_durationDays, is_daka, group_info, daka_time):



        ruler_completedTimes = group_info['completedTimes']
        lasted_daka_time = group_info['daka_time'] if group_info['daka_time'] != -1 else 25

        # 将时间戳转换为时间元组
        time_tuple = time.localtime(daka_time)

        # 从时间元组中提取出小时
        daka_hour = time_tuple.tm_hour

        qualified = True
        reason = ""
        if max_completedTimes < ruler_completedTimes:
            qualified = False
            reason += "最长打卡天数不足, "
        if max_completedTimes / max_durationDays  < group_info['rate']:
            qualified = False
            reason += "打卡率不满足要求, "


        if daka_time == 0:
            # 没打卡并且超过最晚打卡时间
            qualified = False
            reason += "没打卡就进班, "
        elif  daka_hour >= lasted_daka_time:
            qualified = False
            reason += "打卡时间超过规定时间, "

        reason = reason.rstrip(", ")
        return qualified, reason


    @print_function_name
    def check_moon(self, max_completedTimes, max_durationDays, is_daka, group_info, daka_time):



        ruler_completedTimes = group_info['completedTimes']
        lasted_daka_time = group_info['daka_time'] if group_info['daka_time'] != -1 else 25

        # 将时间戳转换为时间元组
        time_tuple = time.localtime(daka_time)

        # 从时间元组中提取出小时
        daka_hour = time_tuple.tm_hour

        qualified = True
        reason = ""
        if max_completedTimes < ruler_completedTimes:
            qualified = False
            reason += "最长打卡天数不足, "
        if max_completedTimes / max_durationDays  < group_info['rate']:
            qualified = False
            reason += "打卡率不满足要求, "


        if daka_time == 0:
            # 没打卡并且超过最晚打卡时间
            qualified = False
            reason += "没打卡就进班, "
        elif  daka_hour >= lasted_daka_time:
            qualified = False
            reason += "打卡时间超过规定时间, "

        reason = reason.rstrip(", ")
        return qualified, reason


    @print_function_name
    def check_sun(self, max_completedTimes, max_durationDays, is_daka, group_info, daka_time):



        ruler_completedTimes = group_info['completedTimes']
        lasted_daka_time = group_info['daka_time'] if group_info['daka_time'] != -1 else 25

        # 将时间戳转换为时间元组
        time_tuple = time.localtime(daka_time)

        # 从时间元组中提取出小时
        daka_hour = time_tuple.tm_hour

        qualified = True
        reason = ""
        if max_completedTimes < ruler_completedTimes:
            qualified = False
            reason += "最长打卡天数不足, "
        if max_completedTimes / max_durationDays  < group_info['rate']:
            qualified = False
            reason += "打卡率不满足要求, "


        if daka_time == 0:
            # 没打卡并且超过最晚打卡时间
            qualified = False
            reason += "没打卡就进班, "
        elif  daka_hour >= lasted_daka_time:
            qualified = False
            reason += "打卡时间超过规定时间, "

        reason = reason.rstrip(", ")
        return qualified, reason


    @print_function_name
    def check_flower(self, max_completedTimes, max_durationDays, is_daka, group_info, daka_time):



        ruler_completedTimes = group_info['completedTimes']
        lasted_daka_time = group_info['daka_time'] if group_info['daka_time'] != -1 else 25

        # 将时间戳转换为时间元组
        time_tuple = time.localtime(daka_time)

        # 从时间元组中提取出小时
        daka_hour = time_tuple.tm_hour

        qualified = True
        reason = ""
        if max_completedTimes < ruler_completedTimes:
            qualified = False
            reason += "最长打卡天数不足, "
        if max_completedTimes / max_durationDays  < group_info['rate']:
            qualified = False
            reason += "打卡率不满足要求, "


        if daka_time == 0:
            # 没打卡并且超过最晚打卡时间
            qualified = False
            reason += "没打卡就进班, "
        elif  daka_hour >= lasted_daka_time:
            qualified = False
            reason += "打卡时间超过规定时间, "

        reason = reason.rstrip(", ")
        return qualified, reason