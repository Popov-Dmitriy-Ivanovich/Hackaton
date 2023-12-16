import pandas as pd
import vk
import time
from get_info_by_public import get_groups_info
from cleaning import clean_user_data, create_keys
import json

created_stopwords = "stopwords/custom_stopwords.json"  # Путь к созданным стоп-словам


def get_user_subscriptions(
    id_user, token
):  # Получаем подписки пользователей (int id_user)
    vk_api = vk.API(token)
    try:
        response = vk_api.users.getSubscriptions(user_id=id_user, v=5.92)
        subscriptions = response["groups"]["items"][:15]
        return subscriptions
    except Exception as e:
        return None


def get_user_keys(id_user, token):  # Получаем ключевые слова пользователя
    k = get_user_subscriptions(id_user, token)

    group_info = {"name": [], "description": []}

    for sub in k:
        group_info_result = get_groups_info(sub, token)

        if group_info_result:
            time.sleep(1)  # Лучше использовать 3 секунды
            name, description = group_info_result
            group_info["name"].append(name)
            group_info["description"].append(description)
        else:
            print("ошибка получения группы" + sub)

    com = pd.DataFrame(group_info)

    df = clean_user_data(com)

    keys = create_keys(df, created_stopwords)
    if keys:
        data = pd.DataFrame(keys)
        data = data.drop_duplicates()
        return data
    else:
        return None


def analyze_user(
    user_choice, user_keywords, id_user
):  # Анализ ключевых слов пользователя
    with open(
        "professions_keys/keys_data.json",
        "r",
        encoding="utf-8",
    ) as json_file:
        key_data = json.load(json_file)

    user_data = {}

    for category, professions in key_data.items():
        if category in user_choice:
            for profession, keywords in professions.items():
                normalized_words = [word.lower() for word in keywords]

                for i in user_keywords[0]:
                    if i.lower() in normalized_words:
                        if profession not in user_data:
                            user_data[profession] = 0
                        user_data[profession] += 1

    results = []
    for i in range(3):
        max_key = max(user_data, key=user_data.get)
        max_value = user_data.pop(max_key)
        results.append((max_key, max_value))

    for profession, value in results:
        print(f"{profession}: {value}")

    if results:
        return results
    else:
        print("ошибка получения результатов")
        return None


user_choice = ["Наука и образование"]  # Передаем массив с выбранными специальностями
token = ""
id_user = 175006893
data = get_user_keys(id_user, token)
if data:
    k = analyze_user(user_choice, data, id_user)
else:
    print("ошибка получения ключевых слов пользователя")
