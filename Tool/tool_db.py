import sqlite3

class  DB:
    _DATABASE_URL = r".\db\product.db"

    # # 将游标获取的Tuple根据数据库列表转换为dict
    # def make_dicts(cursor, row):
    #     return dict((cursor.description[i][0], value) for i, value in enumerate(row))

    #获取数据库（建立数据库连接）
    def get_db():
        db=sqlite3.connect(DB._DATABASE_URL)
        return db

    #关闭数据库连接
    def close_connection():
        DB.get_db().close()

    #执行sql语句不返回结果
    def execute_sql(sql,prms=()):
        c=DB.get_db().cursor()
        c.execute(sql,prms)
        c.connection.commit()
        DB.close_connection()

    #执行用于选择数据的sql
    def query_sql(sql,prms=(),single_strip=False):
        c=DB.get_db().cursor()
        if single_strip is False:
            datas=c.execute(sql,prms).fetchall()
            DB.close_connection()
            return datas
        else:
            data=c.execute(sql,prms).fetchone()
            DB.close_connection()
            return data


