import sqlite3
from datetime import datetime
from time import sleep

def create_connect():
    connect = sqlite3.connect("bot_bd.db")
    cursor = connect.cursor()
    return connect, cursor


def speed():
    con, cur = create_connect()
    cur.execute("PRAGMA synchronous = OFF")
    con.commit()
    con.close()


def create_connect_friend():
    connect = sqlite3.connect("bot_bd_friends.db")
    cursor = connect.cursor()
    return connect, cursor


def create_new_user(ids, pill=False):
    current_datetime = datetime.now()
    date = " ".join(str(datetime.now().date()).split("-"))
    time = " ".join(str(datetime.now().time()).split(".")[0].split(":")[:2]) 
    con, cur = create_connect()
    while True:
        try:
            check = cur.execute(f"SELECT time_start FROM users WHERE user_id={ids}").fetchall()
            break
        except:
            pass
    if not check:
        if pill:
            while True:
                try:
                    cur.execute(f"INSERT INTO users(user_id, time_start, pills) VALUES({ids}, '{date + ' ' + time}', 2)")
                    break
                except:
                    pass
        else:
            while True:
                try:
                    cur.execute(f"INSERT INTO users(user_id, time_start) VALUES({ids}, '{date + ' ' + time}')")
                    break
                except:
                    pass
        con.commit()
        con.close()
        return True

    else:
        return False



def infected_user(ids):
    con, cur = create_connect()
    while True:
        try:
            result = cur.execute(f"SELECT count_infected, pills, kits, elixir FROM users WHERE user_id={ids}").fetchall()
            break
        except:
            pass
    count = result[0][0] + 1
    list_count = list(result[0][1:])

    if count % 3 == 0:
        while True:
            try:
                cur.execute(f"""UPDATE users SET count_infected={count}, kits={list_count[1] + 1},
                                                                        pills={list_count[0] + 1}  
                
                                WHERE user_id={ids}""")
                break
            except:
                pass
    elif count % 5 == 0:
        while True:
            try:
                cur.execute(f"""UPDATE users SET count_infected={count}, elixir={list_count[2] + 1},
                                                                        pills={list_count[0] + 1}
                
                                WHERE user_id={ids}""")
                break
            except:
                pass
    else:
        while True:
            try:
                cur.execute(f"""UPDATE users SET count_infected={count}, pills={list_count[0] + 1}
                                WHERE user_id={ids}""")
                break
            except:
                pass
    con.commit()
    con.close()
    

def get_life_time(time):
    day = time // 60 // 24
    if day != 0:
        time -= 24 * 60 * day
        hours = time // 60
    else:
        hours = time // 60

    if hours != 0:
        time -= 60 * hours
        minut = time
    else:
        minut = time

    time = [day, hours, minut]
    return time


def get_statistic(ids):
    con, cur = create_connect()
    while True:
        try:
            result = cur.execute(f"SELECT pills, elixir, kits, count_infected, time_life FROM users WHERE user_id={ids}").fetchall()[0]
            break
        except:
            pass
    time = get_life_time(result[4]) 
    

    con.close()
    return [*result[:4], time]


def pill(ids):
    con, cur = create_connect()
    while True:
        try:
            result = cur.execute(f"SELECT pills, time_life FROM users WHERE user_id={ids}").fetchall()
            break
        except:
            pass
    count = result[0][0]
    life = result[0][1]
    if count > 0 and life > 0:
        while True:
            try:
                cur.execute(f"UPDATE users SET pills={count - 1}, time_life={life + 240} WHERE user_id={ids}")
                break
            except:
                pass
        con.commit()
        con.close()
        return (True, True, count - 1, get_life_time(life + 240))
    elif life == 0:
        con.close()
        return (True, False)
    else:
        con.close()
        return (False, True)


def elixir(ids):
    con, cur = create_connect()
    while True:
        try:
            result = cur.execute(f"SELECT elixir, time_life FROM users WHERE user_id={ids}").fetchall()
            break
        except:
            pass
    count = result[0][0]
    life = result[0][1]
    if count > 0 and life > 0:
        while True:
            try:
                cur.execute(f"UPDATE users SET elixir={count - 1}, time_life={life + 600} WHERE user_id={ids}")
                break
            except:
                pass
        con.commit()
        con.close()
        return (True, True, count - 1, get_life_time(life + 600))
    elif life == 0:
        con.close()
        return (True, False)
    else:
        con.close()
        return (False, True)


def kits(ids):
    con, cur = create_connect()
    while True:
        try:
            result = cur.execute(f"SELECT kits FROM users WHERE user_id={ids}").fetchall()
            break
        except:
            pass
    count = result[0][0]
    if count > 0:
        while True:
            try:
                cur.execute(f"UPDATE users SET kits={count - 1} WHERE user_id={ids}")
                break
            except:
                pass
        con.commit()
        con.close()
        return (True, count - 1)
    else:
        con.close()
        return (False, 0)

def get_all_id():
    con, cur = create_connect()
    while True:
        try:
            result = cur.execute("SELECT user_id FROM users WHERE 1").fetchall()
            break
        except:
            pass
    result_2 = [i[0] for i in result]
    con.close()
    return result_2


def get_top_pills(friend_list=None):
    con, cur = create_connect()
    if not friend_list:
        while True:
            try:
                result = cur.execute("SELECT user_id, pills, count_infected FROM users WHERE 1").fetchall()
                break
            except:
                pass
    else:
        result = []
        for item in friend_list:
            while True:
                try:
                    result.append(list(cur.execute(f"SELECT user_id, pills, count_infected FROM users WHERE user_id={item}").fetchall()[0]))
                    break
                except:
                    pass
    result.sort(key=lambda x: x[1], reverse = True)
    result = result
    return result


