import re
import nltk
import os
import pymorphy3 # или pymorphy 2
from nltk.corpus import stopwords
import pandas as pd

nltk.download("stopwords")  # Стоп-слова из nltk

stop_words = set(stopwords.words("russian"))

morph = pymorphy3.MorphAnalyzer()

created_stopwords = "custom_stopwords.txt"  # Стоп-слова, созданные вручную -- здесь необязательно менять, тк больше собираем инфу из вк


def contains_special_characters(text):  # есть ли спец-символы
    pattern = re.compile(r'[!@#$%^&*(),.?":{}|<>1234567890]')
    return bool(pattern.search(text))


def contains_emoji(text):  # есть ли эмодзи
    pattern = re.compile(r"[^\w\s]")
    return bool(pattern.search(text))


def contains_digits(text):  # есть ли цифры
    pattern = re.compile(r"\d")
    return bool(pattern.search(text))


def clean_data(filename):  # Приводим csv в стандартный вид
    df = pd.read_csv(filename)

    try:
        news = ["index", "id_group", "name", "description", "count"]
        df.columns = news
        df = df.drop("index", axis=1)
    except ValueError:
        news = ["id_group", "name", "description", "count"]
        df.columns = news

    df = df.drop_duplicates(subset="id_group")
    df = df.dropna()
    return df


def clean_user_data(filename):  # приводим в стандартный вид подписки пользователя
    df = pd.read_csv(filename)

    news = ["name", "description"]
    df.columns = news
    return df


def create_keys(df, created_stopwords):  # создаем список ключевых слов
    with open(created_stopwords, "r", encoding="utf-8") as file:
        my_stopwords = set(file.read().splitlines())

    keys = []

    for i in df["name"]:
        j = i.split()
        j = [
            word
            for word in j
            if word.lower() not in stop_words and word.lower() not in my_stopwords
        ]
        for k in j:
            if (
                not (contains_digits(k))
                and not (contains_emoji(k))
                and not (contains_special_characters(k))
            ):
                keys.append(morph.parse(k)[0].normal_form)

        for i in df["description"]:
            if pd.notna(i):
                j = i.split()
                j = [
                    word
                    for word in j
                    if word.lower() not in stop_words
                    and word.lower() not in my_stopwords
                ]
                for k in j:
                    if (
                        not (contains_digits(k))
                        and not (contains_emoji(k))
                        and not (contains_special_characters(k))
                    ):
                        keys.append(morph.parse(k)[0].normal_form)

    return pd.DataFrame(keys)


def find_keys_files(directory):  # Ищем csv-файлы профессий
    keys_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if ".csv" in file:
                keys_files.append(os.path.join(os.path.relpath(root, directory), file))

    return keys_files


def clean_final_subs():
    directory_path = "/content/drive/MyDrive/professions"

    keys_files_list = find_keys_files(directory_path)

    for file_path in keys_files_list:
        filename = "/content/drive/MyDrive/professions/" + file_path
        df = clean_data(filename)

        keys = create_keys(df, created_stopwords)
        com = pd.DataFrame(keys)

        com.to_csv(filename[:-4] + "_keys.csv", header=False, index=False)
