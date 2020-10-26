import vk_api
import sqlite3

def get_list_friend(ids):
    vk_session = vk_api.VkApi(app_id=7384283, 
                            token='3430c3273430c3273430c3272334406ffc334303430c3276ab396d8a16a30629b9754ff',  
                            client_secret='GQ1YgQrNmS6hlgYDgalK')

    vk = vk_session.get_api()

    try:
        list_friends = vk.friends.get(user_id=ids)["items"]
    except:
        return []


    vk_session = vk_api.VkApi(token='ee144cc76dde314e4fe3161f41313d06e59b9fd9f6ae2c281481c03867c86caf948f06c132271c431860b')

    bot = vk_session.get_api()

    list_friends_is_member = []


    con = sqlite3.connect("bot_bd.db")
    cur = con.cursor()

    result = [i[0] for i in cur.execute("SELECT user_id FROM users WHERE 1").fetchall()]

    for item in list_friends:
        if item in result:
            list_friends_is_member.append(item)

    return list_friends_is_member


def generate_friend_keyboard(list_friend):
    json = """
{
    "one_time": false,
    "buttons": [
      

"""
    for index, item in enumerate(list_friend):
        if len(item) > 40:
            item = item[:40]
        json += f"""[
            {{
                    "action": {{
                    "type": "text",
                    "label": "{item}"
                }}
            }}]"""
        if index != len(list_friend) - 1:
            json += ","
    json += """
        ]
}"""
    return json