def get_top_infected(friend_list=None):
    con, cur = create_connect()
    if not friend_list:
        while True:
            try:
                result = cur.execute("SELECT user_id, count_infected, pills FROM users WHERE 1").fetchall()
                break
            except:
                pass
    else:
        result = []
        for item in friend_list:
            while True:
                try:
                    result.append(list(cur.execute(f"SELECT user_id, count_infected, pills FROM users WHERE user_id={item}").fetchall()[0]))
                    break
                except:
                    pass
    result.sort(key=lambda x: x[1], reverse = True)
    result = result
    return result


def get_top_time(friend_list=None):
    con, cur = create_connect()
    if not friend_list:
        while True:
            try:
                result = cur.execute("SELECT user_id, time_start, pills, count_infected FROM users WHERE 1").fetchall()
                break
            except:
                pass
    else:
        result = []
        for item in friend_list:
            while True:
                try:
                    result.append(list(cur.execute(f"SELECT user_id, time_start, pills, count_infected FROM users WHERE user_id={item}").fetchall()[0]))
                    break
                except:
                    pass
    result_1 = [get_time(list(i)) for i in result]
    result_1.sort(key=lambda x: x[1].total_seconds(), reverse = True)
    return result_1
    #return result


def get_time(item):
    current_datetime = datetime.now()
    date = str(datetime.now().date()).split("-")
    time = str(datetime.now().time()).split(".")[0].split(":")[:2]

    d1 = datetime(*[int(i) for i in item[1].split()])
    d2 = datetime(*([int(i) for i in date + time]))
    
    time_dead_1 = d2 - d1

    item[1] = time_dead_1

    return item


def add_pill(ids, types):
    con, cur = create_connect()
    while True:
        try:
            pill_count = cur.execute(f"SELECT pills FROM users WHERE user_id={ids}").fetchall()[0][0]
            break
        except:
            pass
    if types == 1:
        while True:
            try:
                is_sub = cur.execute(f"SELECT is_sub FROM users WHERE user_id={ids}").fetchall()[0][0]
                break
            except:
                pass
        if not is_sub:
            while True:
                try:
                    cur.execute(f"UPDATE users SET pills={pill_count + 1}, is_sub={1} WHERE user_id={ids}")
                    break
                except:
                    pass
            con.commit()
            con.close()
            return True
        else:
            con.commit()
            con.close()
            return False
    elif types == 2:
        while True:
            try:
                is_reklama = cur.execute(f"SELECT is_reklama FROM users WHERE user_id={ids}").fetchall()[0][0]
                break
            except:
                pass
        if not is_reklama:
            while True:
                try:
                    cur.execute(f"UPDATE users SET pills={pill_count + 1}, is_reklama={1} WHERE user_id={ids}")
                    break
                except:
                    pass
            con.commit()
            con.close()
            return True
        else:
            con.commit()
            con.close()
            return False


def get_list_reklama():
    con, cur = create_connect()
    while True:
        try:
            result = cur.execute(f"SELECT user_id FROM users WHERE reklama={1}").fetchall()
            break
        except:
            pass
    with open("mailing_list.txt", "w") as file:
        for item in result:
            file.write(str(item[0]) + "\n")
    con.close()


def get_reklama(ids):
    con, cur = create_connect()
    try:
        while True:
            try:
                result = cur.execute(f"SELECT reklama FROM users WHERE user_id={ids}").fetchall()
                break
            except:
                pass
        con.close()
        if result[0][0] > 0:
            return True
        else:
            return False
    except:
        con.close()
        return False


def set_reklama(ids, value):
    con, cur = create_connect()
    while True:
        try:
            cur.execute(f"UPDATE users SET reklama={value} WHERE user_id={ids}")
            break
        except:
            pass
    con.commit()
    con.close()


def time_tick():
    while True:
        sleep(60)
        con, cur = create_connect()
        cur.execute(f"UPDATE users SET time_life=time_life-1 WHERE 1")
        con.commit()
        con.close()


def is_user(ids):
    con, cur = create_connect()
    while True:
        try:
            if cur.execute(f"SELECT time_start FROM users WHERE user_id={ids}").fetchall():
                con.close()
                return True
            else:
                con.close()
                return False
        except:
            pass


def is_life(ids):
    con, cur = create_connect() 
    while True:  
        try:
            if cur.execute(f"SELECT time_life FROM users WHERE user_id={ids}").fetchall()[0][0] > 0:
                con.close()
                return True
            else:
                con.close()
                return False
        except:
            pass


def dead_inside(ids, time):
    con, cur = create_connect()
    while True:
        try:
            cur.execute(f"UPDATE users SET time_life={time} WHERE user_id={ids}")
            con.commit()
            break
        except:
            pass
    con.close()


def get_friends_kits(ids_list):
    con, cur = create_connect()
    list_friend = []

    
    for item in ids_list:
        while True:
            try:
                list_friend.append(list(cur.execute(f"SELECT user_id, time_life, pills FROM users WHERE user_id={item}").fetchall()[0]))
                break
            except:
                pass
    for i in range(len(list_friend)):
        list_friend[i][1] = get_life_time(list_friend[i][1])

            
    list_friend.sort(key=lambda x: x[1][0])
    return list_friend


def add_life_kits(ids):
    con, cur = create_connect()
    while True:
        try:
            life = cur.execute(f"SELECT time_life FROM users WHERE user_id={ids}").fetchall()[0][0]
            cur.execute(f"UPDATE users SET time_life={life + 480} WHERE user_id={ids}")
            con.commit()
            break
        except:
            pass
    con.close()


speed()