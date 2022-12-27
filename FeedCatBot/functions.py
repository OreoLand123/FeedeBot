import sqlite3
import time
import re

conect = sqlite3.connect("db_feed_count.db")
cur = conect.cursor()

def db(table_name):
    sqlite_select_query = f"""SELECT * from {table_name}"""
    cur.execute(sqlite_select_query)
    records = cur.fetchall()
    return records


def list_bd_feed(flag):
    list_name = []
    records = db("feed_count")
    if flag:
        for i in records:
            list_name.append(i)
        list_name = [i[1] for i in list_name]
        return list_name
    else:
        for i in records:
            list_name.append(i)
        list_name = [i[1] + " " + str(i[-2]) + "/" + str(i[-1]) for i in list_name]
        return list_name


def cheak_db_anction(num, name_feed, flag):
    records = db("feed_count")
    list_count = [i for i in records]
    if flag == True:
        for i in list_count:
            if name_feed in i:
                if num <= i[4] and num > 0:
                    return True
                else:
                    res = str(i[3]) + "/" + str(i[4])
                    return res

    elif flag == None:
        for i in list_count:
            if name_feed in i:
                if num <= i[4]:
                    time.sleep(4)
                    cur.execute('UPDATE feed_count SET remainder = ?   WHERE ID = ?', (i[4] - num, i[0],))
                    conect.commit()
                    return True
                else:
                    return False
    else:
        for i in list_count:
            if name_feed in i:
                return i[2]


def db_title(call):
    index = call[-1]
    records = db("feed_count")
    list_title = [i for i in records]
    for i in list_title:
        if int(index) == i[0]:
            return f"{i[1]}:\n{i[2]}"



def number_cheak(number):
    if len(re.findall(r'\+7\d{10}', number)) and len(number) == 12:
        return True
    else:
        return False

def db_register(name, tg_name, tg_id, number):
    cur.execute(f"INSERT INTO user (tg_id, tg_name, name, number) VALUES (?, ?, ?, ?)", [tg_id, f"@{tg_name}", name, number])
    conect.commit()

def get_userdata(tg_id):
    date = list(cur.execute("SELECT name, tg_name, number FROM user WHERE tg_id = ?", [tg_id]).fetchall())
    return '\n\n'.join(date)
