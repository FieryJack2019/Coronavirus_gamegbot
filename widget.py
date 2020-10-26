import vk_api
from database import get_top_infected
from time import sleep

def update_table(): 
    vk_widget = vk_api.VkApi(token='35e5ec051d60d0169d733926e21fa8f19fa793705c92f99c46a9ae2bf31ed6868b3d38f9267c1130800dd')
    vk_widget = vk_widget.get_api()

    code = '''
return {
    "title": "Топ по заражениям",
    "title_url": "vk.com/title_url"
    "head": [
        {
            "text": "🎮 Игрок"
        },
        {
            "text": "Заражения",
            "align": "right"
        }
    ],
    "body": [
        
    '''

    for index, item in enumerate(get_top_infected()):
        if index > 6:
            break
        name = vk_widget.users.get(user_ids=[item[0]])[0]["first_name"]
        code += f'''
        [
            {{
                "icon_id": "id{item[0]}",
                "text": "{name}",
                "url": "https://vk.com/id{item[0]}"
            }},
            {{
                "text": "☠{item[1]}"
            }}
        ],'''


    code += """
    ],
    "more": "Играть",
    "more_url": "https://vk.com/write-145153671",
};"""
    try:
        vk_widget.appWidgets.update(code=code, type="table")
    except:
        pass


def update_time_tick():
    while True:
        update_table()
        sleep(300)
