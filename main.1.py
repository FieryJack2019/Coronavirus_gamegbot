import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint
import requests
import threading
from widget import update_time_tick
from system_pay import *
from database import *
from friends_system import *


#vk = vk_api.VkApi(login = input("Введите логин: "), password = 'Введите пароль: ')
#ee144cc76dde314e4fe3161f41313d06e59b9fd9f6ae2c281481c03867c86caf948f06c132271c431860b
vk_session = vk_api.VkApi(token='ee144cc76dde314e4fe3161f41313d06e59b9fd9f6ae2c281481c03867c86caf948f06c132271c431860b')
longpoll = VkBotLongPoll(vk_session, '145153671')


user_info = {}
is_top_friend = {}
reklama_ras = ""

bot = vk_session.get_api()

update_time = threading.Thread(target=time_tick)
update_top_widget = threading.Thread(target=update_time_tick)

update_time.start()
update_top_widget.start()
#update_time.join()

def message_profile(from_id):
    info = get_statistic(from_id)
    try:
        bot.messages.send(user_id=from_id,
                                message=f"""
☢ Ваша статистика:
💬 ID: {from_id}
💊 Таблеток: {info[0]}
🔮 Эликсира: {info[1]}
💉 Аптечек: {info[2]}
😷 Заражено: {info[3]}
☠ До смерти: {info[4][0]} д {info[4][1]} ч {info[4][2]} мин

🎁 За подписку на паблик и рассылку дается по одной беспатной таблетке!""",
                                random_id=randint(1, 99999999),
                                keyboard=create_keyboard(event.obj.from_id))
    except:
        pass


def create_keyboard(ids):
    if get_reklama(ids):
        return open("keyboard-main_2.json","r",encoding="UTF-8").read()
    else:
        return open("keyboard-main.json","r",encoding="UTF-8").read()



def get_list_admins():
    result = bot.groups.getMembers(group_id=145153671,filter="managers")['items']
    list_admins = []
    for item in result:
        list_admins.append(item["id"])
    return list_admins


def upload_file(ids):
    url = bot.docs.getMessagesUploadServer(type="doc", peer_id=ids)
    b = requests.post(url['upload_url'], files={"file": open('mailing_list.txt', 'rb')}).json()
    c = bot.docs.save(file=b["file"], title="Список рассылка")
    owner_id = c["doc"]['owner_id']
    photo_id = c["doc"]['id']
    attach = 'doc'+str(owner_id)+'_'+str(photo_id)
    return attach


