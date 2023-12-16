import pandas as pd
import vk
import time
import nltk
from nltk.corpus import stopwords
import pymorphy3
from analys.prof_info import file_mapping, user_data
import unicodedata

nltk.download('stopwords')
morph = pymorphy3.MorphAnalyzer()

CREATED_STOPWORDS_PATH = "analys/stopwords/custom_stopwords.txt"  
PROF_KEYS_FOLDER = "analys/data/professions_keys/"

with open(CREATED_STOPWORDS_PATH, "r", encoding="utf-8") as file:
    my_stopwords = set(file.read().splitlines())

stop_words = set(stopwords.words("russian"))


class UserAnaliser(object):
    def __init__(self,id_user,token,user_choise) -> None:
        self._id_user = id_user
        self._token = token
        self._user_choise = user_choise
        self._user_data = user_data.copy()

    def _get_user_subscriptions(self):
        vk_api = vk.API(self._token)
        response = vk_api.users.getSubscriptions(user_id=self._id_user, v=5.92)
        return response["groups"]["items"][:15]
    
    def _get_group_info(self,group_id):
        vk_api = vk.API(self._token)
        response = vk_api.groups.getById(group_id=group_id, fields="description", v=5.92)
        return response[0]["name"], response[0]["description"]

    def clean_user_data(self,com):
        com.columns = ["name", "description"]
        return com

    def create_word_list(self,lst):
        res = []
        for word in lst:
            if word.lower() not in stop_words.union(my_stopwords):
                res.append(word)
        return res

    # создаем список ключевых слов
    def create_keys(self,df):  
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
        k = self._get_user_subscriptions()
        group_info = {"name": [], "description": []}

        for sub in k:
            time.sleep(0.5)
            tmp = self._get_group_info(sub)
            name, description = tmp
            group_info["name"].append(name)
            group_info["description"].append(description)
        
        com = pd.DataFrame(group_info)
        df = self.clean_user_data(com)
        keys = self.create_keys(df)
        return pd.DataFrame(keys).drop_duplicates()
    
    def analyze_user(self,user_keywords):  
        user_data = self._user_data
        for category, keys in file_mapping.items():
            # Нет смысла проходиться по категориям, которые неинтересны пользователю
            if category in self._user_choise  or len(self._user_choise)==0:
                for file_name, profession in keys.items():
                    # Правильно прописываем путь к папке с keys
                    filename = PROF_KEYS_FOLDER + file_name
                    filename = unicodedata.normalize("NFKC", filename)
                    df = pd.read_csv(filename + "_keys.csv", header=None)
                    normalized_words = df[0]
                    for i in user_keywords[0]:
                        if i in normalized_words.values:
                            self._user_data[profession] += 1
        sorted_user_data = sorted(user_data.items(), key=lambda x: x[1], reverse=True)
        #list типа [('Учитель', 56), ('Археолог', 37), ('Библиотекарь', 35)]
        return sorted_user_data[:3]

    def get_user_professions(self):
        data = self.get_user_keys()
        res = self.analyze_user(data)
        return list(map(lambda x: x[0],res))
