import pandas as pd
import vk
import time
from prof_info import file_mapping, user_data
from get_info_by_public import get_groups_info
from cleaning import clean_user_data, create_keys
import unicodedata

created_stopwords = (
    "/home/evm/Hackaton/analys/stopwords/custom_stopwords.txt"  # Путь к созданным стоп-словам
)


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

    filename = str(id_user) + "_piblics.csv"

    group_info = {"name": [], "description": []}

    for sub in k:
        if get_groups_info(sub, token):
            time.sleep(1) # А лучше 3
            name, description = get_groups_info(sub, token)
            group_info["name"].append(name)
            group_info["description"].append(description)
        com = pd.DataFrame(group_info)
        com.to_csv(filename, index=False)

    df = clean_user_data(filename)

    keys = create_keys(df, created_stopwords)
    print(keys)
    data = pd.DataFrame(keys)
    data = data.drop_duplicates()
    return data


def analyze_user(
    user_choice, user_keywords, id_user
):  # Анализ ключевых слов пользователя
    with open(str(id_user) + ".txt", "w", encoding="utf-8") as output_file:
        for category, keys in file_mapping.items():
            if (
                category in user_choice
            ):  # Нет смысла проходиться по категориям, которые неинтересны пользователю
                for file_name, profession in keys.items():
                    filename = (
                        "/home/evm/Documents/professions_keys/" + file_name
                    )  # Правильно прописываем путь к папке с keys
                    filename = unicodedata.normalize("NFKC", filename)
                    df = pd.read_csv(filename + "_keys.csv", header=None)

                    normalized_words = df[0]

                    print(normalized_words.values)
                    for i in user_keywords[0]:
                        if i in normalized_words.values:
                            user_data[profession] += 1
                            print(i)
                            output_file.write(i + "\n")


    sorted_user_data = sorted(user_data.items(), key=lambda x: x[1], reverse=True)

    top_3 = sorted_user_data[:3] #list типа [('Учитель', 56), ('Археолог', 37), ('Библиотекарь', 35)]
    for profession, value in top_3:
        print(f"{profession}: {value}")
    return top_3


user_choice = ["Наука и образование"]  # Передаем массив с выбранными специальностями
token = ""
id_user = 425735901
data = get_user_keys(id_user, token)
k = analyze_user(user_choice, data, id_user)