for event in longpoll.listen():
    if event.type == VkBotEventType.VKPAY_TRANSACTION:
        result = check_pay(event.obj.from_id, event.obj.amount // 1000)
        if result[0] == 1 and result[1] == True:
            bot.messages.send(user_id=event.obj.from_id,
                                message="Таблетки успешно зачислены на ваш счет",
                                random_id=randint(1, 99999999),
                                keyboard=create_keyboard(event.obj.from_id))
        elif result[0] == 2 and result[1] == True:
            bot.messages.send(user_id=event.obj.from_id,
                                message="Вы вернулись к жизни 💥",
                                random_id=randint(1, 99999999),
                                keyboard=create_keyboard(event.obj.from_id))

    if event.type == VkBotEventType.GROUP_JOIN:
        if create_new_user(event.obj.user_id, True):
            add_pill(event.obj.user_id, 1)
        else:
            if add_pill(event.obj.user_id, 1):
                try:
                    bot.messages.send(user_id=event.obj.user_id,
                                    message=f"+💊 за подписку на группу",
                                    random_id=randint(1, 99999999),
                                    keyboard=create_keyboard(event.obj.from_id))
                except:
                    pass
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.obj.text == "/получить_файл":
            if event.obj.from_id in get_list_admins():
                get_list_reklama()
                bot.messages.send(user_id=event.obj.from_id,
                                    attachment=upload_file(event.obj.from_id),
                                    random_id=randint(1, 99999999))
        if is_user(event.obj.from_id):
            if is_life(event.obj.from_id):
                if event.obj.text == "☠ Заразить":
                    try:
                        bot.messages.send(user_id=event.obj.from_id,
                                        message="😷 Распространяйте свою реферальную ссылку для заражения, за каждого зараженного человека Вы будете получать 1 таблетку!\n\n" + bot.utils.getShortLink(url=f"https://vk.com/write-{145153671}?ref={event.obj.from_id}&ref_source={event.obj.from_id}")["short_url"],
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                    except:
                        pass
                elif event.obj.text == "😷 Профиль":
                    message_profile(event.obj.from_id)

                elif event.obj.text == "💊 Выпить":
                    result = pill(event.obj.from_id)
                    if not result[1]:
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                        message="Вы умерли.\nДля того чтобы вернуться в игру попросите друзей воскресить вас с помощью аптечки",
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                        except:
                            pass
                    elif result[0]:
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                        message=f"""
💉 Вы успешно выпили 1 таблетку, прибавив 4 часа к своей жизни!

💊 Осталось таблеток: {result[2]}
☠ До смерти: {result[3][0]} д {result[3][1]} ч {result[3][2]} мин
Вы можете получить новые таблетки и эликсир двумя способами, заразив друзей, либо купив в магазине""",
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                        except:
                            pass
                    else:
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                        message=f"""
⛔ У Вас не осталось таблеток, заражайте своих друзей для получения таблеток и эликсира, либо купите в магазине. Таблетки даются за каждого зараженого

🎁 За подписку на паблик дается одна беспатная таблетка!
Отписываться нельзя! Тогда таблетка пропадет
        """,
                                        random_id=randint(1, 99999999),
                                        keyboard=open("inline_keyboard_pay_select.json","r",encoding="UTF-8").read())
                        except:
                            pass
                elif event.obj.text == "🔮 Эликсир":
                    result = elixir(event.obj.from_id)
                    if not result[1]:
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                        message="Вы умерли.\nДля того чтобы вернуться в игру попросите друзей воскресить вас с помощью аптечки",
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                        except:
                            pass
                    elif result[0]:
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                        message=f"""
💉 Вы успешно выпили 1 эликсир, прибавив 10 часов к своей жизни!

🔮 Осталось эликсиров: {result[2]}
☠ До смерти: {result[3][0]} д {result[3][1]} ч {result[3][2]} мин
Вы можете получить новые таблетки и эликсир двумя способами, заразив друзей, либо купив в магазине""",
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                        except:
                            pass
                    else:
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                        message=f"""
⛔ У Вас не осталось бутылок с эликсиром, заражайте своих друзей для получения таблеток и эликсира, либо купите в магазине. Эликсир дается за каждого 5 зараженого

🎁 За подписку на паблик дается одна беспатная таблетка!
Отписываться нельзя! Тогда таблетка пропадет""",
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                        except:
                            pass
                elif event.obj.text == "💉 Аптечка":
                    list_friend = get_list_friend(event.obj.from_id)
                    if not list_friend:
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                        message="Список ваших друзей недоступен, либо у вас их нет! Для того что-бы использовать аптечку, нужно открыть свой профиль!",
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                        except:
                            pass
                    else:
                        result = get_friends_kits(list_friend)
                        users_name = [item["first_name"] + " " + item["last_name"] for item in bot.users.get(user_ids=[i[0] for i in result])]
                        message = {}
                        for i in range(1, 6):
                            try:
                                message[f"{i}. {users_name[i - 1]} — {result[i - 1][1][0]} д {result[i - 1][1][1]} ч {result[i - 1][1][2]} мин | 💊{result[i - 1][2]}"] = result[i - 1][0]
                            except:
                                break
                        user_info[event.obj.from_id] = message
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                            message="Выберите друга которому хотите помочь",
                                            random_id=randint(1, 99999999),
                                            keyboard=generate_friend_keyboard(list(message.keys())))
                        except:
                            pass

                elif event.obj.text == "⭐ Топ":
                    try:
                        bot.messages.send(user_id=event.obj.from_id,
                                        message="▶ Выберите раздел топа с помощью кнопок",
                                        random_id=randint(1, 99999999),
                                        keyboard=open("keyboard-top.json","r",encoding="UTF-8").read())
                    except:
                        pass
                    is_top_friend[event.obj.from_id] = False
                
                elif event.obj.text == "👬 Друзья":
                    try:
                        bot.messages.send(user_id=event.obj.from_id,
                                        message="▶ Выберите раздел топа друзей с помощью кнопок",
                                        random_id=randint(1, 99999999),
                                        keyboard=open("keyboard-top-friend.json","r",encoding="UTF-8").read())
                    except:
                        pass
                    is_top_friend[event.obj.from_id] = True

                elif event.obj.text == "💊 Таблетки":
                    try:
                        if is_top_friend[event.obj.from_id]:
                            friend_list = get_list_friend(event.obj.from_id)
                            if friend_list:
                                result = get_top_pills(friend_list)
                                users_name = [item["first_name"] for item in bot.users.get(user_ids=[i[0] for i in result])]
                                message = ""
                                for i in range(1, 51):
                                    try:
                                        message += f"\n{i}. @id{result[i - 1][0]}({users_name[i - 1]}) — 💊{result[i - 1][1]} | ☠{result[i - 1][2]}"
                                    except:
                                        break
                                my_index = 0
                                for index in range(len(result)):
                                    if result[index][0] == event.obj.from_id:
                                        my_index = index + 1
                                try:
                                    bot.messages.send(user_id=event.obj.from_id,
                                                    message=message,
                                                    random_id=randint(1, 99999999),
                                                    keyboard=open("keyboard-top-friend.json","r",encoding="UTF-8").read())
                                except:
                                    pass
                            else:
                                try:
                                    bot.messages.send(user_id=event.obj.from_id,
                                            message="Список ваших друзей недоступен, либо у вас их нет! Для того что-бы просматривать топ друзей, нужно открыть свой профиль!",
                                            random_id=randint(1, 99999999),
                                            keyboard=open("keyboard-top.json","r",encoding="UTF-8").read())
                                except:
                                    pass
                        else:
                            result = get_top_pills()
                            users_name = [item["first_name"] for item in bot.users.get(user_ids=[i[0] for i in result])]
                            message = ""
                            for i in range(1, 51):
                                try:
                                    message += f"\n{i}. @id{result[i - 1][0]}({users_name[i - 1]}) — 💊{result[i - 1][1]} | ☠{result[i - 1][2]}"
                                except:
                                    break
                            my_index = 0
                            for index in range(len(result)):
                                if result[index][0] == event.obj.from_id:
                                    my_index = index + 1
                            message += f"\n\n▶ Ваше место: {my_index}"
                            try:
                                bot.messages.send(user_id=event.obj.from_id,
                                                message=message,
                                                random_id=randint(1, 99999999),
                                                keyboard=open("keyboard-top.json","r",encoding="UTF-8").read())
                            except:
                                pass
                    except:
                        result = get_top_pills()
                        users_name = [item["first_name"] for item in bot.users.get(user_ids=[i[0] for i in result])]
                        message = ""
                        for i in range(1, 51):
                            try:
                                message += f"\n{i}. @id{result[i - 1][0]}({users_name[i - 1]}) — 💊{result[i - 1][1]} | ☠{result[i - 1][2]}"
                            except:
                                break
                        my_index = 0
                        for index in range(len(result)):
                            if result[index][0] == event.obj.from_id:
                                my_index = index + 1
                        message += f"\n\n▶ Ваше место: {my_index}"
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                                message=message,
                                                random_id=randint(1, 99999999),
                                                keyboard=open("keyboard-top.json","r",encoding="UTF-8").read())
                        except:
                            pass
                            
                elif event.obj.text == "☠ Заражения":
                    try:
                        if is_top_friend[event.obj.from_id]:
                            friend_list = get_list_friend(event.obj.from_id)
                            if friend_list:
                                result = get_top_infected(friend_list)
                                users_name = [item["first_name"] for item in bot.users.get(user_ids=[i[0] for i in result])]
                                message = ""
                                for i in range(1, 51):
                                    try:
                                        message += f"\n{i}. @id{result[i - 1][0]}({users_name[i - 1]}) — ☠{result[i - 1][1]} | 💊{result[i - 1][2]}"
                                    except:
                                        break
                                my_index = 0
                                for index in range(len(result)):
                                    if result[index][0] == event.obj.from_id:
                                        my_index = index + 1
                                try:
                                    bot.messages.send(user_id=event.obj.from_id,
                                                    message=message,
                                                    random_id=randint(1, 99999999),
                                                    keyboard=open("keyboard-top-friend.json","r",encoding="UTF-8").read())
                                except:
                                    pass
                            else:
                                try:
                                    bot.messages.send(user_id=event.obj.from_id,
                                            message="Список ваших друзей недоступен, либо у вас их нет! Для того что-бы просматривать топ друзей, нужно открыть свой профиль!",
                                            random_id=randint(1, 99999999),
                                            keyboard=open("keyboard-top.json","r",encoding="UTF-8").read())
                                except:
                                    pass
                        else:
                            result = get_top_infected()
                            users_name = [item["first_name"] for item in bot.users.get(user_ids=[i[0] for i in result])]
                            message = ""
                            for i in range(1, 51):
                                try:
                                    message += f"\n{i}. @id{result[i - 1][0]}({users_name[i - 1]}) — ☠{result[i - 1][1]} | 💊{result[i - 1][2]}"
                                except:
                                    break
                            my_index = 0
                            for index in range(len(result)):
                                if result[index][0] == event.obj.from_id:
                                    my_index = index + 1
                            message += f"\n\n▶ Ваше место: {my_index}"
                            try:
                                bot.messages.send(user_id=event.obj.from_id,
                                                message=message,
                                                random_id=randint(1, 99999999),
                                                keyboard=open("keyboard-top.json","r",encoding="UTF-8").read())
                            except:
                                pass
                    except:
                        result = get_top_infected()
                        users_name = [item["first_name"] for item in bot.users.get(user_ids=[i[0] for i in result])]
                        message = ""
                        for i in range(1, 51):
                            try:
                                message += f"\n{i}. @id{result[i - 1][0]}({users_name[i - 1]}) — ☠{result[i - 1][1]} | 💊{result[i - 1][2]}"
                            except:
                                break
                        my_index = 0
                        for index in range(len(result)):
                            if result[index][0] == event.obj.from_id:
                                my_index = index + 1
                        message += f"\n\n▶ Ваше место: {my_index}"
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                                message=message,
                                                random_id=randint(1, 99999999),
                                                keyboard=open("keyboard-top.json","r",encoding="UTF-8").read())
                        except:
                            pass
                elif event.obj.text == "⌛ Время жизни":
                    try:
                        if is_top_friend[event.obj.from_id]:
                            friend_list = get_list_friend(event.obj.from_id)
                            if friend_list:
                                result = get_top_time(friend_list)
                                users_name = [item["first_name"] for item in bot.users.get(user_ids=[i[0] for i in result])]
                                message = ""
                                for i in range(1, 51):
                                    try:
                                        time = str(result[i - 1][1]).split(', ')

                                        if len(time) == 2:
                                            time[0] = time[0].split()[0] + " д"
                                            time_2 = time[1].split(":")
                                            time[1] = time_2[0] + " ч " + time_2[1] + " мин "
                                            time = ' '.join(time)
                                        else:
                                            time_2 = time[0].split(":")
                                            time = time_2[0] + " ч " + time_2[1] + " мин "
                                        message += f"\n{i}. @id{result[i - 1][0]}({users_name[i - 1]}) — {time} | 💊{result[i - 1][2]} | ☠{result[i - 1][3]}"
                                    except:
                                        break
                                my_index = 0
                                for index in range(len(result)):
                                    if result[index][0] == event.obj.from_id:
                                        my_index = index + 1
                                try:
                                    bot.messages.send(user_id=event.obj.from_id,
                                                    message=message,
                                                    random_id=randint(1, 99999999),
                                                    keyboard=open("keyboard-top-friend.json","r",encoding="UTF-8").read())
                                except:
                                    pass
                            else:
                                try:
                                    bot.messages.send(user_id=event.obj.from_id,
                                            message="Список ваших друзей недоступен, либо у вас их нет! Для того что-бы просматривать топ друзей, нужно открыть свой профиль!",
                                            random_id=randint(1, 99999999),
                                            keyboard=open("keyboard-top.json","r",encoding="UTF-8").read())
                                except:
                                    pass
                        else:
                            result = get_top_time()
                            users_name = [item["first_name"] for item in bot.users.get(user_ids=[i[0] for i in result])]
                            message = ""
                            for i in range(1, 51):
                                try:
                                    time = str(result[i - 1][1]).split(', ')

                                    if len(time) == 2:
                                        time[0] = time[0].split()[0] + " д"
                                        time_2 = time[1].split(":")
                                        time[1] = time_2[0] + " ч " + time_2[1] + " мин "
                                        time = ' '.join(time)
                                    else:
                                        time_2 = time[0].split(":")
                                        time = time_2[0] + " ч " + time_2[1] + " мин "
                                    message += f"\n{i}. @id{result[i - 1][0]}({users_name[i - 1]}) — {time} | 💊{result[i - 1][2]} | ☠{result[i - 1][3]}"
                                except:
                                    break
                            my_index = 0
                            for index in range(len(result)):
                                if result[index][0] == event.obj.from_id:
                                    my_index = index + 1
                            message += f"\n\n▶ Ваше место: {my_index}"
                            try:
                                bot.messages.send(user_id=event.obj.from_id,
                                                message=message,
                                                random_id=randint(1, 99999999),
                                                keyboard=open("keyboard-top.json","r",encoding="UTF-8").read())
                            except:
                                pass
                    except:
                        result = get_top_time()
                        users_name = [item["first_name"] for item in bot.users.get(user_ids=[i[0] for i in result])]
                        message = ""
                        for i in range(1, 51):
                            try:
                                time = str(result[i - 1][1]).split(', ')

                                if len(time) == 2:
                                    time[0] = time[0].split()[0] + " д"
                                    time_2 = time[1].split(":")
                                    time[1] = time_2[0] + " ч " + time_2[1] + " мин "
                                    time = ' '.join(time)
                                else:
                                    time_2 = time[0].split(":")
                                    time = time_2[0] + " ч " + time_2[1] + " мин "
                                message += f"\n{i}. @id{result[i - 1][0]}({users_name[i - 1]}) — {time} | 💊{result[i - 1][2]} | ☠{result[i - 1][3]}"
                            except:
                                break
                        my_index = 0
                        for index in range(len(result)):
                            if result[index][0] == event.obj.from_id:
                                my_index = index + 1
                        message += f"\n\n▶ Ваше место: {my_index}"
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                                message=message,
                                                random_id=randint(1, 99999999),
                                                keyboard=open("keyboard-top.json","r",encoding="UTF-8").read())
                        except:
                            pass
                elif event.obj.text == "▶ Назад":
                    try:
                        bot.messages.send(user_id=event.obj.from_id,
                                        message="▶ Выберите раздел топа с помощью кнопок",
                                        random_id=randint(1, 99999999),
                                        keyboard=open("keyboard-top.json","r",encoding="UTF-8").read())
                    except:
                        pass
                    is_top_friend[event.obj.from_id] = False
                
                elif event.obj.text == "💯 Подписка на рассылку":
                    set_reklama(event.obj.from_id, 1)
                    if add_pill(event.obj.from_id, 2):
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                        message="+💊 за подписку на рекламную рассылку",
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                        except:
                            pass
                    else:
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                        message="Спасибо за подписку на рассылку",
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                        except:
                            pass
                elif event.obj.text == "💯 Отписаться от рассылки":
                    set_reklama(event.obj.from_id, 0)
                    try:
                        bot.messages.send(user_id=event.obj.from_id,
                                        message="Вы отписались от рекламной рассылки(",
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                    except:
                        pass

                elif event.obj.text == "💳 Оплатить":
                    try:
                        bot.messages.send(user_id=event.obj.from_id,
                                        message="Выберите количество:",
                                        random_id=randint(1, 99999999),
                                        keyboard=open("keyboard-select-pay.json","r",encoding="UTF-8").read())
                    except:
                        pass
                
                elif event.obj.text in ["💊 1", "💊 5", "💊 10", "💊 50"]:
                    create_new_pay(event.obj.from_id, event.obj.text.split()[1] + " таблеток")
                    try:
                        bot.messages.send(user_id=event.obj.from_id,
                                        message="Оплатите",
                                        random_id=randint(1, 99999999),
                                        keyboard=open(create_pay_keyboard(int(event.obj.text.split()[1]) * 10),"r",encoding="UTF-8").read())
                    except:
                        pass
                else:
                    if event.obj.ref:
                        if create_new_user(event.obj.from_id):
                            infected_user(event.obj.ref)
                            result_referal = bot.users.get(user_ids=[int(event.obj.ref)])
                            try:
                                bot.messages.send(user_id=event.obj.from_id,
                                        message=f"""
✅ @id{event.obj.ref}(Друг) заразил вас.
💊 Вы умрете через: 24 часов.
❤ Заразите других командой "заразить" и проживите дольше."""
                                        ,
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                            except:
                                pass
                            try:
                                bot.messages.send(user_id=int(event.obj.ref),
                                                message=f"""➕💊 @id{event.obj.from_id}(Друг) зарегистрировался по вашей реферальной ссылке, Вы получили 1 таблетку!""",
                                                random_id=randint(1, 99999999))
                            except:
                                pass
                        else:
                            message_profile(event.obj.from_id)
                    else:
                        if create_new_user(event.obj.from_id):
                            try:
                                bot.messages.send(user_id=event.obj.from_id,
                                        message=f"""
Ты зашел в опасную зону и заразился коронавирусом, чтобы излечиться, тебе нужно собирать таблетки, чтобы их получать заражай друзей"""
                                        ,
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                            except:
                                pass
                        else:
                            try:
                                if user_info[event.obj.from_id]:
                                    result = kits(event.obj.from_id)

                                    if result[0]:
                                        add_life_kits(user_info[event.obj.from_id][event.obj.text])

                                        try:
                                            bot.messages.send(user_id=event.obj.from_id,
                                        message=f"Вы успешно добавил 8 часов жизни своему @id{user_info[event.obj.from_id][event.obj.text]}(другу)\n\n🧰 Осталось аптечек: {result[1]} ",
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                                        except:
                                            pass
                                        
                                    else:
                                        try:
                                            bot.messages.send(user_id=event.obj.from_id,
                                                message="""⛔ У Вас не осталось аптечек, заражайте своих друзей для получения таблеток и эликсира, либо купите в магазине. Аптечки даются за каждого 3 зараженого

🎁 За подписку на паблик дается одна беспатная таблетка!
Отписываться нельзя! Тогда таблетка пропадет""",
                                                random_id=randint(1, 99999999),
                                                keyboard=create_keyboard(event.obj.from_id))
                                        except:
                                            pass
                                    user_info[event.obj.from_id] = []
                                else:
                                    message_profile(event.obj.from_id)
                            except:
                                message_profile(event.obj.from_id)
            else:
                if event.obj.text == "👼 Возродиться":
                    pills = get_statistic(event.obj.from_id)[0]
                    if pills >= 2:
                        dead_inside(event.obj.from_id, 480)
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                        message=f"""
Вы вернулись к жизни 💥
""",
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                        except:
                            pass
                    else:
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                    message=f"""
Для возрождения на балансе должно быть не менее 2 таблеток! Либо заразите двух друзей!
У вас таблеток: {pills}
""",
                                    random_id=randint(1, 99999999),
                                    keyboard=open("inline_keyboard_dead.json","r",encoding="UTF-8").read())
                        except:
                            pass
                elif event.obj.text == "💀 Заразить":
                    try:
                        bot.messages.send(user_id=event.obj.from_id,
                                        message="😷 Распространяйте свою реферальную ссылку для заражения, за каждого зараженного человека Вы будете получать 1 таблетку!\n\n" + bot.utils.getShortLink(url=f"https://vk.com/write-{145153671}?ref={event.obj.from_id}&ref_source={event.obj.from_id}")["short_url"],
                                        random_id=randint(1, 99999999),
                                        keyboard=create_keyboard(event.obj.from_id))
                    except:
                        pass
                elif event.obj.text == "💳 Оплатить":
                    create_new_pay(event.obj.from_id, "воскрешение")
                    try:
                        bot.messages.send(user_id=event.obj.from_id,
                                        message="Стоимость воскрешения составляет 40 руб.\nДля оплаты нажмите кнопку ниже",
                                        random_id=randint(1, 99999999),
                                        keyboard=open(create_pay_keyboard(40),"r",encoding="UTF-8").read())
                    except:
                        pass

                else:
                    try:
                        bot.messages.send(user_id=event.obj.from_id,
                                        message=f"""
💀 Коронавирус оказался сильнее вашего иммунитета. ⚡ Вы можете возродиться с помощью команды «Возродиться»!
    """,
                                        random_id=randint(1, 99999999),
                                        keyboard=open("keyboard-dead.json","r",encoding="UTF-8").read())
                    except:
                        pass
        else:
            if event.obj.text == "/получить_файл":
                if event.obj.from_id in get_list_admins():
                    get_list_reklama()
                    bot.messages.send(user_id=event.obj.from_id,
                                attachment=upload_file(event.obj.from_id),
                                random_id=randint(1, 99999999))

            else:
                if event.obj.ref:
                    if create_new_user(event.obj.from_id):
                        infected_user(event.obj.ref)
                        result_referal = bot.users.get(user_ids=[int(event.obj.ref)])
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                message=f"""
✅ @id{event.obj.ref}(Друг) заразил вас.
💊 Вы умрете через: 24 часов.
❤ Заразите других командой "заразить" и проживите дольше."""
                                ,
                                random_id=randint(1, 99999999),
                                keyboard=create_keyboard(event.obj.from_id))
                        except:
                            pass
                        try:
                            bot.messages.send(user_id=int(event.obj.ref),
                                            message=f"""➕💊 @id{event.obj.from_id}(Друг) зарегистрировался по вашей реферальной ссылке, Вы получили 1 таблетку!""",
                                            random_id=randint(1, 99999999))
                        except:
                            pass
                    else:
                        message_profile(event.obj.from_id)
                else:
                    if create_new_user(event.obj.from_id):
                        try:
                            bot.messages.send(user_id=event.obj.from_id,
                                message=f"""
    Ты зашел в опасную зону и заразился коронавирусом, чтобы излечиться, тебе нужно собирать таблетки, чтобы их получать заражай друзей"""
                                ,
                                random_id=randint(1, 99999999),
                                keyboard=create_keyboard(event.obj.from_id))
                        except:
                            pass
                    else:
                        message_profile(event.obj.from_id)

