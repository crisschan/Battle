import sqlite3
import base64

class SQLiteHelper(object):
    connected = False
    __conn = None

    def __init__(self, db_path):
        try:
            self.__conn = sqlite3.connect(db_path)
            self.__conn.row_factory = sqlite3.Row
            self.connected = True
        except sqlite3.Error as e:
            print(f'数据库连接失败: {e}')

    def insert(self, table, val_obj):
        keys = ', '.join(val_obj.keys())
        placeholders = ', '.join(['?'] * len(val_obj))
        sql = f'INSERT INTO {table} ({keys}) VALUES ({placeholders})'
        try:
            with self.__conn:
                cursor = self.__conn.execute(sql, tuple(val_obj.values()))
            return cursor.lastrowid
        except sqlite3.Error as e:
            print({e, sql})
            return False

    def insert_many(self, table, params, all_data):
        keys = ', '.join(params)
        placeholders = ', '.join(['?'] * len(params))
        sql = f'INSERT INTO {table} ({keys}) VALUES ({placeholders})'
        try:
            with self.__conn:
                self.__conn.executemany(sql, all_data)
            return True
        except sqlite3.Error as e:
            print({e, sql})
            return False

    def update(self, table, val_obj, range_str):
        set_clause = ', '.join([f"{key} = ?" for key in val_obj.keys()])
        sql = f'UPDATE {table} SET {set_clause} WHERE {range_str}'
        try:
            with self.__conn:
                cursor = self.__conn.execute(sql, tuple(val_obj.values()))
            return cursor.rowcount
        except sqlite3.Error as e:
            print({e, sql})
            return False

    def delete(self, table, range_str):
        sql = f'DELETE FROM {table} WHERE {range_str}'
        try:
            with self.__conn:
                cursor = self.__conn.execute(sql)
            return cursor.rowcount
        except sqlite3.Error as e:
            print({e, sql})
            return False

    # def select_one(self, table, factor_str, field='*'):
    #     sql = f'SELECT {field} FROM {table} WHERE {factor_str}'
    #     try:
    #         cursor = self.__conn.execute(sql)
    #         return dict(cursor.fetchone())
    #     except sqlite3.Error as e:
    #         print({e, sql})
    #         return False
    # 查询唯一数据在数据表中
    def select_one(self,sql):
        try:
            cursor = self.__conn.execute(sql)
            return dict(cursor.fetchone())
        except sqlite3.Error as e:
            print({e, sql})
            return False
    # def select_more(self, table, range_str, field='*'):
    #     sql = f'SELECT {field} FROM {table} WHERE {range_str}'
    #     try:
    #         cursor = self.__conn.execute(sql)
    #         return [dict(row) for row in cursor.fetchall()]
    #     except sqlite3.Error as e:
    #         print({e, sql})
    #         return False
    # 查询多条数据在数据表中
    def select_more(self,sql):
        # sql = 'SELECT ' + field + ' FROM ' + table + ' WHERE ' + range_str
        try:
            cursor = self.__conn.execute(sql)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            return False
    def count(self, table, range_str='1=1'):
        sql = f'SELECT COUNT(*) FROM {table} WHERE {range_str}'
        try:
            cursor = self.__conn.execute(sql)
            return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print({e, sql})
            return False

    def sum(self, table, field, range_str='1=1'):
        sql = f'SELECT SUM({field}) AS res FROM {table} WHERE {range_str}'
        try:
            cursor = self.__conn.execute(sql)
            return cursor.fetchone()['res']
        except sqlite3.Error as e:
            print({e, sql})
            return False

    def query(self, sql):
        try:
            cursor = self.__conn.execute(sql)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(str(e))
            return False

    def __del__(self):
        if self.__conn:
            self.__conn.close()

    def close(self):
        self.__del__() 