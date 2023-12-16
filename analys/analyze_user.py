import time
from nltk.corpus import stopwords
import json
import pymorphy3
import time
import pandas as pd
from nltk.corpus import stopwords
from analys.vk_api_resolver import VkApiResolver


CREATED_STOPWORDS_PATH = "analys/resourses/stopwords/custom_stopwords.txt"
PROF_KEY_WORDS_PATH = "analys/resourses/professions_keywords.json"
USER_DATA_OBJ_PATH = "analys/resourses/user_data.json"

with open(CREATED_STOPWORDS_PATH, "r", encoding="utf-8") as file:
    my_stopwords = set(file.read().splitlines())

with open(PROF_KEY_WORDS_PATH, "r", encoding="utf-8") as keywords_file:
    professions_keys = json.load(keywords_file)

with open(USER_DATA_OBJ_PATH, "r", encoding="utf-8") as user_data_file:
    user_data = json.load(user_data_file)

stop_words = set(stopwords.words("russian"))
morph = pymorphy3.MorphAnalyzer()


class UserAnaliser(object):
    def __init__(self, id_user, token, user_choise) -> None:
        self._id_user = id_user
        self._token = token
        self._user_choise = user_choise
        self._user_data = user_data.copy()
        self._vk_resolver = VkApiResolver(self._token, self._id_user)

    def clean_user_data(self, com):
        com.columns = ["name", "description"]
        return com

    def create_word_list(self, lst):
        res = []
        for word in lst:
            if word.lower() not in stop_words.union(my_stopwords):
                res.append(word)
        return res

    # создаем список ключевых слов
    def create_keys(self, df):
        keys = []
        for i in df["name"]:
            j = self.create_word_list(i.split())
            for k in j:
                if not k.isalpha():
                    continue
                keys.append(morph.parse(k)[0].normal_form)

            for i in df["description"]:
                if not pd.notna(i):
                    continue
                j = self.create_word_list(i.split())
                for k in j:
                    if not k.isalpha():
                        continue
                    keys.append(morph.parse(k)[0].normal_form)
        return pd.DataFrame(keys)

    def get_user_keys(self):
        k = self._vk_resolver.get_user_subscriptions()
        group_info = {"name": [], "description": []}
        group_info = self._vk_resolver.get_group_info(k)
        com = pd.DataFrame(group_info)
        df = self.clean_user_data(com)
        keys = self.create_keys(df)
        return pd.DataFrame(keys).drop_duplicates()

    def analyze_user(self, user_keywords):
        for category, keys in professions_keys.items():
            # Нет смысла проходиться по категориям, которые неинтересны пользователю
            if category in self._user_choise or len(self._user_choise) == 0:
                for profession, normalized_words in keys.items():
                    for i in user_keywords[0]:
                        if i in normalized_words:
                            self._user_data[profession] += 1

        sorted_user_data = sorted(
            self._user_data.items(), key=lambda x: x[1], reverse=True
        )
        # list типа [('Учитель', 56), ('Археолог', 37), ('Библиотекарь', 35)]
        return sorted_user_data[:3]

    def get_user_professions(self):
        data = self.get_user_keys()
        res = self.analyze_user(data)
        return list(map(lambda x: x[0], res))
