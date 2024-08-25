# from src.config import Config
#
# config = Config()
# # 解析小班
#
# def split_group(groups: str) -> list:
#
#
#     groups = groups.replace(" ", "")
#     groups = groups.strip()
#     groups = groups.split('+')
#
#
#     group_infos = []
#
#     for group in groups:
#         group_info = config.idx2info.get(group, "")
#         if group_info == "":
#             print(f"输入内容{groups}有误,请重新输入")
#         else:
#             group_infos.append(group_info)
#     return group_infos

from src.config import Config
config = Config()


def safe_encode(s: str, encoding='gbk') -> str:
    return s.encode(encoding, 'ignore').decode(encoding)


def print_function_name(func):
    def wrapper(*args, **kwargs):
        # config.logger(f"Function name: {func.__name__}")
        config.logger.debug(f"Function name: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper