import sqlite3
import time

def db():
    conect = sqlite3.connect("db_feed_count.db")
    cur = conect.cursor()
    sqlite_select_query = """SELECT * from feed_count"""
    cur.execute(sqlite_select_query)
    records = cur.fetchall()
    return records

def list_bd_feed(flag):
    list_name = []
    records = db()
    if flag == True:
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
    conect = sqlite3.connect("db_feed_count.db")
    cur = conect.cursor()
    sqlite_select_query = """SELECT * from feed_count"""
    cur.execute(sqlite_select_query)
    records = cur.fetchall()
    list_count = [i for i in records]
    if flag == True:
        for i in list_count:
            if name_feed in i:
                if num <= i[4]:
                    return True
                else:
                    res = str(i[3]) + "/" + str(i[4])
                    return res

    elif flag == None:
        for i in list_count:
            if name_feed in i:
                if num <= i[4]:
                    time.sleep(4)
                    cur.execute('UPDATE feed_count SET remainder = ?  WHERE ID = ?', (i[4] - num, i[0],))
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
    records = db()
    list_title = [i for i in records]
    for i in list_title:
        if int(index) == i[0]:
            return f"{i[1]}:\n{i[2]}"



def number_cheak(number):
    if number == None:
        return None
    try:
        number = int(number)
        number = str(number)
        if ([0] == "+" and [1] == "7" and len(number) > 10) or (([0] == "7" or [0] == "8") and len(number) == 11) or len(number) < 10 or len(number) > 10:
            return False
        else:
            return True
    except ValueError:
        return False
