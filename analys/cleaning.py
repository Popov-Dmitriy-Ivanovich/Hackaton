import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

stop_words = set(stopwords.words('russian')) # Стоп-слова по типу "и, да, но, без итд"


def contains_special_characters(text): # Удаление спецсимфолов
    pattern = re.compile(r'[!@#$%^&*(),.?":{}|<>1234567890]')
    return bool(pattern.search(text))

def contains_emoji(text): # Удаление эмодзи
    pattern = re.compile(r'[^\w\s]')
    return bool(pattern.search(text))

def contains_digits(text): # Удаление цифр
    pattern = re.compile(r'\d')
    return bool(pattern.search(text))

def clean_data(filename):
  df = pd.read_csv(filename)
  news = ["index", "id_group", "name", "description", "count"] # Необязательно,
  df.columns = news                                            # если есть названия
  df = df.drop("index", axis=1)                                # и удалены индексы
  df = (df.drop_duplicates(subset="id_group"))

def create_keys(filename): # Создаем набор ключей, очищенный 
  df = pd.read_csv(filename)
  keys = []
  for i in df["name"]:
    j = i.split()
    j = [word for word in j if word.lower() not in stop_words]
    for k in j:
      
      if not(contains_digits(k)) and not(contains_emoji(k)) and not(contains_special_characters(k)):
        keys.append(k)


    for i in df["description"]:
        if pd.notna(i):
          j=i.split()
          j = [word for word in j if word.lower() not in stop_words]
          for k in j:
              if not(contains_digits(k)) and not(contains_emoji(k)) and not(contains_special_characters(k)):
                keys.append(k)
  return keys

filename = '/content/drive/MyDrive/hackaton2/Образование.csv'

print(create_keys(filename))


