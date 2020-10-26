import sqlite3


def create_new_pay(ids, types):
    print(types)
    if types == "1 таблеток":
        count_pay = 1
    elif types == "5 таблеток":
        count_pay = 2
    elif types == "10 таблеток":
        count_pay = 100
    elif types == "50 таблеток":
        count_pay = 500
    elif types == "воскрешение":
        count_pay = 40
    
    con = sqlite3.connect("bot_bd_pay.db")
    cur = con.cursor()

    result = cur.execute(f"SELECT * FROM users_pay WHERE id={ids}").fetchall()
    if result:
        cur.execute(f"UPDATE users_pay SET count_pay={count_pay}, type_pay='{types}' WHERE id={ids}")
    else:
        cur.execute(f"INSERT INTO users_pay(id, count_pay, type_pay) VALUES({ids}, {count_pay}, '{types}')")
    con.commit()
    con.close()


def check_pay(ids, count_pay):
    print(count_pay)
    con = sqlite3.connect("bot_bd_pay.db")
    cur = con.cursor()

    result = cur.execute(f"SELECT type_pay FROM users_pay WHERE id={ids}").fetchall()
    con.close()
    types = ""
    if result:
        types = result[0][0]
    if types == "1 таблеток":
        if count_pay >= 1:
            pay_ok(ids, types)
            return (1, True)
        else:
            return (1, False)
    elif types == "5 таблеток":
        if count_pay >= 2:
            pay_ok(ids, types)
            return (1, True)
        else:
            return (1, False)
    elif types == "10 таблеток":
        if count_pay >= 100:
            pay_ok(ids, types)
            return (1, True)
        else:
            return (1, False)
    elif types == "50 таблеток":
        if count_pay >= 500:
            pay_ok(ids, types)
            return (1, True)
        else:
            return (1, False)
    elif types == "воскрешение":
        if count_pay >= 40:
            pay_ok(ids, types)
            return (2, True)
        else:
            return (2, False)


def pay_ok(ids, types):
    con = sqlite3.connect("bot_bd.db")
    cur = con.cursor()

    if "таблеток" in types:
        pills = cur.execute(f"SELECT pills FROM users WHERE user_id={ids}").fetchall()[0][0]
        cur.execute(f"UPDATE users SET pills={pills + int(types.split()[0])} WHERE user_id={ids}")
    elif types == "воскрешение":
        cur.execute(f"UPDATE users SET time_life={1440} WHERE user_id={ids}")
    con.commit()
    con.close()

    con = sqlite3.connect("bot_bd_pay.db")
    cur = con.cursor()

    cur.execute(f"DELETE FROM users_pay WHERE id=?", (ids,))
    con.commit()
    con.close()


def create_pay_keyboard(count):
    with open("pay_inline.json", "w", encoding="UTF-8") as file:
        file.write(f"""
{{
    "inline": true,
    "buttons": [
      [{{
        "action": {{
          "type": "vkpay",
          "payload": "{{\\"button\\":\\"1\\"}}",
          "hash": "action=pay-to-group&group_id=145153671&amount={count}"
        }}
      }}]
    ]
  }}
""")
    return "pay_inline.json"