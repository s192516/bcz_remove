

from src.config import Config
import sqlite3
import os
import time
import sys
from typing import Union
import collections
from src.utility import safe_encode, print_function_name
import datetime
from datetime import date, datetime



class SQLite:
    @print_function_name
    def __init__(self, config: Config) -> None:
        self.config = config
        self.logger = config.logger

        self.whitelist = collections.defaultdict(set)
        self.whitelist_name = collections.defaultdict(set)

        self.db_path = config.database_path
        # 是否合格	小班名字	百词斩ID	用户名	日期	时间	备注	小班1	打卡数据	小班2	打卡数据	小班3	打卡数据	小班4	打卡数据	小班5	打卡数据	小班6	打卡数据
        self.init_sql = [
            '''CREATE TABLE IF NOT EXISTS WHITELIST (
                BCZID INTEGER,               ---百词斩ID
                USERNAME TEXT,               ---用户名
                GROUPNAME TEXT,              ---小班名称
                DATE TEXT                    ---有效日期
            )''',

            '''CREATE TABLE IF NOT EXISTS AUTO_PURE (
                REMAIN TEXT,                 ---是否合格
                GROUPNAME TEXT,              ---小班名字
                BCZID INTEGER,               ---百词斩ID
                USERNAME TEXT,               ---用户名
                DATE TEXT,                   ---日期
                TIME TEXT,                   ---时间
                REMARK TEXT,                 ---备注
                GROUP1 TEXT,                 ---小班1
                DAKA1 TEXT,                  ---打卡数据
                GROUP2 TEXT,                 ---小班2
                DAKA2 TEXT,                  ---打卡数据
                GROUP3 TEXT,                 ---小班3
                DAKA3 TEXT,                  ---打卡数据
                GROUP4 TEXT,                 ---小班4
                DAKA4 TEXT,                  ---打卡数据
                GROUP5 TEXT,                 ---小班5
                DAKA5 TEXT,                  ---打卡数据
                GROUP6 TEXT,                 ---小班6
                DAKA6 TEXT                   ---打卡数据
            )'''

        ]

        self.init()

    @print_function_name
    def connect(self, db_path: str = '') -> sqlite3.Connection:
        '''连接数据库，并返回连接态(记得手动关闭)'''
        if not db_path:
            db_path = self.db_path
        try:
            if path := os.path.dirname(db_path):
                os.makedirs(path, exist_ok=True)
            conn = sqlite3.connect(db_path)

            conn.set_trace_callback(lambda statement: self.logger.debug(f'在{db_path}执行SQLite指令: {statement}'))
            # logger.info(f'连接数据库{db_path}成功')
            return conn
        except sqlite3.Error:
            self.logger.error('数据库读取异常...无法正常运行，程序会在5秒后自动退出')
            time.sleep(5)
            sys.exit(0)

    @print_function_name
    def init(self) -> None:
        '''初始化不存在的库'''
        conn = self.connect(self.db_path)
        cursor = conn.cursor()
        for sql in self.init_sql:
            cursor.execute(sql)
            conn.commit()
        conn.close()

    @print_function_name
    def read(self, sql: str, param: Union[list, tuple] = ()) -> list:
        '''SQL执行读数据操作'''
        try:
            conn = self.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql, param)
            result = cursor.fetchall()
            conn.close()
            self.logger.debug( "读取数据库成功")
            self.logger.debug(result)
            return result
        except sqlite3.DatabaseError as e:
            self.logger.error(f'读取数据库{self.db_path}出错: {e}')
            raise e

    @print_function_name
    def write(self, sql: str, param: Union[list, tuple] = ()) -> bool:
        '''SQL执行写数据操作'''
        try:
            conn = self.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql, param)
            conn.commit()
            conn.close()
            # logger.info( "写入数据库成功")
            return True
        except sqlite3.DatabaseError as e:
            self.logger.error(f'写入数据库{self.db_path}出错: {e}')
        return False

    @print_function_name
    def get_whitelist(self) -> set:
        '''获取白名单, result: [(BCZID, USERNAME, GROUPNAME, DATE)]'''
        sql = 'SELECT * FROM whitelist'
        result = self.read(sql)


        # whitelist = collections.defaultdict(set)
        # whitelist_name = collections.defaultdict(set)
        new_member = collections.defaultdict(set)

        for line in result:
            bcz_id = line[0]
            username = safe_encode(line[1])
            groupname = safe_encode(line[2])
            try:
                date1 = datetime.strptime(line[3], "%Y-%m-%d").date()
            except:
                date1 = datetime.strptime("2099-01-01", "%Y-%m-%d").date()
            today = date.today()

            if today <= date1: # 在时效日期之前

                if bcz_id not in self.whitelist[groupname]:
                    new_member[groupname].add(username)

                    self.whitelist[groupname].add(bcz_id)
                    self.whitelist_name[groupname].add(username)
            # else:
            #     msg = f"{groupname}的{username}, id为{bcz_id}的白名单资格已过期"
            #     self.config.logger.info( msg  )
            #     print(  msg )




        return self.whitelist, self.whitelist_name, new_member



    @print_function_name
    def add_auto_purge(self, data: list) -> bool:
        '''添加自动清除记录'''
        columns = ['REMAIN', 'GROUPNAME', 'BCZID', 'USERNAME', 'DATE', 'TIME', 'REMARK',
                   'GROUP1', 'DAKA1', 'GROUP2', 'DAKA2','GROUP3', 'DAKA3',
                   'GROUP4', 'DAKA4', 'GROUP5', 'DAKA5','GROUP6', 'DAKA6']
        placeholders = ', '.join(['?'] * len(data))
        columns_str = ', '.join(columns[:len(data)])
        sql = f'INSERT INTO AUTO_PURE ({columns_str}) VALUES ({placeholders})'

        self.write(sql, tuple(data))


    @print_function_name
    def add_whitelist(self, data: list):

        sql = f'INSERT INTO WHITELIST (BCZID, USERNAME, GROUPNAME, DATE) VALUES (?, ?, ?, ?)'
        self.write(sql, data)

